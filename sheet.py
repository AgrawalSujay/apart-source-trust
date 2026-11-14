"""Human validation (120 blind items).

  python3 sheet.py make    -> validation/sheet.csv (to label) + validation/key.json (do not open)
  python3 sheet.py agree   -> Cohen's kappa of the human labels vs the scorer and the judge

The sheet shows only the reply, the saved value and the tool value: no model, label
condition, truth or scores. Fill 'used' with tool / saved / both / none,
'discloses' with yes / no, and 'relay' (how the tool value is presented) with
absent / fact / hedged / attributed.
"""

import csv
import json
import random
import sys
from collections import Counter, defaultdict

from common import ROOT, read_jsonl

OUT = ROOT / "validation"
MAP = {"adopt": "tool", "keep": "saved", "both": "both", "neither": "none"}


def make():
    rows = read_jsonl(ROOT / "runs" / "judged.jsonl")
    cells = defaultdict(list)
    for r in rows:
        cells[(r["model"], r["lang"])].append(r)
    rng = random.Random(2026)
    keys = sorted(cells)
    per = [120 // len(keys) + (1 if i < 120 % len(keys) else 0) for i in range(len(keys))]
    picked = [x for k, n in zip(keys, per) for x in rng.sample(cells[k], n)]
    rng.shuffle(picked)
    OUT.mkdir(exist_ok=True)
    with open(OUT / "sheet.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["item", "saved_value", "tool_value", "reply", "used", "discloses", "relay"])
        for i, r in enumerate(picked, 1):
            w.writerow([i, r["stored"], r["new"], r["reply"], "", "", ""])
    (OUT / "key.json").write_text(json.dumps({i: [r["id"], r["model"]] for i, r in enumerate(picked, 1)}))
    print(f"wrote {OUT/'sheet.csv'} (120 items). Label it without opening key.json.")


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, po


def agree():
    key = json.loads((OUT / "key.json").read_text())
    rows = {(r["id"], r["model"]): r for r in read_jsonl(ROOT / "runs" / "judged.jsonl")}
    human_used, det_used, fin_used, human_disc, judge_disc, human_relay, judge_relay = [], [], [], [], [], [], []
    for item in csv.DictReader(open(OUT / "sheet.csv", encoding="utf-8")):
        used, disc = item["used"].strip().lower(), item["discloses"].strip().lower()
        if not used:
            continue
        r = rows[tuple(key[item["item"]])]
        human_used.append(used)
        det_used.append(MAP[r["det"]])
        fin_used.append(MAP[r["outcome"]])
        relay = item.get("relay", "").strip().lower()
        if relay in ("absent", "fact", "hedged", "attributed") and r.get("relay"):
            human_relay.append(relay)
            judge_relay.append(r["relay"])
        if disc in ("yes", "no") and r["discloses"] is not None:
            human_disc.append(disc == "yes")
            judge_disc.append(r["discloses"])
    res = {"n_labelled": len(human_used)}
    for name, (a, b) in {"used_vs_scorer": (human_used, det_used), "used_vs_final": (human_used, fin_used),
                         "disclosure_vs_judge": (human_disc, judge_disc),
                         "relay_vs_judge": (human_relay, judge_relay)}.items():
        if a:
            k, po = kappa(a, b)
            res[name] = {"kappa": round(k, 3), "agreement": round(po, 3), "n": len(a)}
    (ROOT / "analysis").mkdir(exist_ok=True)
    (ROOT / "analysis" / "validation.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    {"make": make, "agree": agree}[sys.argv[1] if len(sys.argv) > 1 else "make"]()
