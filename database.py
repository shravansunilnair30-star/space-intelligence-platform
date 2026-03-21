import sqlite3
import os

# ✅ Correct DB path (IMPORTANT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "space_news.db")


def connect_db():
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles(
        title TEXT,
        link TEXT,
        source TEXT,
        content TEXT,
        importance TEXT,
        topic TEXT
    )
    """)

    conn.commit()
    conn.close()


def ensure_columns():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(articles)")
    columns = [col[1] for col in cursor.fetchall()]

    if "importance" not in columns:
        cursor.execute("ALTER TABLE articles ADD COLUMN importance TEXT")

    if "topic" not in columns:
        cursor.execute("ALTER TABLE articles ADD COLUMN topic TEXT")

    conn.commit()
    conn.close()


def article_exists(title):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM articles WHERE title=?", (title,))
    result = cursor.fetchone()

    conn.close()
    return result is not None


def save_article(title, link, source, content, importance, topic):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO articles VALUES (?, ?, ?, ?, ?, ?)",
        (title, link, source, content, importance, topic)
    )

    print("Inserted into DB:", title)  # 🔥 debug

    conn.commit()
    conn.close()