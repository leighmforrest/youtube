import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.googleapis.com/youtube/v3"
YOUTUBE_KEY = os.getenv("YOUTUBE_KEY")
DB_PATH = Path(__file__).parent.parent
