import os
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
USER_ID = os.getenv("USER_ID")

if not STEAM_API_KEY:
    raise ValueError("Missing STEAM_API_KEY in environment")