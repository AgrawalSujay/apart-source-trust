"""Evaluate the base and both adapters on Kaggle. Dry-run uses only the standard library."""
import argparse
import gc
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ARMS = {"qwen3.5-4b-base": None, "qwen3.5-4b-ft-en": "en", "qwen3.5-4b-ft-multi": "multi"}
PUBLIC_BASE = "Qwen/Qwen3.5-4B"
CAP = 400
KAGGLE_WORKING = Path("/kaggle/working")


class NonFiniteScores(RuntimeError):
    pass


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def valid_rows(path, arm, ids):
    """Preserve complete lines and recover from an interrupted final append."""
    if not path.exists():
        return set()
    seen = set()
    with path.open("r+b") as fh:
        while line := fh.readline():
            if not line.endswith(b"\n"):
                fh.seek(-len(line), os.SEEK_CUR)
                fh.truncate()
                break
            row = json.loads(line)
            if row["id"] not in ids or row["id"] in seen or row["model"] != arm or row["rep"] != 0:
                raise ValueError(f"{path} has an unexpected or duplicate result {row.get('id')!r}")
            if row["finish"] not in ("stop", "length") or row["error"] is not None:
                raise ValueError(f"{path} has a failed or invalid result {row['id']!r}")
            seen.add(row["id"])
    return seen


def row_for(episode, arm, reply, tokens):
    return {"id": episode["id"], "model": arm, "rep": 0, "reply": reply,
            "finish": "length" if tokens >= CAP else "stop",
            "usage": {"completion_tokens": tokens}, "error": None, "cap_retry": False}


def append_rows(path, rows):
    with path.open("a", encoding="utf-8") as dest:
        dest.writelines(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
        dest.flush()
        os.fsync(dest.fileno())


def render_prompt(tokenizer, prompt):
    # Training rows supplied the same flattened prompt as the prompt/completion input.
    return tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}], tokenize=False,
        add_generation_prompt=True, enable_thinking=False,
    )


def collect(arm, path, pending, total, batch_size, generate):
    done = total - len(pending)
    offset = 0
    started = time.monotonic()
    first = True
    while offset < len(pending):
        batch = pending[offset:offset + batch_size]
        answers = generate(batch, first)
        if len(answers) != len(batch):
            raise RuntimeError("Batch returned the wrong number of replies")
        append_rows(path, [row_for(ep, arm, reply, tokens)
                           for ep, (reply, tokens) in zip(batch, answers)])
        offset += len(batch)
        elapsed = time.monotonic() - started
        if first:
            print(f"{arm}: first batch {elapsed:.1f}s; estimated time for this arm "
                  f"{elapsed * total / len(batch) / 60:.1f} min at this batch rate.", flush=True)
            first = False
        if offset == len(batch) or done + offset == total or offset % (batch_size * 10) == 0:
            eta = elapsed * (len(pending) - offset) / offset / 60
            print(f"{arm}: {done + offset}/{total} done, ~{eta:.1f} min remaining.", flush=True)


def resolve_base(root, override, revision):
    from huggingface_hub import HfApi
    from huggingface_hub.errors import HfHubHTTPError

    choices = {read_json(root / "adapters" / arm / "adapter_config.json")["base_model_name_or_path"]
               for arm in ("en", "multi")}
    if len(choices) != 1:
        raise ValueError(f"Adapters name different bases: {sorted(choices)}")
    preferred = override or choices.pop()
    hub = HfApi()
    candidates = [preferred, PUBLIC_BASE] if preferred != PUBLIC_BASE and not override else [preferred]
    for candidate in candidates:
        try:
            model = hub.model_info(candidate, revision=revision)
        except HfHubHTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None
            if status not in (401, 403, 404) or candidate == candidates[-1]:
                raise
            print(f"{candidate} unavailable (HTTP {status}); trying {PUBLIC_BASE} for all arms.", flush=True)
            continue
        if any(f.rfilename.endswith(".safetensors") and f.rfilename.startswith("model")
               for f in model.siblings or ()):
            if not model.sha:
                raise RuntimeError(f"Could not resolve a commit revision for {candidate}")
            return candidate, model.sha
        print(f"{candidate} has no base safetensors files.", flush=True)
    raise RuntimeError("No compatible base weights found; select a readable model with --base.")


