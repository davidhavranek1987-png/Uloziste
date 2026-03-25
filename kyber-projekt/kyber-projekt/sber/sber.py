import httpx
import feedparser
import time
from selectolax.parser import HTMLParser
from config import RSS_FEEDS, REQUEST_DELAY, MAX_ARTICLES
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

def povoleno_robots(url, user_agent="*"):
    """Zkontroluje, zda můžeme stáhnout danou URL podle robots.txt"""
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(base_url)
    try:
        rp.read()
    except Exception:
        return True
    return rp.can_fetch(user_agent, url)

def stahni_clanek(url):
    try:
        response = httpx.get(url, timeout=10)
        html = HTMLParser(response.text)
        paragraphs = html.css("p")
        text_parts = []
        for p in paragraphs:
            text_parts.append(p.text())
        text = " ".join(text_parts)
        return text
    except Exception:
        return ""

def sber_clanku():
    articles = []
    for feed_url in RSS_FEEDS:
        response = httpx.get(feed_url)
        try:
            feed = feedparser.parse(response.text)
        except Exception:
            print(f"Nelze parsovat RSS feed: {feed_url}")
            continue
        for entry in feed.entries:
            if len(articles) >= MAX_ARTICLES:
                return articles
            url = entry.get("link", "")
            title = entry.get("title", "")
            date = entry.get("published", "")
            author = entry.get("author", "")
            section = ""
            if povoleno_robots(url):
                text = stahni_clanek(url)
            else:
                print(f"Stahování zakázáno robots.txt: {url}")
                text = ""
            article = {
                "source": feed_url,
                "url": url,
                "title": title,
                "date": str(date),
                "author": author,
                "section": section,
                "text": text
            }
            articles.append(article)
            time.sleep(REQUEST_DELAY)
    return articles