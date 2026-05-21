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

            CREATE TABLE IF NOT EXISTS articles(
                user_id TEXT,
                title TEXT,
                description TEXT,
                url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );
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

def save_articles(user_id, articles):
    (title, description, url) = articles
    with sqlite3.connect("articles.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?)",
            (user_id, title, description, url, timestamp)
        )
        conn.commit()
    return None

def get_articles(user_id):
    with sqlite3.connect("articles.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title, description, url FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = cursor.fetchall()
    return row