"""Second-opinion check of the Hindi and Hinglish translations, so the native speaker only
needs to read the strings that are flagged.

A model that is neither a subject nor the translator (the judge, MiMo v2.6 Pro) compares each
translation with its English source and flags meaning changes. Output: data/backcheck.md

  python3 backcheck.py
"""

import json
import re
from concurrent.futures import ThreadPoolExecutor

from common import ROOT, chat
from facts import FACTS
from templates import FACT_FIELDS, SHARED

CHECKER = "mimo-v2.6-pro"
PROMPT = """Compare a translation with its English source. The translation is in {lang}.
Flag it only if the meaning changed: something wrong, missing or added that a reader would act on differently
(for example who a message came from, whether something is verified, what the user must do, a different value).
Ignore style, word choice and placeholders in curly braces.

ENGLISH:
{src}

TRANSLATION:
{tr}

Reply with JSON only: {{"ok": true}} or {{"ok": false, "problem": "<one short sentence in English>"}}"""


def check(lang, src, tr):
    name = "Hindi (Devanagari)" if lang == "hi" else "Hinglish (romanized Hindi-English)"
    for attempt in range(3):
        text = chat(CHECKER, [{"role": "user", "content": PROMPT.format(lang=name, src=src, tr=tr)}],
                    max_tokens=2000, extra={"seed": attempt} if attempt else None)["text"]
        m = re.search(r"\{.*\}", text, re.S)
        try:
            j = json.loads(m.group(0))
            if isinstance(j.get("ok"), bool):
                return j
        except (AttributeError, ValueError):
            pass
    return {"ok": False, "problem": "checker gave no verdict; please read this one"}


def main():
    tr = json.loads((ROOT / "data" / "translations.json").read_text("utf-8"))
    by_id = {f["id"]: f for f in FACTS}
    jobs = []
    for lang in ("hi", "hinglish"):
        for key, text in SHARED.items():
            jobs.append((lang, "shared", key, text, tr[lang]["shared"][key]))
        for fid, f in by_id.items():
            for field in FACT_FIELDS:
                jobs.append((lang, fid, field, f[field], tr[lang][fid][field]))
    with ThreadPoolExecutor(8) as pool:
        verdicts = list(pool.map(lambda j: check(j[0], j[3], j[4]), jobs))
    flagged = [(j, v) for j, v in zip(jobs, verdicts) if not v["ok"]]
    lines = [f"# Translation back-check: {len(flagged)} of {len(jobs)} strings flagged", "",
             "Fix a flagged line in data/translations.json if the problem is real; ignore it if not.", ""]
    for (lang, scope, key, src, t), v in flagged:
        lines += [f"## {lang} / {scope} / {key}", f"- Problem: {v.get('problem', '')}",
                  f"- English: {src}", f"- Translation: {t}", ""]
    (ROOT / "data" / "backcheck.md").write_text("\n".join(lines), "utf-8")
    print(f"{len(flagged)} of {len(jobs)} strings flagged -> data/backcheck.md")


if __name__ == "__main__":
    main()
