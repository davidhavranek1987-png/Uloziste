import sqlite3
from config import DATABASE_PATH

def vytvor_databazi():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        source TEXT,
        url TEXT UNIQUE,
        title TEXT,
        date TEXT,
        author TEXT,
        section TEXT,
        text TEXT
    )
    """)
    conn.commit()
    conn.close()

def uloz_clanky(articles):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    for article in articles:
        cursor.execute("""
        INSERT OR IGNORE INTO articles
        (source, url, title, date, author, section, text)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            article["source"],
            article["url"],
            article["title"],
            article["date"],
            article["author"],
            article["section"],
            article["text"]
        ))
    conn.commit()
    conn.close()