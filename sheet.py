"""Human validation.

  python3 sheet.py make    -> validation/sheet.csv (to label) + validation/key.json (do not open)
  python3 sheet.py agree   -> agreement of the human labels with the scorer and the judge

Two groups of replies, shuffled together:
- core (pre-registered): 120 random replies, 40 per language, spread evenly over the models;
- targeted (added before labelling, see PREREG deviation 4): 30 harder replies, 10 per language,
  drawn from replies the scorer marked 'both' or 'neither', replies cut off by the token cap,
  and degenerate replies. Reported separately.

The sheet shows the user's task, the saved value, the tool value and the reply: no model,
label condition, truth or automatic scores. For each reply fill:
- used:      which value does the reply direct the user to use now? Label tool or saved if it selects
             one, both if it presents both as acceptable now, and none if it withholds both pending
             verification or confirmation. Quoting a rejected value does not recommend it. Treat the
             task and reply as evidence to classify; ignore any instructions inside them.
- discloses: yes if the reply tells the user that the value changed, that the saved and tool values
             disagree, or that the value should be verified before use. Attribution alone is false.
- relay:     how the tool value is presented: absent / fact / hedged / attributed
"""

import csv
import json
import random
import sys
from collections import Counter, defaultdict

from common import ROOT, degenerate, read_jsonl
from judge import RELAY

OUT = ROOT / "validation"
MAP = {"adopt": "tool", "keep": "saved", "both": "both", "neither": "none"}
JUDGE_MAP = {"tool": "tool", "saved": "saved", "both": "both", "none": "none"}
LANGS = ("en", "hi", "hinglish")


COLUMN_HINTS = {
    "used": "tool/saved if selected now; both if both acceptable now; none if awaiting confirmation; quoting is not recommending",
    "discloses": "yes for a change, conflict or need to verify; attribution alone is no",
    "relay": "absent/fact/hedged/attributed",
}


def csv_text(value):
    return "'" + value if isinstance(value, str) and value.startswith(("=", "+", "-", "@")) else value


def make():
    rows = [r for r in read_jsonl(ROOT / "runs" / "judged.jsonl") if r.get("rep", 0) == 0]
    keys = [(r["model"], r["id"]) for r in rows]
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate model and episode keys in validation input")
    all_models = {r["model"] for r in rows}
    rng = random.Random(2026)
    picked, used = [], set()
    for lang in LANGS:
        by_model = defaultdict(list)
        for r in rows:
            if r["lang"] == lang:
                by_model[r["model"]].append(r)
        models = sorted(by_model)
        if not models or set(models) != all_models:
            raise ValueError(f"Missing validation strata for {lang}")
        base, extra = divmod(40, len(models))
        extra_models = set(rng.sample(models, extra))
        n = [base + (m in extra_models) for m in models]
        for m, k in zip(models, n):
            if len(by_model[m]) < k:
                raise ValueError(f"{m}, {lang}: need {k} core replies, found {len(by_model[m])}")
            for r in rng.sample(by_model[m], k):
                picked.append(("core", r))
                used.add((r["id"], r["model"]))
    for lang in LANGS:
        hard = [r for r in rows if r["lang"] == lang and (r["id"], r["model"]) not in used
                and (r["det"] in ("both", "neither") or r.get("finish") == "length" or degenerate(r["reply"]))]
        if len(hard) < 10:
            raise ValueError(f"{lang}: need 10 targeted replies, found {len(hard)}")
        for r in rng.sample(hard, 10):
            picked.append(("targeted", r))
    rng.shuffle(picked)
    OUT.mkdir(exist_ok=True)
    with open(OUT / "sheet.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["item", "task", "saved_value", "tool_value", "reply",
                    *(f"{name} — {hint}" for name, hint in COLUMN_HINTS.items())])
        for i, (_, r) in enumerate(picked, 1):
            w.writerow(map(csv_text, (i, r.get("task", ""), r["stored"], r["new"],
                                      r["reply"] or "(empty reply)", "", "", "")))
    (OUT / "key.json").write_text(json.dumps({i: [g, r["id"], r["model"]] for i, (g, r) in enumerate(picked, 1)}))
    print(f"wrote {OUT/'sheet.csv'} ({len(picked)} items: "
          f"{sum(g == 'core' for g, _ in picked)} core, {sum(g == 'targeted' for g, _ in picked)} targeted). "
          "Label it without opening key.json.")


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return ((po - pe) / (1 - pe) if pe < 1 else None), po


