from fastapi import APIRouter
from core.gateway import ask_llm

router = APIRouter()

@router.get("/")
async def ask(question: str):
    response = await ask_llm(question)
    return {"answer_he": response} 
