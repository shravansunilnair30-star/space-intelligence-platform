import sqlite3

DB_PATH = "/tmp/space_news.db"   # 🔥 FORCE THIS


def connect_db():
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