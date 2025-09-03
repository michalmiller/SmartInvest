# somee_client.py
import os, requests, json
from typing import Any, Dict

SOMEE_BASE = os.getenv("SOMEE_BASE", "").rstrip("/")
SOMEE_API_KEY = os.getenv("SOMEE_API_KEY", "")

def _must_cfg():
    if not SOMEE_BASE or not SOMEE_API_KEY:
        raise RuntimeError("SOMEE_BASE / SOMEE_API_KEY are not set")

def save_json(key: str, data: Any) -> Dict[str, Any]:
    _must_cfg()
    r = requests.post(
        f"{SOMEE_BASE}/upload.php",
        params={"key": key, "api_key": SOMEE_API_KEY},
        json=data,
        timeout=15
    )
    r.raise_for_status()
    if r.headers.get("content-type","").startswith("application/json"):
        return r.json()
    return {"ok": True}

def load_json(key: str) -> Any:
    try:
        with open(f"backend/data/{key}.json", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ שגיאה בקריאת {key}.json: {e}")
        return []
