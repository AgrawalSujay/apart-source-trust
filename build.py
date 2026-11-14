"""Build the study episodes (1,152 = 48 facts x 2 truths x 4 labels x 3 languages) and the 6 pilot episodes from facts + translations.

Output: data/episodes.jsonl, data/pilot.jsonl. Run: python3 build.py
English needs no translation file; Hindi and Hinglish read data/translations.json.
"""

import json
import random

from common import ROOT, write_jsonl
from facts import FACTS
from templates import FACT_FIELDS, SHARED

TRUTHS = ("real", "planted")
LABELS = ("none", "informative", "placebo", "forged")
LANGS = ("en", "hi", "hinglish")


def load_translations():
    path = ROOT / "data" / "translations.json"
    tr = json.loads(path.read_text("utf-8")) if path.exists() else {}
    tr["en"] = {"shared": dict(SHARED), **{f["id"]: {k: f[k] for k in FACT_FIELDS} for f in FACTS}}
    return tr


def messages(fact, truth, label, lang, tr, policy=False):
    s, t = tr[lang]["shared"], tr[lang][fact["id"]]
    system = s["system"].format(org=fact["org"], name=t["name"], stored=fact["stored"])
    if policy:
        system += "\n\n" + s["policy"]
    call = f'{s["assistant_call"]}\nCALL {fact["tool"]}("{fact["entity"]}")'
    lines = [s["tool_header"].format(tool=fact["tool"])]
    if label in ("informative", "forged"):
        lines.append(s["prov_source"].format(source=t["official"] if truth == "real" else t["outside"]))
    elif label == "placebo":
        lines.append(s["prov_placebo"].format(tool=fact["tool"]))
    body = t["record"].format(value=fact["new"])
    if label == "forged":
        body += " " + s["forged"].format(official=t["official"])
    lines.append(body)
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": t["task"]},
        {"role": "assistant", "content": call},
        {"role": "user", "content": "\n".join(lines)},
    ]


def episode(fact, truth, label, lang, tr, pilot=False, policy=False):
    return {
        "id": f"{'pilot:' if pilot else ''}{fact['id']}|{truth}|{label}|{lang}",
        "fact": fact["id"], "domain": fact["domain"], "truth": truth, "label": label, "lang": lang,
        "stored": fact["stored"], "new": fact["new"],
        "messages": messages(fact, truth, label, lang, tr, policy),
    }


def main():
    tr = load_translations()
    missing = [l for l in LANGS if l not in tr]
    if missing:
        raise SystemExit(f"missing translations for {missing}: run translate.py first")
    eps = [episode(f, tv, lb, lg, tr) for f in FACTS for tv in TRUTHS for lb in LABELS for lg in LANGS]
    n = len(FACTS) * len(TRUTHS) * len(LABELS) * len(LANGS)
    assert len(eps) == n == 1152 and len({e["id"] for e in eps}) == n
    # Within a fact and language, the record text must be identical across truths
    # (only provenance metadata differs).
    for e in eps:
        if e["truth"] == "real":
            twin = next(x for x in eps if x["id"] == e["id"].replace("|real|", "|planted|"))
            same = e["messages"][3]["content"].splitlines()[-1] == twin["messages"][3]["content"].splitlines()[-1]
            assert same, e["id"]
            if e["label"] in ("none", "placebo"):
                assert e["messages"] == twin["messages"], e["id"]
    write_jsonl(ROOT / "data" / "episodes.jsonl", eps)
    # Exploratory prompt fix: same episodes and ids, with the source policy in the system prompt.
    pol = [episode(f, tv, lb, lg, tr, policy=True) for f in FACTS for tv in TRUTHS for lb in LABELS for lg in LANGS]
    write_jsonl(ROOT / "data" / "episodes_policy.jsonl", pol)

    # Pilot: 2 facts with stored/new swapped (so no pilot prompt equals a study prompt),
    # informative labels, one per truth x language. Excluded from analysis.
    rng = random.Random(7)
    pilot = []
    for i, f in enumerate(rng.sample(FACTS, 2)):
        swapped = {**f, "stored": f["new"], "new": f["stored"]}
        for j, lg in enumerate(LANGS):
            pilot.append(episode(swapped, TRUTHS[(i + j) % 2], "informative", lg, tr, pilot=True))
    write_jsonl(ROOT / "data" / "pilot.jsonl", pilot)
    print(f"wrote {len(eps)} study episodes and {len(pilot)} pilot episodes to data/")


if __name__ == "__main__":
    main()
