FEED_URLS = {
    "朝日新聞": "https://rss.asahi.com/rss/asahi/newsheadlines.rdf",
    "NHK": "https://www.nhk.or.jp/rss/news/cat0.xml",
    "ITmedia": "https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml",
    "Impress Watch": "https://www.watch.impress.co.jp/data/rss/1.0/ipw/feed.rdf"
}

DEFAULT_TOPIC = "AI technology"
DEFAULT_FEED_URL = "https://rss.asahi.com/rss/asahi/newsheadlines.rdf"

PROMPT_WITH_TOPIC = """
以下は複数のニュース記事です。
次の優先順位で5件を選び、それぞれを以下のフォーマットで出力してください。

[選択の優先順位]
1. 「{topic}」に関連度が高い記事
2. 今注目すべき重要なニュース
3. 上記で5件に満たない場合は他の記事で埋める

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
以下のニュース記事を読んで、各記事を指定のフォーマットで５件出力してください。

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