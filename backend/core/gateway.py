import os, httpx


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")

async def ask_llm(question: str) -> str:
    prompt = f"ענה בעברית: {question}"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(f"{OLLAMA_HOST}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except Exception as e:
            return f"שגיאה בתשובה: {e}"
