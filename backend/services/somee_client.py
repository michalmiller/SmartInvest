# somee_client.py
import os, requests, json
from typing import Any, Dict

SOMEE_BASE = os.getenv("SOMEE_BASE", "").rstrip("/")
# במקום לבדוק אם SOMEE_API_KEY קיים, אפשר פשוט לא להשתמש בו
# או להגדיר אותו כערך ריק אם אין צורך

SOMEE_API_KEY = os.getenv("SOMEE_API_KEY", "")
print(f"SOMEE_API_KEY: {SOMEE_API_KEY}")  # הדפסת הערך

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

def load_json(key: str) -> Union[Any, None]:
    """טעינת JSON מ-Somee"""
    try:
        # לטעינה, נשתמש בקובץ שנשמר
        url = f"{SOMEE_BASE}/{key}.json"
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # קובץ לא קיים - זה בסדר, נחזיר None
            return None
        else:
            print(f"Somee load error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error loading from Somee: {e}")
        return None