"""Run the subject models on the episodes.

  python3 run.py --pilot              # 6 pilot episodes x 3 models (excluded from analysis)
  python3 run.py                      # 576 study episodes x 3 models
  python3 run.py --models glm-5.3     # one model
  python3 run.py --samples 3          # exploratory: 3 extra samples per episode at temperature 0.7

Output: runs/<model>.jsonl (or runs/pilot_<model>.jsonl). Successful non-empty replies are cached.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor

from common import ROOT, chat, read_jsonl, write_jsonl

MODELS = ("deepseek-v4.1-flash-1017", "glm-5.3", "qwen3.8-27b",            # Vultr
          "gemma-4-31b-it", "gemma-4-26b-a4b-it", "qwen3.5-397b", "glm-5.2")  # Adaption


# Per-model overrides, set from the pilot before any study run (see PREREG.md): these models
# reason before answering and their APIs did not turn it off, so 400 tokens left 2-5 of 6 replies empty.
MAX_TOKENS = {"glm-5.3": 8000, "glm-5.2": 8000, "qwen3.5-397b": 8000}  # 4,000 was not always enough (see PREREG deviations)


def run_one(model, ep, rep=0, cache_scope=None):
    temp, extra = (0.0, None) if rep == 0 else (0.7, {"seed": rep})
    cap = MAX_TOKENS.get(model, 400)
    retried, first_finish = False, None
    try:
        out = chat(model, ep["messages"], max_tokens=cap, temperature=temp, extra=extra,
                   cache_scope=cache_scope)
        first_finish = out["finish"]
        if not out["text"] and first_finish == "length":
            retried = True
            cap *= 4
            out = chat(model, ep["messages"], max_tokens=cap, temperature=temp, extra=extra,
                       cache_scope=cache_scope)
        reply, finish, usage, error = out["text"], out["finish"], out["usage"], None
    except Exception as exc:
        reply, finish, usage, error = "", None, {}, str(exc)[:300]
    return {"id": ep["id"], "model": model, "rep": rep, "reply": reply, "finish": finish,
            "usage": usage, "error": error, "cap_retry": retried, "first_finish": first_finish,
            "max_tokens": cap}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=list(MODELS))
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--samples", type=int, default=0)
    ap.add_argument("--policy", action="store_true", help="exploratory prompt-fix episodes")
    ap.add_argument("--scope-cache", action="store_true", help="scope cached replies by episode and replicate")
    a = ap.parse_args()
    src = "pilot.jsonl" if a.pilot else ("episodes_policy.jsonl" if a.policy else "episodes.jsonl")
    eps = read_jsonl(ROOT / "data" / src)
    for model in a.models:
        jobs = [(e, r) for e in eps for r in (range(1, a.samples + 1) if a.samples else [0])]
        done = [0]

        def tick(j):
            ep, rep = j
            scope = (src, ep["id"], rep) if a.scope_cache else None
            r = run_one(model, ep, rep, cache_scope=scope)
            done[0] += 1
            if done[0] % 50 == 0 or done[0] == len(jobs):
                print(f"  {model}: {done[0]}/{len(jobs)}", flush=True)
            return r

        with ThreadPoolExecutor(a.concurrency) as pool:
            rows = list(pool.map(tick, jobs))
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
