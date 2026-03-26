import os

from crawler import get_articles
from notifier import send_message
from database import create_table, save_article
from analyzer import get_importance, generate_insight, classify_topic


# -------------------------------
# RSS FEEDS
# -------------------------------
feeds = [
    "https://spacenews.com/feed/",
    "https://www.nasaspaceflight.com/feed/",
    "https://www.universetoday.com/feed/",
    "https://www.space.com/feeds/all",
    "https://blogs.nasa.gov/rss/",
    "https://www.esa.int/rssfeed/Our_Activities",
]


# -------------------------------
# CORE FUNCTION
# -------------------------------
def run_once():
    print("\n🔄 Running update...")

    try:
        articles = get_articles(feeds)
        print("Articles found:", len(articles))

        new_count = 0

        for article in articles:

            title = article.get("title", "")
            link = article.get("link", "")
            source = article.get("source", "")
            published = article.get("published", "")

            if not title:
                continue

            # No existence check needed anymore ✅
            text = title  # (replace later if you fetch full content)

            importance = get_importance(title)
            topic = classify_topic(title)
            insight = generate_insight(title)

            if importance == "HIGH":
                message = f"""
🚀 SPACE UPDATE

📰 {title}
📅 {published}

📊 Topic: {topic}

🧠 Insight:
{insight}

🔗 {link}
"""
                send_message(message)

            save_article(title, link, source, text, importance, topic, published)
            new_count += 1

        print(f"✅ Added {new_count} new articles")
        return new_count

    except Exception as e:
        print("❌ Error:", e)
        return 0


# -------------------------------
# INIT
# -------------------------------
create_table()


if __name__ == "__main__":
    run_once()