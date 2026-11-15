"""Build the upload package using only local files."""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from train_data import flatten

FILES = (
    "adapter_config.json", "adapter_model.safetensors", "config.json", "trainer_state.json",
    "tokenizer.json", "chat_template.jinja", "tokenizer_config.json", "special_tokens_map.json",
)
TOKENIZER_FILES = FILES[4:]
# Conservative size check, including the uncompressed dataset if the upload is expanded.
LIMIT = 100_000_000_000


def adapter_folder(path):
    direct = path / "adapter_config.json"
    configs = [direct] if direct.is_file() else sorted(path.rglob("adapter_config.json"))
    if len(configs) != 1:
        raise ValueError(f"Expected one adapter directory under {path}, found {len(configs)}")
    folder = configs[0].parent
    missing = [name for name in FILES if not (folder / name).is_file()]
    if missing:
        raise ValueError(f"{folder} is missing {', '.join(missing)}")
    return folder


def sha256(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def prepare(episodes, checkpoints, output, expected_count):
    rows = [json.loads(line) for line in episodes.read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = {r["id"] for r in rows}
    if len(rows) != expected_count or len(ids) != len(rows):
        raise ValueError(f"Expected {expected_count} different episode IDs, found {len(ids)} in {len(rows)} rows")
    folders = {arm: adapter_folder(checkpoints / arm) for arm in ("en", "multi")}
    for name in TOKENIZER_FILES:
        if sha256(folders["en"] / name) != sha256(folders["multi"] / name):
            raise ValueError(f"Checkpoint tokenizer assets disagree: {name}")

    output.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output) as tmp:
        staging = Path(tmp)
        package = staging / "package"
        package.mkdir()
        with (package / "episodes.jsonl").open("w", encoding="utf-8") as dest:
            for row in rows:
                entry = {"id": row["id"], "prompt": flatten(row["messages"])}
                dest.write(json.dumps(entry, ensure_ascii=False) + "\n")
        shutil.copyfile(Path(__file__).with_name("eval.py"), package / "eval.py")
        for arm, folder in folders.items():
            dest = package / "adapters" / arm
            dest.mkdir(parents=True)
            for name in FILES:
                shutil.copyfile(folder / name, dest / name)

        files = sorted(path for path in package.rglob("*") if path.is_file())
        size = sum(path.stat().st_size for path in files)
        if size >= LIMIT:
            raise ValueError(f"Uncompressed package is {size:,} bytes, above the {LIMIT:,}-byte limit")
        manifest = package / "manifest.json"
        manifest.write_text(json.dumps({
            "episode_count": expected_count,
            "sha256": {p.relative_to(package).as_posix(): sha256(p) for p in files},
        }, indent=2) + "\n", encoding="utf-8")
        archive = staging / "ft_eval_package.zip"
        with ZipFile(archive, "w", ZIP_DEFLATED, compresslevel=1) as dest:
            for path in [*files, manifest]:
                dest.write(path, path.relative_to(package))
        archive_size = archive.stat().st_size
        if archive_size >= LIMIT:
            raise ValueError(f"ZIP is {archive_size:,} bytes, above the {LIMIT:,}-byte limit")
        target = output / "package"
        if target.exists():
            shutil.rmtree(target)
        package.replace(target)
        archive.replace(output / archive.name)
    print(f"{expected_count:,} episodes; ZIP {archive_size / 2**20:.1f} MiB "
          f"({archive_size:,} bytes), below the conservative {LIMIT / 10**9:g} GB size check.")
    print(output / "ft_eval_package.zip")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=Path, default=ROOT / "data" / "episodes.jsonl")
    parser.add_argument("--checkpoints", type=Path, default=ROOT / "checkpoints")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--expected-count", type=int, default=1152)
    args = parser.parse_args()
    prepare(args.episodes, args.checkpoints, args.output, args.expected_count)


if __name__ == "__main__":
    main()
