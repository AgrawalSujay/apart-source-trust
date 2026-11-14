"""Translate the templates and fact fields into Hindi and Hinglish (once, cached).

The translator (MiniMax M3.1 Flash) is not one of the study's subject models.
Placeholders in braces and fact values are protected and checked after translation.
Output: data/translations.json. Run: python3 translate.py
"""

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor

from common import ROOT, chat
from facts import FACTS
from templates import FACT_FIELDS, SHARED

TRANSLATOR = "minimax-m3.1-flash"
LANGS = {
    "hi": "Hindi in Devanagari script, as written in everyday Indian office messages",
    "hinglish": "Hinglish: Hindi written in Latin (Roman) script mixed naturally with English, as Indians type in chats",
}


def translate(text, lang):
    keep = re.findall(r"\{[a-z_]+\}", text)
    prompt = (
        f"Translate the text below into {LANGS[lang]}.\n"
        "Rules: keep every placeholder in curly braces exactly as it is; keep names of people, "
        "companies, email addresses, URLs, codes, numbers and tool names unchanged; keep line breaks "
        "and the square brackets; do not add anything. Reply with the translation only.\n\nTEXT:\n" + text
    )
    for attempt in range(3):
        # Generous budget: if the translator reasons before answering, a small cap leaves an empty reply.
        out = chat(TRANSLATOR, [{"role": "user", "content": prompt}], max_tokens=4000,
                   extra={"seed": attempt} if attempt else None)["text"].strip()
        out = re.sub(r"^(TEXT|Translation|अनुवाद)\s*:\s*", "", out).strip()
        if all(k in out for k in keep) and out:
            return out
    print(f"FAILED ({lang}): {text[:80]!r} -> last output {out[:120]!r}")
    return None


def main():
    jobs = []
    for lang in LANGS:
        for key, text in SHARED.items():
            jobs.append((lang, "shared", key, text))
        for f in FACTS:
            for field in FACT_FIELDS:
                jobs.append((lang, f["id"], field, f[field]))
    with ThreadPoolExecutor(6) as pool:
        results = list(pool.map(lambda j: translate(j[3], j[0]), jobs))
    failed = [j for j, tr in zip(jobs, results) if tr is None]
    if failed:
        raise SystemExit(f"{len(failed)} strings failed to translate (see FAILED lines above); "
                         "re-run: finished ones are cached and cost nothing.")
    out = {}
    for (lang, scope, key, src), tr in zip(jobs, results):
        out.setdefault(lang, {}).setdefault(scope, {})[key] = tr
    # Every protected token in the English source must survive.
    problems = []
    for (lang, scope, key, src), tr in zip(jobs, results):
        for tok in re.findall(r"[\w.+-]+@[\w.-]+|https?://\S+|\b[A-Z]{2,}[-\w]*\d[\w-]*\b", src):
            if tok.rstrip(".,") not in tr:
                problems.append(f"{lang}/{scope}/{key}: lost {tok}")
    path = ROOT / "data" / "translations.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), "utf-8")
    print(f"wrote {path} ({len(jobs)} strings)")
    if problems:
        print("CHECK THESE (protected tokens changed):\n" + "\n".join(problems))
        sys.exit(1)


if __name__ == "__main__":
    main()
