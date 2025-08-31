# gui_config.py
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

RENDER_API = os.getenv("RENDER_API", "https://michalinvest.onrender.com").rstrip("/")
