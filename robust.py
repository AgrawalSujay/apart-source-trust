"""Robustness and effect sizes (added before analysis, see PREREG deviation 4). Does not replace analyze.py,
which runs the pre-registered tests; this reports, next to them:

1. generation failures by model x language (empty/failed, cut off by the cap, degenerate, usable);
2. effect sizes for H1-H7 with 95% intervals from a bootstrap that resamples whole facts
   (all models, languages and conditions of a fact move together), for two outcome definitions:
   'pre-registered outcome' = the scorer with judge resolution of both and 'recommend' = the value the judge says the
   reply directs the user to use;
3. H2 split into its two parts: change in real updates followed, change in planted claims accepted;
4. the same effects on usable replies only (whole model x fact units dropped if any reply
   in them is unusable);
5. the main figure: real updates followed, planted values recommended, silent wrong recommendations,
   by label condition, pooled with fact-level intervals and one dot per model;
6. one matched pair of real replies for the paper.

  python3 robust.py [runs-dir]     (default runs)
"""

import json
import random
import re
from collections import defaultdict
from itertools import product

import numpy as np

from analysis_input import load_analysis
from common import degenerate, usable

LABELS = ("none", "informative", "placebo", "forged")
TRUTHS = ("real", "planted")
LANGS = ("en", "hi", "hinglish")
# Per-row indicators summed into cells.
IND = ("n", "adopt", "rec", "disc", "silent", "silent_rec", "defer", "adopt_disc", "rec_disc")


def indicators(r):
    adopt = r["outcome"] == "adopt"
    rec = r.get("judge_relies_on") == "tool"
    disc = bool(r.get("discloses"))
    planted = r["truth"] == "planted"
    return {"n": 1, "adopt": adopt, "rec": rec, "disc": disc,
            "silent": planted and adopt and not disc, "silent_rec": planted and rec and not disc,
            "defer": r.get("judge_relies_on") in ("both", "none"),
            "adopt_disc": adopt and disc, "rec_disc": rec and disc}


def cube(rows, facts):
    """facts x label x truth x lang x indicator, summed over models."""
    fi = {f: i for i, f in enumerate(facts)}
    a = np.zeros((len(facts), 4, 2, 3, len(IND)))
    for r in rows:
        ind = indicators(r)
        a[fi[r["fact"]], LABELS.index(r["label"]), TRUTHS.index(r["truth"]), LANGS.index(r["lang"])] += [ind[k] for k in IND]
    return a


def K(name):
    return IND.index(name)


def rate(c, num, label=None, truth=None, lang=None, den="n"):
    """Ratio of summed indicators over the selected cells of a facts-summed cube (label x truth x lang x ind)."""
    sel = c
    sel = sel[LABELS.index(label)] if label else sel.sum(0)
    sel = sel[TRUTHS.index(truth)] if truth else sel.sum(0)
    sel = sel[LANGS.index(lang)] if lang else sel.sum(0)
    return sel[K(num)] / sel[K(den)] if sel[K(den)] else np.nan


def effects(c, mode):
    """All effect sizes from one facts-summed cube; mode 'pre-registered outcome' or 'recommend'."""
    a, s, ad = ("adopt", "silent", "adopt_disc") if mode == "pre-registered outcome" else ("rec", "silent_rec", "rec_disc")
    real = lambda lb: rate(c, a, lb, "real")
    pl = lambda lb, lg=None: rate(c, a, lb, "planted", lg)
    e = {
        "H1 tool value used, no labels": rate(c, a, "none"),
        "H2 discrimination gain (informative - none)": (real("informative") - pl("informative")) - (real("none") - pl("none")),
        "H2a real updates followed: informative - none": real("informative") - real("none"),
        "H2b planted accepted: informative - none": pl("informative") - pl("none"),
        "H3 planted accepted: forged - informative": pl("forged") - pl("informative"),
        "H4 planted accepted: placebo - none": pl("placebo") - pl("none"),
        "H5 planted accepted (informative): hi - en": pl("informative", "hi") - pl("informative", "en"),
        "H5 planted accepted (informative): hinglish - en": pl("informative", "hinglish") - pl("informative", "en"),
        "H6 disclosure among replies using the tool value": rate(c, ad, den=a),
        "H7 disclosure (none): en - hi": rate(c, "disc", "none", lang="en") - rate(c, "disc", "none", lang="hi"),
        "H7 disclosure (none): en - hinglish": rate(c, "disc", "none", lang="en") - rate(c, "disc", "none", lang="hinglish"),
        "Silent wrong (all planted), none": rate(c, s, "none", "planted"),
        "Silent wrong (all planted), informative": rate(c, s, "informative", "planted"),
        "Silent wrong (all planted), placebo": rate(c, s, "placebo", "planted"),
        "Silent wrong (all planted), forged": rate(c, s, "forged", "planted"),
    }
    return e


def finite(value):
    return float(value) if np.isfinite(value) else None


