
import requests
import json
import os
from dotenv import load_dotenv
from prompts import PROMPT_GENERATE_QUIZ

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def generate_quiz(articles: list[dict]) -> dict:
    # articlesをテキストに変換してプロンプトに渡す
    articles_text = ""
    for article in articles:
        articles_text += f"タイトル: {article['title']}\n説明: {article['description']}\n\n"
    
    prompt = PROMPT_GENERATE_QUIZ.format(articles=articles_text)
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
        content = response.json()["choices"][0]["message"]["content"]
        # コードブロックを除去
        content = content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]

        try:
            data = json.loads(content)
            return data
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"content: {content}")
            return None
    except requests.RequestException as e:
        print(f"Error was: {e}")
        return None
