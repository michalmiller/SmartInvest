from fastapi import APIRouter, Body
import os
import json
from datetime import datetime
router = APIRouter()

DATA_FILE = os.path.join(os.path.dirname(__file__), "../portfolio.json")
@router.get("/")
def get_portfolio():
    return {"portfolio": []}


@router.post("/")
def add_portfolio(data: dict = Body(...)):
    data["timestamp"] = datetime.now().isoformat()  # הוספת תאריך ושעה

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.append(data)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    return {"status": "saved", "portfolio": data}