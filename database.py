import sqlite3
import os

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
        topic TEXT,
        published TEXT
    )
    """)

    conn.commit()
    conn.close()


def article_exists(title):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM articles WHERE title=?", (title,))
    result = cursor.fetchone()

    conn.close()
    return result is not None


def save_article(title, link, source, content, importance, topic, published):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO articles VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, link, source, content, importance, topic, published)
    )

    conn.commit()
    conn.close()