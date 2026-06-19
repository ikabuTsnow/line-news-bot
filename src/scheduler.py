from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
from database import get_all_users, save_summary, get_summary, save_quiz, get_quiz
from news_fetcher import fetch_news
from line_sender import push_message
from summarizer import summarize
from quiz import generate_quiz

load_dotenv()
token = os.getenv("CHANNEL_ACCESS_TOKEN")

scheduler = BackgroundScheduler()

@scheduler.scheduled_job("cron", hour=6, minute=50)
def fetch_job():
    print("fetch_job start")
    users = get_all_users()
    for user_id, topic in users:
        article = fetch_news(topic)
        summary = summarize(article, topic)
        save_summary(user_id, summary)

        quiz = generate_quiz(article)
        if quiz:
            save_quiz(user_id, quiz["question"], quiz["answer"])
    print("fetch_job complete")


@scheduler.scheduled_job("cron", hour=7, minute=0)
def send_news_job():
    print("send_news_job start")
    users = get_all_users()
    for user_id, _, _ in users:
        summary = get_summary(user_id)
        push_message(summary, user_id, token)
    print("send_news_job complete")

@scheduler.scheduled_job("cron", hour=12, minute=0)
def send_quiz_job():
    print("send_quiz_job start")
    users = get_all_users()
    for user_id, _, _ in users:
        quiz = get_quiz(user_id)
        if quiz:
            question, answer = quiz
            push_message(f"❓ 今日のクイズ！\n\n{question}\n\n番号で答えてください！", user_id, token)
    print("send_quiz_job complete")