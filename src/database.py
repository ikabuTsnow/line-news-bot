import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def init_db() -> None:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                topic TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS summaries (
                user_id TEXT PRIMARY KEY,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quizzes (
                user_id TEXT PRIMARY KEY,
                question TEXT,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    return None

def save_user(user_id, topic) -> None:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, topic) VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE SET topic=%s
        """, (user_id, topic, topic))
        conn.commit()
    return None

def get_user(user_id):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT topic FROM users WHERE user_id = %s",
            (user_id,)
        )
        row = cursor.fetchone()
    return row

def get_all_users():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, topic FROM users")
        return cursor.fetchall()

def save_summary(user_id, summary) -> None:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO summaries (user_id, summary) VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE SET summary=%s
        """, (user_id, summary, summary))
        conn.commit()
    return None

def get_summary(user_id):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT summary FROM summaries WHERE user_id = %s",
            (user_id,)
        )
        row = cursor.fetchone()
    return row[0] if row else None

def save_quiz(user_id, question, answer) -> None:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO quizzes (user_id, question, answer) VALUES (%s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET question=%s, answer=%s
        """, (user_id, question, answer, question, answer))
        conn.commit()
    return None

def get_quiz(user_id):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT question, answer FROM quizzes WHERE user_id = %s",
            (user_id,)
        )
        row = cursor.fetchone()
    return row if row else None