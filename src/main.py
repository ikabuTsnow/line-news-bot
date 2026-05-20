from news_fetcher import fetch_news
from summarizer import summarize
from line_sender import push_message

def main():
    newses = fetch_news("https://rss.asahi.com/rss/asahi/newsheadlines.rdf")
    res = summarize(newses, "")
    print(res)
    return 0

if __name__ == "__main__":
    main()