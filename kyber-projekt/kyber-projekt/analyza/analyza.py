import sqlite3
import re
import polars as pl
from config import DATABASE_PATH


def rozdel_vety(text):
    return re.split(r"[.!?]", text)

def rozdel_slova(text):
    return re.findall(r"\w+", text)


def analyzuj_text(text):
    sentences = rozdel_vety(text)
    words = rozdel_slova(text)
    if len(sentences) == 0 or len(words) == 0:
        return None
    avg_sentence_length = len(words) / len(sentences)
    avg_word_length = sum(len(w) for w in words) / len(words)
    long_words = [w for w in words if len(w) >= 6]
    long_word_ratio = len(long_words) / len(words)
    unique_ratio = len(set(words)) / len(words)

    score = (
        avg_sentence_length * 0.4 +
        avg_word_length * 0.3 +
        long_word_ratio * 10 * 0.2 +
        unique_ratio * 10 * 0.1
    )

    return {
        "avg_sentence_length": avg_sentence_length,
        "avg_word_length": avg_word_length,
        "long_word_ratio": long_word_ratio,
        "unique_ratio": unique_ratio,
        "score": score
    }


def analyzuj_databazi():
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute("SELECT title, text, date FROM articles").fetchall()
    results = []
    for title, text, date in rows:
        metrics = analyzuj_text(text)
        if metrics:
            metrics["title"] = title
            metrics["date"] = date
            results.append(metrics)
    conn.close()
    return pl.DataFrame(results)