import feedparser

def get_articles(feeds):

    articles = []

    for url in feeds:
        print("Reading feed:", url)   #  DEBUG

        try:
            feed = feedparser.parse(url)

            print("Entries found:", len(feed.entries))  #  DEBUG

            for entry in feed.entries[:10]:
                print("Found article:", entry.title)   #  DEBUG

                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": url
                })

        except Exception as e:
            print("Error reading feed:", url, e)

    return articles