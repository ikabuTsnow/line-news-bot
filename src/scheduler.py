from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
from database import get_all_users, save_summary, get_summary
from line_sender import push_message
from news_fetcher import fetch_news
from summarizer import summarize

load_dotenv()
token = os.getenv("CHANNEL_ACCESS_TOKEN")

scheduler = BackgroundScheduler()

@scheduler.scheduled_job("cron", hour=6, minute=50)
def fetch_job():
    users = get_all_users()
    for user_id, topic, feed_url in users:
        article = fetch_news(feed_url)
        summary = summarize(article, topic)
        save_summary(user_id, summary)

@scheduler.scheduled_job("cron", hour=7, minute=0)
def send_job():
    users = get_all_users()
    for user_id, _, _ in users:
        summary = get_summary(user_id)
        push_message(summary, user_id, token)