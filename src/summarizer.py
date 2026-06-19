from dotenv import load_dotenv
import requests
import time
import os
from config import DEFAULT_TOPIC
from prompts import PROMPT_WITH_TOPIC, PROMPT_WITHOUT_TOPIC

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def summarize(articles: list[dict], topic: str = DEFAULT_TOPIC) -> str:

    # ニュースの読み取り
    blocks = []
    for article in articles:
        title = article["title"]
        description = article["description"]
        url = article["url"]

        block = f"""
                タイトル:{title}
                説明:{description}
                URL:{url}
                """

        blocks.append(block)

    # プロンプト設計
    prompt=""
    if topic:
        prompt = PROMPT_WITH_TOPIC.format(topic=topic)
    else:
        prompt = PROMPT_WITHOUT_TOPIC

    for block in blocks:
        prompt = f"{prompt}\n{block}"


    # 要約
    for attempt in range(3):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "openai/gpt-oss-120b:free",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"rate limit. wait for {4 ** attempt} seconds....")
                time.sleep(4 ** attempt)
                continue
            print(f"Error was:{e}")
            return None

        except Exception as e:
            print(f"Error was:{e}")

