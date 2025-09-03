# gui_config.py
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

RENDER_API = os.getenv("RENDER_API", "https://smartinvest-ms9n.onrender.com").rstrip("/")
