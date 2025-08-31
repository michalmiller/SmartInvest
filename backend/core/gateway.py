import os, httpx
from googletrans import Translator

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "https://ollama-render-kwqx.onrender.com")
MODEL_NAME  = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_URL  = f"{OLLAMA_HOST.rstrip('/')}/api/generate"
translator = Translator()
async def call_ollama(prompt: str) -> str:
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    async with httpx.AsyncClient(timeout=120.0) as client:
        r = await client.post(OLLAMA_URL, json=payload)
        r.raise_for_status()
        return r.json().get("response", "[No response]")

async def ask_llm(question: str) -> str:
    print("🟣 שאלה שהוזנה:", question)

    # תרגום מעברית לאנגלית
    #translated = translator.translate(question, src='he', dest='en')
   # translated_question = translated.text
    # print("🟠 שאלה מתורגמת:", translated_question)

    # קריאה למודל
    response_en = await call_ollama(question)
    print("🟢 תשובה באנגלית:", response_en)

    # תרגום חזרה לעברית
    #translated = translator.translate(response_en, src='en', dest='he')
    #translated_answer = translated.text
    #print("🔵 תשובה מתורגמת לעברית:", response_en)

    return response_en
