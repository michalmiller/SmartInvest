from fastapi import APIRouter, Query
from backend.services.somee_client import load_json


router = APIRouter()
KEY = "investments"

@router.get("/")
def search_by_category(q: str = Query(..., alias="query")):
    data = load_json(KEY) or []
    ql = (q or "").strip().lower()
    results = [item for item in data if ql in (item.get("asset", "").lower())]
    return {"results": results}
