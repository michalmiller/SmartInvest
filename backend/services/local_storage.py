import json
import os
from typing import Any

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "storage")

def _path(filename: str) -> str:
    os.makedirs(BASE_DIR, exist_ok=True)
    return os.path.join(BASE_DIR, filename)

def load_json(filename: str) -> Any:
    path = _path(filename)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(filename: str, data: Any) -> None:
    path = _path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