def attach_adapter(base, folder):
    from peft import PeftConfig, get_peft_model, set_peft_model_state_dict
    from peft.utils.save_and_load import load_peft_weights

    state = load_peft_weights(str(folder), device="cpu")
    original_modules = dict(base.named_modules())
    modules = set()
    for key in state:
        prefix = "base_model.model."
        name, _, suffix = key.rpartition(".lora_")
        if not name.startswith(prefix) or suffix not in ("A.weight", "B.weight"):
            raise ValueError(f"Unexpected adapter tensor in {folder.name}: {key}")
        target = name.removeprefix(prefix)
        if not target.startswith("model.language_model.layers.") or target not in original_modules:
            raise ValueError(f"Adapter module absent from the base language model: {target}")
        modules.add(target)
    if not modules:
        raise ValueError(f"No language-model LoRA tensors in {folder}")
    model = get_peft_model(base, PeftConfig.from_pretrained(str(folder)), autocast_adapter_dtype=False)
    result = set_peft_model_state_dict(model, state, adapter_name="default")
    missing = [key for key in result.missing_keys if ".lora_" in key]
    if missing or result.unexpected_keys:
        raise RuntimeError(f"{folder.name}: PEFT keys did not match. "
                           f"Missing adapter keys: {missing}; unexpected keys: {result.unexpected_keys}")
    print(f"{folder.name}: loaded {len(state)} LoRA tensors across {len(modules)} language-model layers/projections.",
          flush=True)
    return model


def torch_generator(model, tokenizer, torch, device):
    from transformers import LogitsProcessor

    class CheckFinite(LogitsProcessor):
        def __call__(self, input_ids, scores):
            if not torch.isfinite(scores).all().item():
                raise NonFiniteScores("NaN/inf in the first batch's generation scores")
            return scores

    eos = model.generation_config.eos_token_id
    eos = set(eos if isinstance(eos, (list, tuple)) else [eos])
    eos.add(tokenizer.eos_token_id)
    eos.discard(None)

    def generate(batch, first):
        prompts = [render_prompt(tokenizer, row["prompt"]) for row in batch]
        inputs = tokenizer(prompts, padding=True, add_special_tokens=False,
                           return_token_type_ids=False, return_tensors="pt").to(device)
        with torch.inference_mode():
            sequences = model.generate(
                **inputs, do_sample=False, max_new_tokens=CAP, use_cache=True,
                pad_token_id=tokenizer.pad_token_id, eos_token_id=sorted(eos),
                logits_processor=[CheckFinite()] if first else None,
            )
        result = []
        for tokens in sequences[:, inputs["input_ids"].shape[1]:].tolist():
            for i, token in enumerate(tokens):
                if token in eos:
                    tokens = tokens[:i + 1]
                    break
            result.append((tokenizer.decode(tokens, skip_special_tokens=True).strip(), len(tokens)))
        return result

    return generate


def run_precision(root, out, arm, pending, total, batch_size, tokenizer, base, revision, precision, meta):
    import torch
    from transformers import Qwen3_5ForConditionalGeneration

    path = out / f"{arm}.jsonl"
    print(f"{arm}: {base}@{revision}, {precision}, {len(pending)} pending, batch {batch_size}", flush=True)
    # Attach before CPU offloading so Accelerate registers both base and adapter tensors.
    load_device = "cpu" if precision == "float32" else 0
    base_model = Qwen3_5ForConditionalGeneration.from_pretrained(
        base, revision=revision, dtype=getattr(torch, precision), device_map={"": load_device},
    )
    adapter = ARMS[arm]
    model = attach_adapter(base_model, root / "adapters" / adapter) if adapter else base_model
    if precision == "float32":
        from accelerate import dispatch_model, infer_auto_device_map

        memory = {i: int(torch.cuda.get_device_properties(i).total_memory * 0.86)
                  for i in range(torch.cuda.device_count())} | {"cpu": "15GiB"}
        placement = infer_auto_device_map(model, max_memory=memory,
                                          no_split_module_classes=base_model._no_split_modules)
        if "disk" in placement.values():
            raise RuntimeError("The float32 fallback exceeds available GPU and CPU memory.")
        model = dispatch_model(model, device_map=placement)
    model.eval()
    device = model.get_input_embeddings().weight.device
    if device.type == "meta":
        device = torch.device("cuda:0")
    generate = torch_generator(model, tokenizer, torch, device)

    def checked_generate(batch, first):
        answers = generate(batch, first)
        if first:
            scratch = meta.with_suffix(".tmp")
            scratch.write_text(json.dumps({
                "base": base, "revision": revision, "precision": precision,
                "package_sha256": package_hash(root),
            }, indent=2) + "\n", encoding="utf-8")
            scratch.replace(meta)
        return answers

    collect(arm, path, pending, total, batch_size, checked_generate)


def package_hash(root):
    return hashlib.sha256((root / "manifest.json").read_bytes()).hexdigest()


