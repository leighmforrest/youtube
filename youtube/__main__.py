import os
from dotenv import load_dotenv
import requests
from pprint import pprint

load_dotenv()

if __name__ == "__main__":
    youtube_key = os.getenv("YOUTUBE_KEY")
    handle = "RickBeato"
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q=@{handle}&type=channel&key={youtube_key}'

    
    response = requests.get(url)
    data = response.json()
    pprint(data)
