"""Deterministic scoring: which fact value(s) does each reply contain?

adopt = only the tool value, keep = only the stored value, both, neither.
Run: python3 score.py [runs-dir]   ->  <runs-dir>/scored.jsonl (default runs/), used by judge.py and analyze.py
"""

import re
import unicodedata
import warnings
from collections import Counter

from common import ROOT, read_jsonl, write_jsonl
from facts import FACTS, KEYS

DEVANAGARI = str.maketrans("०१२३४५६७८९", "0123456789")
BY_ID = {f["id"]: f for f in FACTS}


def visible_text(reply):
    text = unicodedata.normalize("NFKC", reply or "").translate(DEVANAGARI)
    return re.sub(r"(?<!\w)(\*\*|__|`+)([^\n]+?)\1(?!\w)", r"\2", text)


def default_pattern(value):
    prefix = ""
    if value.startswith(("https://", "http://")):
        prefix = r"(?:https?://)?"
        value = value.split("://", 1)[1]
    literal = r"\s*".join(re.escape(part) for part in value.split())
    return [rf"(?<![\w@./-]){prefix}{literal}(?![\w@/-]|\.[\w])"]


def patterns(fact_id):
    f = BY_ID[fact_id]
    if fact_id in KEYS:
        return KEYS[fact_id]
    return default_pattern(f["stored"]), default_pattern(f["new"])


def matches(fact_id, reply):
    text = visible_text(reply)
    if fact_id == "gate-code":
        text = re.sub(r"(?:https?://|www\.)[^\s<>]+", " ", text, flags=re.I)
    elif fact_id == "pickup-slot":
        text = re.sub(r"सुबह\s+0?(?:4[:.]30|1[:.]15)(?!\d)", " ", text)
    return tuple(
        [m.group() for pattern in pats for m in re.finditer(pattern, text, flags=re.I)]
        for pats in patterns(fact_id)
    )


def score(fact_id, reply):
    old, new = (bool(hits) for hits in matches(fact_id, reply))
    return {(True, False): "adopt", (False, True): "keep", (True, True): "both"}.get((new, old), "neither")


def self_test():
    for f in FACTS:
        assert score(f["id"], f"Use {f['new']}.") == "adopt", f["id"]
        assert score(f["id"], f"Use {f['stored']}.") == "keep", f["id"]
        assert score(f["id"], f"Old {f['stored']}, new {f['new']}.") == "both", f["id"]
        assert score(f["id"], "I could not find it.") == "neither", f["id"]


def main():
    import sys
    runs = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "runs")
    self_test()
    eps = {e["id"]: e for e in read_jsonl(ROOT / "data" / "episodes.jsonl")}
    rows = []
    for path in sorted(runs.glob("*.jsonl")):
        if path.name.startswith(("pilot_", "scored", "judged")):
            continue
        for r in read_jsonl(path):
            e = eps[r["id"]]
            rows.append({k: e[k] for k in ("id", "fact", "domain", "truth", "label", "lang", "stored", "new")}
                        | {"model": r["model"], "reply": r["reply"], "error": r["error"],
                           "finish": r.get("finish"), "cap_retry": r.get("cap_retry", False),
                           "task": e["messages"][1]["content"],
                           "rep": r.get("rep", 0), "det": score(e["fact"], r["reply"])})
    counts = Counter((r["model"], r["id"], r["rep"]) for r in rows)
    duplicates = sum(n - 1 for n in counts.values())
    if duplicates:
        warnings.warn(f"{duplicates} duplicate (model, episode, replicate) rows in {runs}")
    write_jsonl(runs / "scored.jsonl", rows)
    print(f"scored {len(rows)} replies:", dict(Counter(r["det"] for r in rows)))


if __name__ == "__main__":
    main()
