import requests
import os
from dotenv import load_dotenv

load_dotenv()
gnews_api_key = os.getenv("GNEWS_API_KEY")

def fetch_news(topic: str, max_items: int = 20) -> list[dict]:
    try:
        response = requests.get(
            "https://gnews.io/api/v4/search",
            params={
                "q": topic,
                "lang": "ja",
                "max": max_items,
                "apikey": gnews_api_key
            },
            timeout=10
        )
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return [
            {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "url": a.get("url", "")
            }
            for a in articles
        ]
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []