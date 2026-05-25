import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def init_db() -> None :
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                topic TEXT,
                feed_url TEXT
                            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS summaries (
                user_id TEXT PRIMARY KEY,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
        """)
        conn.commit()

    return None

def save_user(user_id, topic, feed_url) -> None :
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, topic, feed_url) VALUES (%s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET topic=%s, feed_url=%s
        """,
        (user_id, topic, feed_url, topic, feed_url))
        conn.commit()
    return None

def get_user(user_id):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT topic, feed_url FROM users WHERE user_id = %s",
            (user_id,)
        )
        row = cursor.fetchone()
    return row

def get_all_users():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, topic, feed_url FROM users")
        return cursor.fetchall()


def save_summary(user_id, summary) -> None:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO summaries (user_id, summary) VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE SET summary=%s
        """,
        (user_id, summary, summary))
        conn.commit()
    return None

def get_summary(user_id):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT summary FROM summaries WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
    return row[0] if row else None