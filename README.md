line-news-bot/
├── .github/workflows/daily_news.yml
├── src/
│   ├── main.py          # エントリーポイント
│   ├── news_fetcher.py  # NewsAPI からニュース取得
│   ├── summarizer.py    # Claude で要約（ここが腕の見せ所）
│   └── line_sender.py   # LINE に送信
├── requirements.txt
└── .env.example