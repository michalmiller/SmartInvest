from fastapi import APIRouter
from gateway import ask_llm  # ← מתקן את ה-import שהיה ל-core.gateway

router = APIRouter()

@router.get("/")
async def ask(question: str):
    response = await ask_llm(question)
    return {"answer_he": response} 
