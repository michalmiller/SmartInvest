import httpx
from googletrans import Translator

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"

translator = Translator()

async def call_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "[No response]")
    except Exception as e:
        return f"[ERROR: {e}]"

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
