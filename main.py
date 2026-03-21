import time
import schedule
import sqlite3
import pandas as pd
import os

from crawler import get_articles
from notifier import send_message
from database import create_table, ensure_columns, article_exists, save_article
from analyzer import get_importance, generate_insight, classify_topic
from reporter import generate_daily_report


# ✅ FIXED DATABASE PATH (IMPORTANT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "space_news.db")


feeds = [
    "https://spacenews.com/feed/",
    "https://www.nasaspaceflight.com/feed/",
    "https://www.universetoday.com/feed/",
    "https://www.space.com/feeds/all",
    "https://blogs.nasa.gov/rss/",
    "https://www.esa.int/rssfeed/Our_Activities",
]


def run_agent():
    print("Checking space news...")

    articles = get_articles(feeds)
    print("Articles found:", len(articles))

    for article in articles:

        title = article["title"]
        link = article["link"]
        source = article["source"]

        print("Processing:", title)

        # 🔥 TEMP FORCE SAVE (change back later)
        if True:

            print("Saving article:", title)
            print("Inserted:", title)

            text = title

            # AI layer
            importance = get_importance(title)
            topic = classify_topic(title)

            print("Importance:", importance)
            print("Topic:", topic)

            if importance == "HIGH":

                insight = generate_insight(title)

                message = f"""
🚀 SPACE INTELLIGENCE ALERT

📰 {title}

📊 Topic: {topic}

🧠 Insight:
{insight}

🔗 Source:
{link}
"""

                send_message(message)

            # Save to DB
            save_article(title, link, source, text, importance, topic)


# 🔥 Daily report
def send_daily_report():
    print("Sending daily report...")

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM articles", conn)

    report = generate_daily_report(df)

    send_message(report)


# Setup DB
create_table()
ensure_columns()

# Run once
run_agent()

# Schedule
schedule.every(5).minutes.do(run_agent)
schedule.every().day.at("09:00").do(send_daily_report)

# Loop
while True:
    schedule.run_pending()
    time.sleep(1)