from dotenv import load_dotenv
import os
from news_fetcher import fetch_news
from summarizer import summarize
from line_sender import push_message

load_dotenv()

user_id =os.getenv("USER_ID")
token = os.getenv("CHANNEL_ACCESS_TOKEN")

def main():
    newses = fetch_news("https://rss.asahi.com/rss/asahi/newsheadlines.rdf")
    res = summarize(newses, "")
    push_message(res, user_id, token)
    return 0

if __name__ == "__main__":
    main()