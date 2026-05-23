import feedparser
from config import DEFAULT_FEED_URL

def fetch_news(feed_url: str = DEFAULT_FEED_URL, max_items: int = 20):
    feed = feedparser.parse(feed_url)

    if getattr(feed, "bozo", False):
        print(f"Feed warning: {feed.get('bozo_exception')}")

    entries = feed.entries[:max_items]
    entries_dict = []
    for entry in entries:
        title = entry.get("title", "")
        description = entry.get("summary", entry.get("description", ""))
        url = entry.get("link", "")
        entries_dict.append({
            "title": title,
            "description": description,
            "url": url
        })

    return entries_dict


