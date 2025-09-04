import requests
import os
from typing import Any, Dict, List, Union

# הגדרות מקובץ .env
SOMEE_BASE = os.getenv("SOMEE_BASE", "http://www.michalmiller.somee.com")
SOMEE_API_KEY = os.getenv("SOMEE_API_KEY", "InvestApp_Secure_789_Key")

def save_json(key: str, data: Any) -> bool:
    """שמירת JSON ב-Somee באמצעות POST"""
    try:
        # בנית ה-URL עם הפרמטרים ישירות
        url = f"{SOMEE_BASE}/upload.php?key={key}&api_key={SOMEE_API_KEY}"
        
        # שליחת POST request עם הנתונים ב-body
        response = requests.post(
            url,
            data=str(data).encode('utf-8') if isinstance(data, dict) else str(data).encode('utf-8'),
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Request method: POST")
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            return result.get("ok", False)
        else:
            print(f"Somee save error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error saving to Somee: {e}")
        return False

def load_json(key: str) -> Union[Any, None]:
    """טעינת JSON מ-Somee"""
    try:
        # לטעינה, נשתמש בקובץ שנשמר
        url = f"{SOMEE_BASE}/{key}.json"
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # קובץ לא קיים - זה בסדר, נחזיר None
            return None
        else:
            print(f"Somee load error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error loading from Somee: {e}")
        return None