"""Deterministic scoring: which fact value(s) does each reply contain?

adopt = only the tool value, keep = only the stored value, both, neither.
Run: python3 score.py [runs-dir]   ->  <runs-dir>/scored.jsonl (default runs/), used by judge.py and analyze.py
"""

import re

from common import ROOT, read_jsonl, write_jsonl
from facts import FACTS, KEYS

DEVANAGARI = str.maketrans("०१२३४५६७८९", "0123456789")
BY_ID = {f["id"]: f for f in FACTS}


def default_pattern(value):
    # The value itself, case-insensitive, tolerant of spacing around separators.
    parts = [re.escape(p) for p in re.split(r"\s+", value.strip())]
    pat = r"\s*".join(parts)
    return [rf"(?<![\w]){pat}(?![\w])" if value[-1].isalnum() else pat]


def patterns(fact_id):
    f = BY_ID[fact_id]
    if fact_id in KEYS:
        return KEYS[fact_id]
    return default_pattern(f["stored"]), default_pattern(f["new"])


def found(pats, text):
    return any(re.search(p, text, flags=re.I) for p in pats)


def score(fact_id, reply):
    text = (reply or "").translate(DEVANAGARI)
    old_p, new_p = patterns(fact_id)
    old, new = found(old_p, text), found(new_p, text)
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
                           "rep": r.get("rep", 0), "det": score(e["fact"], r["reply"])})
    write_jsonl(runs / "scored.jsonl", rows)
    from collections import Counter
    print(f"scored {len(rows)} replies:", dict(Counter(r["det"] for r in rows)))


if __name__ == "__main__":
    main()
