from sber.sber import sber_clanku
from cisteni.cisteni import vycisti_text, odstran_duplicity
from database.database import vytvor_databazi, uloz_clanky
from analyza.analyza import analyzuj_databazi
from hlaseni.hlaseni import generuj_html

def main():
    print("Sběr článků...")
    articles = sber_clanku()
    print("Čištění textu...")
    for article in articles:
        article["text"] = vycisti_text(article["text"])
    articles = odstran_duplicity(articles)
    print("Ukládání do databáze...")
    vytvor_databazi()
    uloz_clanky(articles)
    print("Analýza textu...")
    results = analyzuj_databazi()
    print("Generování HTML reportu...")
    generuj_html(results)
    print("Hotovo!")

if __name__ == "__main__":
    main()