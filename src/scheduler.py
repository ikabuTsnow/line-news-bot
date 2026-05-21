from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
from database import get_all_users
from line_sender import push_message
from news_fetcher import fetch_news
from summarizer import summarize

load_dotenv()
token = os.getenv("CHANNEL_ACCESS_TOKEN")

scheduler = BackgroundScheduler()

@scheduler.scheduled_job("cron", hour=7, minute=0)
def job():
    users = get_all_users()
    for user_id, topic, feed_url in users:
        articles = fetch_news(feed_url)
        summary = summarize(articles, topic)
        push_message(summary, user_id, token)

