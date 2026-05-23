FEED_URLS = {
    "朝日新聞": "https://rss.asahi.com/rss/asahi/newsheadlines.rdf",
    "NHK": "https://www.nhk.or.jp/rss/news/cat0.xml",
    "TechCrunch": "https://jp.techcrunch.com/feed/",
}

TOPICS = {
    "AI": "AI technology",
    "スポーツ": "sports",
    "経済": "economy",
}

DEFAULT_TOPIC = "AI technology"
DEFAULT_FEED_URL = "https://rss.asahi.com/rss/asahi/newsheadlines.rdf"

PROMPT_WITH_TOPIC = """
以下は複数のニュース記事です。
この中から「{topic}」に関連する記事を5件選び、
それぞれを以下のフォーマットで出力してください。

[出力フォーマット]
タイトル...
要約...
URL...


※各記事の間には空行を入れてください
※LINEでのメッセージを意識してください
※フォーマット以外の文章は出力しないでください
※要約はニュースの要点を押さえ、ですます調にし、読者が読みたくなるように書いてください

[記事データ]
"""

PROMPT_WITHOUT_TOPIC = """
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