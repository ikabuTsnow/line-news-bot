import feedparser

FEED_URL = "https://rss.asahi.com/rss/asahi/newsheadlines.rdf"


def fetch_news(feed_url: str, max_items: int = 5):
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


