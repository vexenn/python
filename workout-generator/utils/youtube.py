import os
import json
import requests
import re
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CACHE_FILE = 'video_cache.json'

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_to_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=4)

def clean_exercise_name(name):
    clean = re.sub(r'\(.*?\)', '', name)
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', clean)
    return clean.strip().lower() # Lowercase ensures "Wall Sit" and "wall sit" match

def get_youtube_video_id(search_query):
    cleaned_name = clean_exercise_name(search_query)
    cache = load_cache()

    # 1. Check Cache first (Free!)
    if cleaned_name in cache:
        return f"https://www.youtube.com/embed/{cache[cleaned_name]}"

    # 2. Try the API
    query = f"{cleaned_name} exercise tutorial"
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {"part": "snippet", "q": query, "key": YOUTUBE_API_KEY, "maxResults": 1, "type": "video"}

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("items"):
                video_id = data["items"][0]["id"]["videoId"]
                cache[cleaned_name] = video_id
                save_to_cache(cache)
                return f"https://www.youtube.com/embed/{video_id}"
    except:
        pass # Handle network errors silently
    
    # 3. THE FALLBACK (Quota Hit or Error)
    # If we get here, the API failed. Return a search link instead.
    # We replace spaces with '+' for a valid URL
    search_link = f"https://www.youtube.com/results?search_query={cleaned_name.replace(' ', '+')}+exercise"
    print(f"⚠️ Quota hit. Providing search fallback for: {cleaned_name}")
    return search_link