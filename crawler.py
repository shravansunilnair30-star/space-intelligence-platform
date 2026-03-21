import feedparser

def get_articles(feeds):

    articles = []

    for url in feeds:
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:10]:
                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "source": url,
                    "published": entry.get("published", "")
                })

        except Exception as e:
            print("Error reading feed:", url, e)

    return articles