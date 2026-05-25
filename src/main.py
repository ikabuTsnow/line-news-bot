from dotenv import load_dotenv
import os
from flask import Flask, request
from scheduler import scheduler
from config import FEED_URLS, DEFAULT_FEED_URL, DEFAULT_TOPIC
from database import init_db, save_user, get_user
from news_fetcher import fetch_news
from line_sender import reply_message
from summarizer import summarize
from line_sender import push_message
from rich_menu import create_rich_menu

load_dotenv()
my_user_id =os.getenv("USER_ID")
token = os.getenv("CHANNEL_ACCESS_TOKEN")

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()
    events = body["events"]
    for event in events:
        user_id = event["source"]["userId"]
        reply_token = event["replyToken"]
        text = event["message"]["text"]

        if not get_user(user_id):
            save_user(user_id, DEFAULT_TOPIC, DEFAULT_FEED_URL)
            print("saved_user")

        if text in FEED_URLS:
            existing = get_user(user_id)
            topic = existing[0] if existing else ""
            save_user(user_id, topic=topic, feed_url=FEED_URLS[text])
            reply_message(f"{text}に設定しました！", reply_token, token)
        elif text == "ニュース！":
            existing = get_user(user_id)
            if existing:
                topic, feed_url = existing
            else:
                topic, feed_url = DEFAULT_TOPIC, DEFAULT_FEED_URL
            
            try:
                reply_message("ニュースを取得中です...", reply_token, token)
                articles = fetch_news(feed_url)
                summary = summarize(articles, topic)
                push_message(summary, user_id, token)
            except Exception as e:
                print(f"Error: {e}")
                push_message("ニュースの取得に失敗しました。", user_id, token)
        else:
            existing = get_user(user_id)
            feed_url = existing[1] if existing else DEFAULT_FEED_URL
            save_user(user_id, topic=text, feed_url=feed_url)
            reply_message(f"トピックを「{text}」に設定しました！", reply_token, token)

    return "OK"


if __name__ == "__main__":
    init_db()
    if not get_user(my_user_id):
        save_user(my_user_id, DEFAULT_TOPIC, DEFAULT_FEED_URL)
    create_rich_menu()
    scheduler.start()
    app.run(host="0,0,0,0", port=5000)