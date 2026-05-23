from dotenv import load_dotenv
import os
from flask import Flask, request
from scheduler import scheduler
from config import FEED_URLS, TOPICS, DEFAULT_FEED_URL, DEFAULT_TOPIC
from database import init_db, save_user, get_user
from line_sender import reply_message, send_quick_reply

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

        if text in FEED_URLS:
            existing = get_user(user_id)
            topic = existing[0] if existing else ""
            save_user(user_id, topic=topic, feed_url=FEED_URLS[text])
            reply_message(f"{text}に設定しました！", reply_token, token)

        elif text in TOPICS:
            existing = get_user(user_id)
            feed_url = existing[1] if existing else ""
            save_user(user_id, topic=TOPICS[text], feed_url=feed_url)
            reply_message(f"トピックを{text}に設定しました！", reply_token, token)

        else:
            options = list(FEED_URLS.keys()) + list(TOPICS.keys())
            send_quick_reply("選択肢を選んでください", options, reply_token, token)
    return "OK"


if __name__ == "__main__":
    init_db()
    if not get_user(my_user_id):
        save_user(my_user_id, DEFAULT_TOPIC, DEFAULT_FEED_URL)
    scheduler.start()
    app.run(port=5000)