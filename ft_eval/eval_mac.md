# Apple Silicon fallback

An unquantized 4B model is practical on an Apple Silicon Mac with about **24 GB or more of unified memory**. On 16 GB, a single-model test may work with other applications closed, but three full arms can be slow or hit memory pressure. If the exact base weights are unavailable locally, this fallback is unavailable until a Kaggle-downloaded copy can be transferred. Use a local snapshot of the same base revision for all three arms. A quantized substitute changes the evaluation.

1. Install `mlx-lm` in a Python environment. From the repository root, run `python3 ft_eval/prepare.py` if the package is missing.
2. Verify that the local snapshot contains its tokenizer and configuration files and all base weight shards. Use a path on disk as `LOCAL_BASE`. The code below loads that snapshot and uses the checkpoint tokenizer and template for the prompts.
3. From the repo root, run the following block in Terminal. The remap converts the downloaded PEFT tensors to the MLX language-backbone paths, transposes both matrices, and verifies complete adapter coverage and shapes before inference.

```sh
export LOCAL_BASE=/absolute/path/to/local/Qwen3.5-4B
export MLX_OUTPUT=/absolute/path/to/a/new-output-directory
python3 - <<'PY'
import gc
import json
import os
import re
from pathlib import Path

import mlx.core as mx
from mlx.utils import tree_flatten
from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_sampler
from mlx_lm.tuner.utils import linear_to_lora_layers
from transformers import AutoTokenizer

from ft_eval.eval import ARMS, CAP, collect, render_prompt, valid_rows

base = Path(os.environ["LOCAL_BASE"]).resolve()
out = Path(os.environ["MLX_OUTPUT"])
package = Path("ft_eval/package")
out.mkdir(parents=True, exist_ok=True)
if not (base / "config.json").is_file() or not list(base.glob("*.safetensors")):
    raise SystemExit("LOCAL_BASE must be a complete local base snapshot")

episodes = [json.loads(line) for line in (package / "episodes.jsonl").read_text().splitlines()]
assert len(episodes) == 1152
ids = {row["id"] for row in episodes}
folder = package / "adapters/en"
tokenizer = AutoTokenizer.from_pretrained(folder, local_files_only=True)
tokenizer.chat_template = (folder / "chat_template.jinja").read_text()
sampler = make_sampler(temp=0)


def attach(model, folder):
    config = json.loads((folder / "adapter_config.json").read_text())
    assert not (config.get("use_rslora") or config.get("use_dora") or
                config.get("rank_pattern") or config.get("alpha_pattern"))
    weights = mx.load(str(folder / "adapter_model.safetensors"))
    keys, converted = set(), {}
    for name, tensor in weights.items():
        match = re.fullmatch(
            r"base_model\.model\.model\.language_model\.layers\.(\d+)\.(.+)\.lora_([AB])\.weight", name
        )
        if not match:
            raise ValueError(f"Unexpected PEFT tensor: {name}")
        layer, target, side = match.groups()
        keys.add(target)
        converted[f"language_model.model.layers.{layer}.{target}.lora_{side.lower()}"] = tensor.T

    linear_to_lora_layers(model, len(model.layers), {
        "keys": sorted(keys), "rank": config["r"], "scale": config["lora_alpha"] / config["r"], "dropout": 0,
    })
    slots = {name: tensor for name, tensor in tree_flatten(model.parameters())
             if name.endswith((".lora_a", ".lora_b"))}
    if slots.keys() != converted.keys() or any(slots[k].shape != w.shape for k, w in converted.items()):
        raise ValueError("The MLX adapter names or shapes do not match the model")
    model.load_weights(list(converted.items()), strict=False)


for arm, adapter in ARMS.items():
    path = out / f"{arm}.jsonl"
    seen = valid_rows(path, arm, ids)
    pending = [row for row in episodes if row["id"] not in seen]
    if not pending:
        continue
    model, base_tokenizer = load(str(base))
    if adapter:
        attach(model, package / "adapters" / adapter)
    model.eval()

    def generate(batch, first):
        ids = tokenizer.encode(render_prompt(tokenizer, batch[0]["prompt"]), add_special_tokens=False)
        pieces = []
        last = None
        for step in stream_generate(model, base_tokenizer, ids, max_tokens=CAP, sampler=sampler):
            pieces.append(step.text)
            last = step
        if last is None:
            raise RuntimeError("Generation returned no completion status")
        return [("".join(pieces).strip(), last.generation_tokens)]

    collect(arm, path, pending, len(episodes), 1, generate)
    del model, base_tokenizer
    gc.collect()
    mx.clear_cache()
PY
```

Use a new output directory when switching base revision or runtime. If you choose the Mac fallback, generate **all three** arms there and label the run as MLX in the report. Move the resulting JSONLs into `runs/finetune/` and follow the analysis commands in the README. The fallback uses the same rendered prompts and decoding cap, and its runtime and numerics can differ from the Kaggle run.

[MLX LM generation and memory notes](https://github.com/ml-explore/mlx-lm) · [MLX Qwen3.5 weight mapping](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/models/qwen3_5.py) · [MLX adapter loader](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/tuner/utils.py)
