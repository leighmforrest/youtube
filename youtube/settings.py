import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3/"
BASE_DIR = Path(__file__).parent.parent / "data"
