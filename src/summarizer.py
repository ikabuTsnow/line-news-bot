from dotenv import load_dotenv
import requests
import time
import os

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def summarize(articles: list[dict], topic: str) -> str:

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

    # プロンプトの整形
    prompt = """
    以下のニュース記事を読んで、各記事を指定のフォーマットで出力してください。

    [出力フォーマット]
    タイトル
    要約(50~150字の要約文)
    URL

    ※各記事の間には空行を入れてください
    ※LINEでのメッセージを意識してください
    ※フォーマット以外の文章は出力しないでください
    ※要約はニュースの要点を押さえ、ですます調にし、読者が読みたくなるように書いてください

    [記事データ]
    """

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