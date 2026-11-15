"""Shared helpers: .env loading, a cached OpenAI-compatible chat client, JSONL I/O."""

import hashlib
import json
import os
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
NO_THINKING = {"chat_template_kwargs": {"enable_thinking": False, "thinking": False}}


# Models served through Adaption's Responses API; everything else goes to the
# OpenAI-compatible chat endpoint (Vultr).
ADAPTION_MODELS = {"gemma-4-31b-it", "gemma-4-26b-a4b-it", "qwen3.5-397b", "glm-5.2", "deepseek-v4-flash", "glm-53-flash"}
ADAPTION_BASE = "https://api.prod.adaptionlabs.ai"


def _env():
    env = {}
    for path in (ROOT / ".env", ROOT.parent / "turnguard" / ".env"):
        if path.exists():
            for line in path.read_text().splitlines():
                name, sep, value = line.removeprefix("export ").partition("=")
                if sep:
                    env.setdefault(name.strip(), value.strip().strip("'\""))
    env.update(os.environ)
    return env


def load_env(model=None):
    env = _env()
    if model in ADAPTION_MODELS:
        key = env.get("ADAPTION_API_KEY")
        if not key:
            raise SystemExit("Set ADAPTION_API_KEY in .env")
        return env.get("ADAPTION_BASE_URL", ADAPTION_BASE).rstrip("/"), key
    base = env.get("VULTR_API_BASE") or env.get("CK_API_BASE") or env.get("TG_API_BASE")
    key = env.get("VULTR_API_KEY") or env.get("CK_API_KEY") or env.get("TG_API_KEY")
    if not (base and key):
        raise SystemExit("Set VULTR_API_BASE and VULTR_API_KEY (or CK_API_BASE / CK_API_KEY) in .env")
    return base.rstrip("/"), key


_lock = threading.Lock()


def chat(model, messages, *, max_tokens=400, temperature=0.0, extra=None, retries=6, timeout=180, cache_scope=None):
    """One chat completion, cached on disk by request content."""
    base, key = load_env(model)
    adaption = model in ADAPTION_MODELS
    if adaption:
        url = f"{base}/api/v1/responses"
        payload = {"model": model, "input": messages, "temperature": temperature,
                   "max_output_tokens": max_tokens, "store": False}
    else:
        url = f"{base}/chat/completions"
        payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
        payload.update(NO_THINKING)
    payload.update(extra or {})
    cache_request = [base, payload]
    if cache_scope is not None:
        cache_request.append(cache_scope)
    digest = hashlib.sha256(json.dumps(cache_request, sort_keys=True).encode()).hexdigest()
    path = CACHE / f"{digest}.json"
    if path.exists():
        try:
            cached = json.loads(path.read_text("utf-8"))
            if isinstance(cached, dict) and cached.get("text") and not cached.get("error"):
                return cached
        except (ValueError, OSError):
            pass
    body = json.dumps(payload).encode()
    last = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url, data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read())
            break
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:300].decode('utf-8', 'replace')}"
            if e.code != 429 and e.code < 500:
                raise RuntimeError(last) from None
        except (urllib.error.URLError, TimeoutError) as e:
            last = str(e)
        if attempt < retries:
            time.sleep(min(60, 2 ** attempt * 2))
    else:
        raise RuntimeError(f"API failed after retries: {last}")
    status = data.get("status")
    if status == "failed" or data.get("error") is not None:
        raise RuntimeError("Provider returned a failed response")
    if adaption:
        parts = [c.get("text") or "" for item in data.get("output") or [] if item.get("type") == "message"
                 for c in item.get("content") or [] if c.get("type") == "output_text"]
        text = data.get("output_text") or "".join(parts)
        reason = (data.get("incomplete_details") or {}).get("reason")
        finish = "length" if status == "incomplete" and reason == "max_output_tokens" else (reason or status)
        usage = data.get("usage") or {}
    else:
        msg = data["choices"][0]["message"]
        text = msg.get("content") or ""
        finish = data["choices"][0].get("finish_reason")
        usage = data.get("usage") or {}
    if "</think>" in text:
        text = text.split("</think>", 1)[1]
    elif "<think>" in text:  # reasoning was cut off before the answer
        text = ""
    out = {"text": text.strip(), "usage": usage, "finish": finish}
    if not out["text"]:
        return out
    CACHE.mkdir(exist_ok=True)
    tmp = path.with_suffix(f".{os.getpid()}.{threading.get_ident()}.tmp")
    tmp.write_text(json.dumps(out, ensure_ascii=False), "utf-8")
    tmp.replace(path)
    return out


def read_jsonl(path):
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def write_jsonl(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def degenerate(text):
    """A reply that collapses into one word repeated 10+ times in a row (e.g. 'our our our ...')."""
    import re
    return bool(re.search(r"(?<!\S)(\S+)(?:\s+\1){9,}(?!\S)", text or ""))


def usable(row):
    """A reply a user could act on: not empty or failed, not cut off by the token cap, not degenerate."""
    return bool(row.get("reply")) and not row.get("error") and row.get("finish") != "length" and not degenerate(row.get("reply"))
