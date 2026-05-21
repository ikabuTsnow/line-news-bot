from dotenv import load_dotenv
import os
from flask import Flask, request
from config import FEED_URLS, TOPICS
from database import init_db, save_user, get_user
from news_fetcher import fetch_news
from summarizer import summarize
from line_sender import push_message, reply_message

load_dotenv()
user_id =os.getenv("USER_ID")
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

        if text in FEED_URLS:
            save_user(user_id, topic="", feed_url=FEED_URLS[text])
            reply_message(f"{text}に設定しました！", reply_token, token)
        elif text in TOPICS:
            save_user(user_id, topic=TOPICS[text], feed_url="")
            reply_message(f"トピックを{text}に設定しました！", reply_token, token)
        else:
            reply_message(f"選択肢：{list(FEED_URLS.keys()) + list(TOPICS.keys())}", reply_token, token)
    return "OK"


if __name__ == "__main__":
    init_db()
    app.run(port=5000)