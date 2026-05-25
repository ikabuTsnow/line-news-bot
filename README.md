# 📰 新聞配達員 - LINE ニュースボット

毎朝指定したニュースソースから記事を取得し、AIで要約してLINEに届けるボットです。

---

## 概要

ユーザーがLINEのリッチメニューからニュースソースを選択し、チャットでトピックを指定すると、毎朝そのユーザーに合わせたニュースが届きます。

## 機能

- **毎朝自動配信** — 毎朝6:50にニュースを取得・要約し、7:00にLINEへ送信
- **ニュースソース選択** — リッチメニューから朝日新聞・NHK・ITmedia・Impress Watchを選択
- **トピック指定** — チャットで自由にトピックを指定（例：「野球」「AI」「政治」）
- **即時配信** — 「ニュース！」と送るとその場でニュースを取得して送信
- **複数ユーザー対応** — 友達追加したユーザーごとに設定を管理

## 技術スタック

| カテゴリ | 技術 |
|---|---|
| バックエンド | Python / Flask |
| データベース | PostgreSQL |
| スケジューラー | APScheduler |
| ニュース取得 | feedparser（RSSフィード） |
| AI要約 | OpenRouter API（GPT-OSS-120B） |
| メッセージ配信 | LINE Messaging API |
| デプロイ | Render |

## システム構成

```
ユーザー（LINE）
    ↓ メッセージ送信
Flask（Webhook受信）
    ↓ ユーザー設定を保存
PostgreSQL
    ↑ 毎朝6:50
APScheduler
    ↓ RSSフィードから記事取得
feedparser
    ↓ AIで要約・絞り込み
OpenRouter API
    ↓ 毎朝7:00
LINE Messaging API
    ↓
ユーザー（LINE）
```

## ファイル構成

```
line-news-bot/
├── src/
│   ├── main.py          # Flaskサーバー・エントリーポイント
│   ├── config.py        # 設定・定数・プロンプト管理
│   ├── database.py      # PostgreSQL操作
│   ├── scheduler.py     # 定時実行ジョブ
│   ├── news_fetcher.py  # RSSフィードからニュース取得
│   ├── summarizer.py    # OpenRouter APIで要約
│   ├── line_sender.py   # LINE Messaging API送信
│   └── rich_menu.py     # リッチメニュー自動生成
├── .env.example
├── requirements.txt
└── Procfile
```

## セットアップ

### 必要なもの

| サービス | 用途 |
|---|---|
| [LINE Developers](https://developers.line.biz/) | Messaging APIチャネル |
| [OpenRouter](https://openrouter.ai/) | AI要約API |
| [Render](https://render.com/) | デプロイ・PostgreSQL |

### 環境変数

```
LINE_CHANNEL_ACCESS_TOKEN=your_token
USER_ID=your_line_user_id
OPENROUTER_API_KEY=your_api_key
DATABASE_URL=your_postgresql_url
```

### ローカル実行

```bash
git clone https://github.com/yourname/line-news-bot
cd line-news-bot
pip install -r requirements.txt
cp .env.example .env
# .envに各キーを入力
python src/main.py
```

## 工夫した点

- **取得と送信を分離** — 6:50に記事取得・要約、7:00に送信することでAPIエラー時の影響を最小化
- **AIによる関連記事の絞り込み** — 単純なキーワード一致ではなくLLMが文脈で関連度を判断
- **リッチメニューの自動生成** — Pillowで画像を自動生成してLINE APIでアップロード
- **SQLインジェクション対策** — プレースホルダー（`%s`）を使用
- **複数ユーザー対応** — PostgreSQLでユーザーごとの設定を永続管理