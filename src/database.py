import sqlite3

def init_db() -> None :
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                topic TEXT,
                feed_url TEXT
                            );

            CREATE TABLE IF NOT EXISTS summaries (
                user_id TEXT PRIMARY KEY,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
        """)
        conn.commit()

    return None

def save_user(user_id, topic, feed_url) -> None :
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
            (user_id, topic, feed_url)
        )
        conn.commit()
    return None

def get_user(user_id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT topic, feed_url FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
    return row

def get_all_users():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, topic, feed_url FROM users")
        return cursor.fetchall()


def save_summary(user_id, summary) -> None:
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO summaries (user_id, summary) VALUES (?, ?)", (user_id, summary))
        conn.commit()
    return None

def get_summary(user_id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT summary FROM summaries WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
    return row[0] if row else None