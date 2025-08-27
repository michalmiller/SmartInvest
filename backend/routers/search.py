from fastapi import APIRouter, Query
import json
import os

router = APIRouter()

@router.get("/")
def search_by_category(q: str = Query(..., alias="query")):
    file_path = os.path.abspath("investments.json")
    if not os.path.exists(file_path):
        return {"results": []}

    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)

    # חיפוש לפי קטגוריה
    results = [
        item for item in data
        if q.lower() in item.get("asset", "").lower()
    ]

    return {"results": results}
