import os

from dotenv import load_dotenv

load_dotenv()

IMGBB_API_URL = os.getenv("IMGBB_API_URL")
IMGBB_KEY = os.getenv("IMGBB_KEY")