def interval(point, draws):
    values = [v for v in draws if np.isfinite(v)]
    if not values:
        return finite(point), None, None, 0
    lo, hi = np.percentile(values, [2.5, 97.5])
    return finite(point), float(lo), float(hi), len(values)


def fact_draws(cubef, reps, seed):
    rng = np.random.default_rng(seed)
    nf = len(cubef)
    for _ in range(reps if nf else 0):
        yield cubef[rng.integers(0, nf, nf)].sum(0)


def boot(cubef, mode, reps=2000, seed=0):
    point = effects(cubef.sum(0), mode)
    draws = defaultdict(list)
    for draw in fact_draws(cubef, reps, seed):
        for k, v in effects(draw, mode).items():
            draws[k].append(v)
    return {k: interval(v, draws[k]) for k, v in point.items()}


def usable_blocks(rows):
    expected = set(product(TRUTHS, LABELS, LANGS))
    units = defaultdict(list)
    for row in rows:
        units[row["model"], row["fact"]].append(row)
    return [r for unit in units.values()
            if len(unit) == len(expected)
            and {(r["truth"], r["label"], r["lang"]) for r in unit} == expected
            and all(map(usable, unit))
            for r in unit]


def cache_twins(rows, models):
    idx = {(r["model"], r["fact"], r["label"], r["lang"], r["truth"]): r for r in rows}
    counts = {m: {lb: {"identical": 0, "different": 0} for lb in ("none", "placebo")} for m in models}
    for (model, fact, label, lang, truth), row in idx.items():
        if truth == "real" and label in counts[model]:
            twin = idx.get((model, fact, label, lang, "planted"))
            if twin is not None:
                category = "identical" if row["reply"] == twin["reply"] else "different"
                counts[model][label][category] += 1
    return counts


def pct(x):
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{100 * x:.1f}"


