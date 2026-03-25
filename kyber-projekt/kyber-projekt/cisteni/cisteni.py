import re

def vycisti_text(text):
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def odstran_duplicity(articles):
    seen = set()
    unique = []
    for article in articles:
        if article["url"] not in seen:
            unique.append(article)
            seen.add(article["url"])
    return unique