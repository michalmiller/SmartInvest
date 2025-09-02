from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List
from backend.services.somee_client import save_json, load_json 


router = APIRouter()
KEY = "portfolio"

@router.post("/")
def add_portfolio(data: Dict[str, Any]):
    try:
        cur: List[Dict[str, Any]] = load_json(KEY) or []
        if not isinstance(cur, list):
            cur = []
        cur.append(data)
        save_json(KEY, cur)
        return {"status": "saved", "portfolio": data}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Somee error: {e}")

@router.get("/")
def get_portfolio():
    try:
        data = load_json(KEY) or []
        return data if isinstance(data, list) else []
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Somee error: {e}")
