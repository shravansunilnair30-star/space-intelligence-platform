import sqlite3
import os

# Detect environment
if os.name == "nt":  # Windows
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_DIR = os.path.join(BASE_DIR, "data")
    os.makedirs(DB_DIR, exist_ok=True)
    DB_PATH = os.path.join(DB_DIR, "space_news.db")
else:
    DB_PATH = "/tmp/space_news.db"  # Render/Linux


def connect_db():
    print("DB PATH:", DB_PATH)  # debug (you can remove later)
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles(
        title TEXT PRIMARY KEY,
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


def save_article(title, link, source, content, importance, topic, published):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO articles 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, link, source, content, importance, topic, published))

    conn.commit()
    conn.close()


def get_all_articles():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM articles")
    data = cursor.fetchall()

    conn.close()
    return data