def main():
    rows, out, snapshot, header = load_analysis(__doc__, rep0_only=True)
    out.mkdir(parents=True, exist_ok=True)
    models = sorted({r["model"] for r in rows})
    facts = sorted({r["fact"] for r in rows})
    md = [header, ""] if header else []
    md += ["# Robustness and effect sizes", "",
           f"{len(rows)} replies, {len(models)} models, {len(facts)} facts. Intervals: 95%, bootstrap over whole facts (2,000 draws).", ""]

    # 1. Generation failures.
    md += ["## Generation failures", "", "| Model | Lang | n | Empty or failed | Cut off by cap | Cap retry | Degenerate | Usable | Asked for another lookup |",
           "|---|---|---|---|---|---|---|---|---|"]
    fail = {}
    for m in models:
        for lg in LANGS:
            sub = [r for r in rows if r["model"] == m and r["lang"] == lg]
            row = {"n": len(sub), "empty": sum(not r["reply"] or bool(r.get("error")) for r in sub),
                   "capped": sum(r.get("finish") == "length" for r in sub),
                   "cap_retry": sum(bool(r.get("cap_retry")) for r in sub),
                   "degenerate": sum(degenerate(r["reply"]) for r in sub), "usable": sum(usable(r) for r in sub),
                   "asked_for_another_lookup": sum(bool(re.search(r"(?m)^\s*CALL\s+lookup_", r["reply"] or "")) for r in sub)}
            fail[f"{m}|{lg}"] = row
            md.append(f"| {m} | {lg} | " + " | ".join(map(str, row.values())) + " |")
    totals = {key: sum(row[key] for row in fail.values())
              for key in ("n", "empty", "capped", "cap_retry", "degenerate", "usable", "asked_for_another_lookup")}
    md.append("| All models | All | " + " | ".join(map(str, totals.values())) + " |")

    twins = cache_twins(rows, models)
    md += ["", "## Identical-input real/planted twin replies", "",
           "| Model | Label | Identical | Different |", "|---|---|---:|---:|"]
    for m in models:
        for lb, counts in twins[m].items():
            md.append(f"| {m} | {lb} | {counts['identical']} | {counts['different']} |")
    md += ["", "Matching reply text does not establish cache reuse."]

    usable_rows = usable_blocks(rows)
    res = {"partial_snapshot": snapshot} if snapshot else {}
    res.update({"failures": fail, "failure_totals": totals, "identical_input_twins": twins,
                "n_usable_units_rows": len(usable_rows)})
    for tag, rs in (("all", rows), ("usable", usable_rows)):
        c = cube(rs, facts)
        for mode in ("pre-registered outcome", "recommend"):
            res[f"{tag}|{mode}"] = boot(c, mode)
    keys = list(res["all|pre-registered outcome"])
    md += ["", "## Effect sizes (percentage points; rates for H1, H6 and silent wrong)", "",
           f"Usable-only keeps {len(usable_rows)} of {len(rows)} replies.", "",
           "| Effect | Pre-registered outcome, all | Recommend, all | Pre-registered outcome, usable | Recommend, usable |", "|---|---|---|---|---|"]
    for k in keys:
        cells = []
        for col in ("all|pre-registered outcome", "all|recommend", "usable|pre-registered outcome", "usable|recommend"):
            p, lo, hi, n = res[col][k]
            cells.append(f"{pct(p)} [{pct(lo)}, {pct(hi)}] ({n:,} finite)")
        md.append(f"| {k} | " + " | ".join(cells) + " |")

    # Per-model recommendation rates (for the figure and the appendix).
    per_model = {}
    for m in models:
        cm = cube([r for r in rows if r["model"] == m], facts).sum(0)
        per_model[m] = {lb: {"real_followed": finite(rate(cm, "rec", lb, "real")),
                             "planted_recommended": finite(rate(cm, "rec", lb, "planted")),
                             "silent_wrong": finite(rate(cm, "silent_rec", lb, "planted")),
                             "defer": finite(rate(cm, "defer", lb))} for lb in LABELS}
    res["per_model_recommend"] = per_model
    md += ["", "## Per model (recommend): real followed / planted recommended / silent wrong", "",
           "| Model | " + " | ".join(LABELS) + " |", "|---|" + "---|" * len(LABELS)]
    for m in models:
        md.append(f"| {m} | " + " | ".join(
            f"{pct(per_model[m][lb]['real_followed'])} / {pct(per_model[m][lb]['planted_recommended'])} / {pct(per_model[m][lb]['silent_wrong'])}"
            for lb in LABELS) + " |")

    # 5. Main figure.
    call = cube(rows, facts)
    panel_def = [("Real updates followed", "rec", "real"), ("Planted values recommended", "rec", "planted"),
                 ("Silent wrong recommendations", "silent_rec", "planted")]
    fig_data = {}
    draws = list(fact_draws(call, 2000, seed=1))
    for title, num, truth in panel_def:
        fig_data[title] = {}
        for lb in LABELS:
            p = rate(call.sum(0), num, lb, truth)
            ds = [rate(d, num, lb, truth) for d in draws]
            fig_data[title][lb] = interval(p, ds)
    res["figure"] = fig_data
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.4), sharey=True)
        keymap = {"Real updates followed": "real_followed", "Planted values recommended": "planted_recommended",
                  "Silent wrong recommendations": "silent_wrong"}
        for ax, (title, _, _) in zip(axes, panel_def):
            for i, lb in enumerate(LABELS):
                p, lo, hi, _ = fig_data[title][lb]
                for j, m in enumerate(models):
                    v = per_model[m][lb][keymap[title]]
                    if v is not None:
                        ax.scatter(i + (j - (len(models) - 1) / 2) * 0.05, 100 * v,
                                   s=10, color="#9a9a9a", zorder=1)
                if lo is not None and hi is not None:
                    ax.vlines(i, 100 * lo, 100 * hi, color="#2a6fb0", lw=1.5, zorder=2)
                if p is not None:
                    ax.scatter(i, 100 * p, color="#2a6fb0", s=32, zorder=3)
            ax.set_xticks(range(4), LABELS, fontsize=9)
            ax.set_title(title, fontsize=10)
            ax.set_ylim(0, 100)
            ax.grid(axis="y", alpha=0.25)
            ax.spines[["top", "right"]].set_visible(False)
        axes[0].set_ylabel("% of episodes")
        fig.text(0.01, -0.02, "Blue: all models pooled, 95% interval resampling facts. Grey: one dot per model.", fontsize=8)
        if header:
            fig.suptitle(header, fontsize=8, wrap=True)
        fig.tight_layout()
        fig.savefig(out / "fig_main.png", dpi=220, bbox_inches="tight")
        md += ["", f"Figure: {out / 'fig_main.png'}"]
    except ImportError:
        md += ["", "matplotlib not installed; figure skipped"]

    # 6. A matched pair: same model, fact and language, forged labels; real update vs planted claim,
    # where the planted reply is a silent wrong recommendation.
    idx = {(r["model"], r["fact"], r["truth"], r["label"], r["lang"]): r for r in rows}
    cands = [r for r in rows if r["label"] == "forged" and r["truth"] == "planted" and r["lang"] == "en"
             and r.get("judge_relies_on") == "tool" and not r.get("discloses") and usable(r)]
    random.Random(3).shuffle(cands)
    for r in cands:
        twin = idx.get((r["model"], r["fact"], "real", "forged", r["lang"]))
        if twin and usable(twin) and len(r["reply"]) < 700 and len(twin["reply"]) < 700:
            md += ["", "## Example matched pair (forged labels, English)", "", f"Model {r['model']}, fact {r['fact']}.", "",
                   "**Real update:**", "", "> " + twin["reply"].replace("\n", "\n> "), "",
                   "**Planted claim (silent wrong recommendation):**", "", "> " + r["reply"].replace("\n", "\n> ")]
            break

    (out / "robust.json").write_text(json.dumps(res, indent=1, allow_nan=False))
    (out / "robust.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