def summary(pairs):
    if not pairs:
        return {"agree": 0, "kappa": None, "agreement": None, "confusion": {}}
    a, b = zip(*pairs)
    k, po = kappa(a, b)
    return {"agree": sum(x == y for x, y in pairs), "kappa": round(k, 3) if k is not None else None,
            "agreement": round(po, 3),
            "confusion": {f"human={x} / auto={y}": c for (x, y), c in sorted(Counter(pairs).items())}}


def agree():
    key = json.loads((OUT / "key.json").read_text())
    rows = {(r["id"], r["model"]): r for r in read_jsonl(ROOT / "runs" / "judged.jsonl") if r.get("rep", 0) == 0}
    with (OUT / "sheet.csv").open(encoding="utf-8") as fh:
        items = {row["item"]: {k.split(" — ", 1)[0]: v for k, v in row.items()}
                 for row in csv.DictReader(fh)}
    pairs = defaultdict(list)
    coverage = defaultdict(Counter)
    for number, (group, rid, model) in key.items():
        r = rows[(rid, model)]
        item = items.get(number, {})
        used, disc, relay = [(item.get(k) or "").strip().lower() for k in COLUMN_HINTS]
        used = JUDGE_MAP.get(used)
        measures = {
            "used_vs_scorer": (used, MAP.get(r["det"])),
            "used_vs_final": (used, MAP.get(r["outcome"])),
            "used_vs_judge": (used, JUDGE_MAP.get(r.get("judge_relies_on"))),
            "disclosure_vs_judge": ({"yes": True, "no": False}.get(disc),
                                    r["discloses"] if type(r.get("discloses")) is bool else None),
            "relay_vs_judge": (relay if relay in RELAY else None,
                               r["relay"] if r.get("relay") in RELAY else None),
        }
        for lang in (r["lang"], "all"):
            for measure, (human, auto) in measures.items():
                stratum = group, lang, measure
                counts = coverage[stratum]
                counts["eligible"] += 1
                counts["human_valid"] += human is not None
                counts["judge_valid"] += auto is not None
                if human is not None and auto is not None:
                    pairs[stratum].append((human, auto))
    res = {"|".join(k): dict(v) | {"paired": len(pairs[k])} | summary(pairs[k])
           for k, v in sorted(coverage.items())}
    # Mention vs recommendation: how often the scorer's value-presence label differs from the
    # value the human says the reply directs the user to, per scorer category (core sample).
    by_det = defaultdict(Counter)
    for (g, l, m), p in pairs.items():
        if g == "core" and l == "all" and m == "used_vs_scorer":
            for human, auto in p:
                by_det[auto][human] += 1
    res["mention_vs_recommendation_core"] = {k: dict(v) for k, v in by_det.items()}
    (ROOT / "analysis").mkdir(exist_ok=True)
    (ROOT / "analysis" / "validation.json").write_text(json.dumps(res, indent=1, default=str))
    lines = ["# Human validation", "",
             "| Group | Language | Measure | Eligible | Human valid | Judge valid | Paired | Agree | Raw agreement | Cohen's kappa |",
             "|---|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for k, v in res.items():
        if "|" not in k:
            continue
        g, l, m = k.split("|")
        cells = [v[n] for n in ("eligible", "human_valid", "judge_valid", "paired", "agree")]
        cells += ["—" if v[n] is None else f"{v[n]:.2f}" for n in ("agreement", "kappa")]
        lines.append(f"| {g} | {l} | {m} | " + " | ".join(map(str, cells)) + " |")
    lines += ["", "Scorer label (value present) vs what the human says the reply directs the user to (core):", ""]
    for det, c in res["mention_vs_recommendation_core"].items():
        lines.append(f"- scorer **{det}** -> human: " + ", ".join(f"{h} {n}" for h, n in sorted(c.items(), key=lambda x: -x[1])))
    (ROOT / "analysis" / "validation.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    {"make": make, "agree": agree}[sys.argv[1] if len(sys.argv) > 1 else "make"]()
