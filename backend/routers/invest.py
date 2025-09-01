from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List
from backend.services.somee_client import save_json, load_json

 # קובץ השירות שלך ל-Somee

router = APIRouter()
KEY = "investments"  # ישמר כ-investments.json ב-Somee

@router.post("/")
def add_investment(data: Dict[str, Any]):
    try:
        cur: List[Dict[str, Any]] = load_json(KEY) or []
        if not isinstance(cur, list):
            cur = []
        cur.append(data)
        save_json(KEY, cur)
        return {"status": "saved", "investment": data}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Somee error: {e}")

@router.get("/")
def get_all_investments():
    try:
        data = load_json(KEY) or []
        return {"investments": data if isinstance(data, list) else []}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Somee error: {e}")

@router.get("/summary/")
def investment_summary():
    try:
        data: List[Dict[str, Any]] = load_json(KEY) or []
        summary: Dict[str, int] = {}
        for it in data:
            cat = (it.get("category") or "Other")
            summary[cat] = summary.get(cat, 0) + 1
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Somee error: {e}")

@router.get("/risk-summary/")
def risk_summary():
    try:
        data: List[Dict[str, Any]] = load_json(KEY) or []
        summary = {"low": 0, "medium": 0, "high": 0}
        for it in data:
            rk = (it.get("risk") or "").lower()
            if rk in summary:
                summary[rk] += 1
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Somee error: {e}")