def gpu_arm(root, out, arm, episodes, batch_size, tokenizer, base, revision):
    import torch

    path = out / f"{arm}.jsonl"
    meta = out / f"{arm}.meta.json"
    seen = valid_rows(path, arm, {ep["id"] for ep in episodes})
    precision = "float16"
    if seen:
        if not meta.is_file():
            raise ValueError(f"Restore {meta.name} alongside {path.name} to verify which model produced it")
        previous = read_json(meta)
        expected = {"base": base, "revision": revision, "package_sha256": package_hash(root)}
        if any(previous[k] != v for k, v in expected.items()):
            raise ValueError(f"Existing {path.name} uses a different base revision or package")
        precision = previous["precision"]

    pending = [ep for ep in episodes if ep["id"] not in seen]
    if not pending:
        print(f"{arm}: already complete ({len(seen)} replies).", flush=True)
        return
    retry_fp32 = False
    try:
        run_precision(root, out, arm, pending, len(episodes), batch_size if precision == "float16" else 1,
                      tokenizer, base, revision, precision, meta)
    except NonFiniteScores:
        if precision == "float32" or seen:
            raise
        retry_fp32 = True
    finally:
        gc.collect()
        torch.cuda.empty_cache()
    if retry_fp32:
        print(f"{arm}: non-finite fp16 scores; retrying this arm in float32 at batch 1.", flush=True)
        try:
            run_precision(root, out, arm, pending, len(episodes), 1, tokenizer, base, revision, "float32", meta)
        finally:
            gc.collect()
            torch.cuda.empty_cache()


def kaggle_eval(root, out, episodes, args):
    if not KAGGLE_WORKING.is_dir():
        raise SystemExit("Run GPU evaluation in a Kaggle notebook; use --dry-run for local checks.")
    if not args.skip_install:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                        "transformers==5.17.0", "peft==0.21.3", "accelerate>=1.10,<2"], check=True)
    import torch
    from transformers import AutoTokenizer

    if not torch.cuda.is_available():
        raise SystemExit("Enable a GPU accelerator in Notebook settings.")
    try:
        torch.zeros(1, device="cuda").add_(1).item()
    except RuntimeError as exc:
        raise RuntimeError("The installed PyTorch build could not run on this GPU. "
                           "See the P100 setup in the README or select T4.") from exc
    folder = root / "adapters" / "en"
    tokenizer = AutoTokenizer.from_pretrained(str(folder), padding_side="left", local_files_only=True)
    tokenizer.chat_template = (folder / "chat_template.jinja").read_text(encoding="utf-8")
    if tokenizer.pad_token_id is None or "enable_thinking" not in tokenizer.chat_template:
        raise ValueError("Expected the checkpoint pad token and a thinking toggle")
    base, revision = resolve_base(root, args.base, args.revision)
    print(f"Device: {torch.cuda.get_device_name(0)}; visible GPUs: {torch.cuda.device_count()}", flush=True)
    for arm in args.arms:
        gpu_arm(root, out, arm, episodes, args.batch_size, tokenizer, base, revision)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--arms", nargs="+", choices=tuple(ARMS), default=list(ARMS))
    parser.add_argument("--base", help="override the adapter's base repository for every arm")
    parser.add_argument("--revision", help="pin --base to a commit, such as for a resumed run")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-install", action="store_true")
    args = parser.parse_args()
    if args.revision and not args.base:
        parser.error("--revision requires --base")
    if args.batch_size < 1:
        parser.error("--batch-size must be positive")
    if args.dry_run and args.output is None:
        parser.error("--dry-run requires a separate --output directory")
    root = args.package
    episodes = [json.loads(line) for line in (root / "episodes.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()]
    ids = {row["id"] for row in episodes}
    manifest = read_json(root / "manifest.json")
    expected = manifest["episode_count"]
    if len(episodes) != expected or len(ids) != expected:
        raise ValueError(f"Expected {expected} unique episodes")
    if not args.dry_run and expected != 1152:
        raise ValueError("The GPU study needs all 1,152 episodes")
    out = args.output or KAGGLE_WORKING
    if args.dry_run:
        # Keep stub files in their own child directory so they cannot masquerade as GPU replies.
        out = out / "dry-run"
        out.mkdir(parents=True, exist_ok=True)
        for arm in args.arms:
            path = out / f"{arm}.jsonl"
            seen = valid_rows(path, arm, ids)
            pending = [ep for ep in episodes if ep["id"] not in seen]
            collect(arm, path, pending, len(episodes), args.batch_size,
                    lambda batch, first: [("offline stub", 2) for _ in batch])
        return
    if not KAGGLE_WORKING.is_dir():
        raise SystemExit("The base model is downloaded only on Kaggle.")
    for name, want in manifest["sha256"].items():
        with (root / name).open("rb") as source:
            if hashlib.file_digest(source, "sha256").hexdigest() != want:
                raise ValueError(f"Upload checksum mismatch: {name}")
    out.mkdir(parents=True, exist_ok=True)
    kaggle_eval(root, out, episodes, args)


if __name__ == "__main__":
    main()
