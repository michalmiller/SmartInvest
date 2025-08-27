from fastapi import APIRouter, Body
import os
import json
from datetime import datetime

router = APIRouter()

DATA_FILE = os.path.join(os.path.dirname(__file__), "../investments.json")

@router.post("/")
def add_investment(data: dict = Body(...)):
    data["timestamp"] = datetime.now().isoformat()  # הוספת תאריך ושעה

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.append(data)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    return {"status": "saved", "investment": data}

@router.get("/summary/")
def investment_summary():
    if not os.path.exists(DATA_FILE):
        return {"summary": {}}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary = {}
    for item in data:
        cat = item.get("category", "Other")
        summary[cat] = summary.get(cat, 0) + 1

    return {"summary": summary}

@router.get("/")
def get_all_investments():
    if not os.path.exists(DATA_FILE):
        return {"investments": []}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {"investments": data}

@router.get("/risk-summary/")
def risk_summary():
    file_path = os.path.abspath("investments.json")
    if not os.path.exists(file_path):
        return {"summary": {}}

    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)

    summary = {"low": 0, "medium": 0, "high": 0}

    for item in data:
        risk = item.get("risk", "").lower()
        if risk in summary:
            summary[risk] += 1

    return {"summary": summary}


