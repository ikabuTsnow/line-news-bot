from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def summarize(articles: list[dict], topic: str) -> str:
    # ニュースの読み取り
    blocks = []
    for article in articles:
        title = article["title"]
        description = article["description"]

        block = f"""
                タイトル:{title}
                説明:{description}
                """

        blocks.append(block)

    # プロンプトの整形
    prompt="""
    ニュースの記事を以下のフォーマットで提供します。
    ニュースの要点、読者が読みたくなるものを意識して、50~150字で要約文章を作成してください。
    
    [記事のフォーマット]
    タイトル：タイトル
    説明：その記事の説明
    """

    for block in blocks:
        prompt = f"{prompt}\n{block}"

    # 要約
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text