"""Input checks shared by the two analysis reports."""

import argparse
from collections import Counter

from common import ROOT, read_jsonl
from ft_eval.eval import ARMS as FINETUNE_ARMS
from judge import judged_row_valid
from run import MODELS


def row_key(row):
    return row["model"], row["id"], row.get("rep", 0)


def load_analysis(description, rep0_only=False):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("name", nargs="?", default="runs")
    parser.add_argument("--partial", action="store_true")
    args = parser.parse_args()

    source = ROOT / args.name
    resolved = source.resolve()
    confirmatory = resolved == (ROOT / "runs").resolve()
    finetune = resolved == (ROOT / "runs" / "finetune").resolve()
    rows = read_jsonl(source / "judged.jsonl")
    counts = Counter(map(row_key, rows))
    invalid = sum(not judged_row_valid(r) for r in rows)
    episodes = read_jsonl(ROOT / "data" / "episodes.jsonl")
    planned = FINETUNE_ARMS if finetune else MODELS
    expected = Counter((m, e["id"], 0) for m in planned for e in episodes)
    missing = sum((expected - counts).values())
    extra = sum((counts - expected).values())
    duplicate = sum(n - 1 for n in counts.values())
    if not args.partial:
        if confirmatory and counts != expected:
            parser.error(f"confirmatory roster mismatch: {missing} missing, {duplicate} duplicate, "
                         f"{extra} extra rows including duplicates")
        if invalid:
            parser.error(f"{invalid} unresolved judge verdicts; resolve them before analysis")
        if any(r["id"].startswith("pilot:") for r in rows):
            parser.error("pilot replies are outside the study")
    else:
        rows_used = [r for r in rows if judged_row_valid(r) and counts[row_key(r)] == 1
                     and not r["id"].startswith("pilot:")
                     and (not (confirmatory or finetune) or row_key(r) in expected)
                     and (not rep0_only or r.get("rep", 0) == 0)]
        observed_models = sorted({r["model"] for r in rows})
        planned_models = list(planned)
        summary = {
            "planned_models": planned_models, "planned_rows": sum(expected.values()),
            "observed_models": observed_models, "observed_rows": len(rows),
            "analysed_rows": len(rows_used),
            "missing": missing, "duplicate": duplicate, "extra_including_duplicates": extra,
            "unresolved_verdicts": invalid,
        }
        plan = "exploratory fine-tune plan" if finetune else "confirmatory plan"
        header = (f"Partial snapshot | {plan}: {summary['planned_rows']:,} rows "
                  f"({', '.join(planned_models)})\n"
                  f"Observed {len(rows):,} rows ({', '.join(observed_models) or 'none'}); "
                  f"analysed {len(rows_used):,}, {invalid} unresolved, {duplicate} duplicate rows.")
        print(header)
        out = ROOT / "analysis" / "partial"
        return rows_used, out / "finetune" if finetune else out, summary, header

    suffix = "" if confirmatory else args.name.removeprefix("runs/").replace("/", "_")
    # Reserve the partial snapshot directory even if an exploratory input is named that way.
    if suffix == "partial":
        suffix = "exploratory_partial"
    if rep0_only:
        rows = [r for r in rows if r.get("rep", 0) == 0]
    return rows, ROOT / "analysis" / suffix, {}, ""
