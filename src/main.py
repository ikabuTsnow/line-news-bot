from dotenv import load_dotenv
import os
from flask import Flask, request
from scheduler import scheduler
from config import DEFAULT_TOPIC, QUICK_TOPICS
from database import init_db, save_user, get_user
from line_sender import reply_message, push_message
from rich_menu import create_rich_menu
from news_fetcher import fetch_news
from summarizer import summarize

load_dotenv()
my_user_id = os.getenv("USER_ID")
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
            save_user(user_id, DEFAULT_TOPIC)
            print("saved_user")

        if text == "ニュース！":
            try:
                existing = get_user(user_id)
                topic = existing[0] if existing else DEFAULT_TOPIC
                reply_message("ニュースを取得中です...", reply_token, token)
                articles = fetch_news(topic)
                summary = summarize(articles, topic)
                push_message(summary, user_id, token)
            except Exception as e:
                print(f"Error: {e}")
                push_message("ニュースの取得に失敗しました。", user_id, token)
        else:
            save_user(user_id, topic=text)
            reply_message(f"トピックを「{text}」に設定しました！", reply_token, token)

    return "OK"

if __name__ == "__main__":
    init_db()
    if not get_user(my_user_id):
        save_user(my_user_id, DEFAULT_TOPIC)
    create_rich_menu()
    push_message("🔄 サーバーが再起動されました", my_user_id, token)
    scheduler.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)