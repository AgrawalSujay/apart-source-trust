"""Upload the training sets to Adaption and run AutoScientist (exploratory fine-tuned fix).

  pip install adaption
  python3 launch.py upload            # uploads data/train_en.csv and data/train_multi.csv as raw datasets
  python3 launch.py models            # lists AutoScientist base models available to this key
  python3 launch.py plan              # shows the hyperparameters AutoScientist would use (launches nothing)
  python3 launch.py train --yes       # starts one SFT run per dataset (spends credits)
  python3 launch.py train en --yes    # only the English-only run
  python3 launch.py status            # run status and win rates
  python3 launch.py download          # best checkpoints -> checkpoints/<arm>/

State (dataset and run ids) is kept in data/adaption_state.json. Reads ADAPTION_API_KEY from .env.
"""

import json
import sys
import tarfile

from common import ROOT, _env

STATE = ROOT / "data" / "adaption_state.json"
BASE_MODEL = "Qwen/Qwen3.5-4B"
ARMS = ("en", "multi")


def client():
    from adaption import Adaption
    return Adaption(api_key=_env()["ADAPTION_API_KEY"])


def load():
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save(state):
    STATE.write_text(json.dumps(state, indent=1))


def upload():
    c, state = client(), load()
    for arm in ARMS:
        if state.get(arm, {}).get("dataset_id"):
            print(arm, "already uploaded:", state[arm]["dataset_id"])
            continue
        up = c.datasets.upload_file(ROOT / "data" / f"train_{arm}.csv", name=f"source-trust-train-{arm}",
                                    processing_mode="raw", column_mapping={"prompt": "prompt", "completion": "completion"})
        c.datasets.wait_for_completion(up.dataset_id)
        state.setdefault(arm, {})["dataset_id"] = up.dataset_id
        save(state)
        print(arm, "uploaded:", up.dataset_id)


def models():
    for m in client().autoscientist.list_models().models:
        print(m.id, getattr(m, "api_model_size", ""), getattr(m, "methods", ""), getattr(m, "training_types", ""))


def plan():
    c, state = client(), load()
    for arm in ARMS:
        hp = c.autoscientist.recommend_hyperparams(dataset_id=state[arm]["dataset_id"], model=BASE_MODEL)
        print(arm, hp)


def train():
    if "--yes" not in sys.argv:
        raise SystemExit("This spends credits. Check the price in the app first, then re-run with --yes.")
    c, state = client(), load()
    arms = [a for a in ARMS if a in sys.argv] or ARMS
    for arm in arms:
        if state[arm].get("run_id"):
            print(arm, "already running:", state[arm]["run_id"])
            continue
        run = c.autoscientist.create(dataset_id=state[arm]["dataset_id"], model=BASE_MODEL,
                                     training_method="instruction", max_iterations=3,
                                     idempotency_key=f"source-trust-{arm}-v1")
        state[arm]["run_id"] = run.id
        save(state)
        print(arm, "run:", run.id, run.status)


def status():
    c, state = client(), load()
    for arm in ARMS:
        if state.get(arm, {}).get("run_id"):
            r = c.autoscientist.get(state[arm]["run_id"])
            print(arm, r.status, "iterations", r.iterations_completed, "best win rate", r.best_win_rate,
                  "download", r.download_available, getattr(r, "error", None) or "")


def download():
    c, state = client(), load()
    for arm in ARMS:
        out = ROOT / "checkpoints" / arm
        out.mkdir(parents=True, exist_ok=True)
        tgz = out / "best-checkpoint.tgz"
        with c.autoscientist.with_streaming_response.download(state[arm]["run_id"]) as resp:
            resp.stream_to_file(tgz)
        with tarfile.open(tgz) as t:
            t.extractall(out, filter="data")
        print(arm, "->", out)


if __name__ == "__main__":
    {"upload": upload, "models": models, "plan": plan, "train": train, "status": status,
     "download": download}[sys.argv[1]]()
