"""Run the subject models on the episodes.

  python3 run.py --pilot              # 6 pilot episodes x 3 models (excluded from analysis)
  python3 run.py                      # 576 study episodes x 3 models
  python3 run.py --models glm-5.3     # one model
  python3 run.py --samples 3          # exploratory: 3 extra samples per episode at temperature 0.7

Output: runs/<model>.jsonl (or runs/pilot_<model>.jsonl). Re-running is free: replies are cached.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor

from common import ROOT, chat, read_jsonl, write_jsonl

MODELS = ("deepseek-v4.1-flash-1017", "glm-5.3", "qwen3.8-27b",            # Vultr
          "gemma-4-31b-it", "gemma-4-26b-a4b-it", "qwen3.5-397b", "glm-5.2")  # Adaption


# Per-model overrides, set from the pilot before any study run (see PREREG.md): these models
# reason before answering and their APIs did not turn it off, so 400 tokens left 2-5 of 6 replies empty.
MAX_TOKENS = {"glm-5.3": 8000, "glm-5.2": 8000, "qwen3.5-397b": 8000}  # 4,000 was not always enough (see PREREG deviations)


def run_one(model, ep, rep=0):
    temp, extra = (0.0, None) if rep == 0 else (0.7, {"seed": rep})
    try:
        cap = MAX_TOKENS.get(model, 400)
        out = chat(model, ep["messages"], max_tokens=cap, temperature=temp, extra=extra)
        retried = False
        if not out["text"] and out["finish"] == "length":
            # Pre-registered (deviation 3): a reply left empty by the token cap is re-run once at 4x the cap.
            out = chat(model, ep["messages"], max_tokens=cap * 4, temperature=temp, extra=extra)
            retried = True
        return {"id": ep["id"], "model": model, "rep": rep, "reply": out["text"], "finish": out["finish"],
                "usage": out["usage"], "error": None, "cap_retry": retried}
    except Exception as e:  # transport errors already retried 6 times inside chat()
        return {"id": ep["id"], "model": model, "rep": rep, "reply": "", "finish": None, "usage": {}, "error": str(e)[:300]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=list(MODELS))
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--samples", type=int, default=0)
    ap.add_argument("--policy", action="store_true", help="exploratory prompt-fix episodes")
    a = ap.parse_args()
    src = "pilot.jsonl" if a.pilot else ("episodes_policy.jsonl" if a.policy else "episodes.jsonl")
    eps = read_jsonl(ROOT / "data" / src)
    for model in a.models:
        jobs = [(e, r) for e in eps for r in (range(1, a.samples + 1) if a.samples else [0])]
        with ThreadPoolExecutor(a.concurrency) as pool:
            rows = list(pool.map(lambda j: run_one(model, *j), jobs))
        sub = ("policy/" if a.policy else "") + ("samples/" if a.samples else "")
        path = ROOT / "runs" / f"{sub}{'pilot_' if a.pilot else ''}{model}.jsonl"
        write_jsonl(path, rows)
        errs = sum(1 for r in rows if r["error"])
        empty = sum(1 for r in rows if not r["reply"])
        cut = sum(1 for r in rows if r["finish"] == "length")
        retried = sum(1 for r in rows if r.get("cap_retry"))
        print(f"{model}: {len(rows)} replies, {errs} errors, {empty} empty, {cut} hit max tokens, "
              f"{retried} re-run at a higher cap -> {path}")
        if a.pilot:
            for r in rows:
                print(f"\n--- {r['id']}\n{r['reply'][:600]}")


if __name__ == "__main__":
    main()
