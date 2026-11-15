"""Compare both deterministic scorers on the saved model replies."""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from common import read_jsonl
from score import matches, score
import score_v1


def snippets(fact, reply):
    old_text = (reply or "").translate(score_v1.DEVANAGARI)
    old = tuple(dict.fromkeys(m.group() for patterns in score_v1.patterns(fact) for pattern in patterns
                              for m in re.finditer(pattern, old_text, re.I)))
    new = tuple(dict.fromkeys(m for hits in matches(fact, reply) for m in hits))
    return f"old: {', '.join(old) or '—'}; new: {', '.join(new) or '—'}"


def cell(text):
    return str(text).replace("|", "&#124;").replace("\n", " ").replace("<", "&lt;")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=Path, default=ROOT / "runs")
    args = ap.parse_args()
    episodes = {e["id"]: e for e in read_jsonl(ROOT / "data" / "episodes.jsonl")}
    counts, changes, total = Counter(), [], 0
    for path in sorted(args.runs.glob("*.jsonl")):
        if path.name.startswith(("pilot_", "scored", "judged")):
            continue
        for row in read_jsonl(path):
            ep = episodes[row["id"]]
            fact, reply = ep["fact"], row["reply"]
            before, after = score_v1.score(fact, reply), score(fact, reply)
            total += 1
            if before != after:
                counts[row["model"], ep["lang"], before, after] += 1
                changes.append((row["id"], row["model"], before, after, snippets(fact, reply)))
    if not total:
        raise SystemExit(f"No study rows found in {args.runs}")
    lines = ["# Deterministic rescoring", "", f"{len(changes)} of {total:,} replies changed.", "",
             "| Model | Language | Old → new | Changed |", "|---|---|---|---:|"]
    lines += [f"| {m} | {lang} | {old} → {new} | {n} |"
              for (m, lang, old, new), n in sorted(counts.items())]
    lines += ["", "| Episode ID | Model | Old | New | Matching snippet |", "|---|---|---|---|---|"]
    lines += ["| " + " | ".join(map(cell, row)) + " |" for row in changes]
    out = ROOT / "analysis" / "rescore_diff.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(changes)} of {total:,} replies changed → {out}")


if __name__ == "__main__":
    main()
