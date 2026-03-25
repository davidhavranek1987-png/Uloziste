# Monitoring a analýza českých zpráv

Tento projekt slouží jako technický základ pro monitoring obsahu v rámci přípravy antidezinformační kampaně.  
Automaticky stahuje články z veřejně dostupných českých zpravodajských webů (novinky.cz, idnes.cz, seznamzpravy.cz, ceskatelevize.cz), čistí a ukládá data do SQLite databáze, provádí základní analýzu obtížnosti textu a generuje HTML report s výsledky.

---

# Instalace

Vytvoř virtuální prostředí:
	python -m venv venv
	source venv/bin/activate  # WSL/Linux
Nainstaluj potřebné knihovny:
	pip install -r requirements.txt
	Ujisti se, že složky data/, analyza/, cisteni/, database/, hlaseni/, sber/ existují.

---

# Spuštění

Hlavní skript je main.py. Spouští se takto:
	python main.py
Po dokončení běhu vzniknou:
	data/articles.db – SQLite databáze článků
	report.html – statický HTML report s výsledky analýzy
Otevření reportu ve Windows:
	explorer.exe report.html

---

# Použité technologie

- **Python 3.12**  
- **Knihovny:**  
  - `feedparser` – čtení RSS a Atom feedů  
  - `selectolax` – rychlý HTML parser  
  - `polars` – práce s tabulkami a výpočty  
  - `httpx` – HTTP požadavky  
  - `jinja2` – generování HTML reportu  

---

# Struktura projektu

kyber-projekt/
├── config.py 		# Konfigurace projektu (zdroje, databáze, limity)
├── sber/
│ └── sber.py 		# sběr článků z RSS
├── cisteni/
│ └── cisteni.py 	# Čištění a deduplikace článků
├── database/
│ └── database.py 	# Funkce pro vytvoření a zápis do databáze
├── data/ 			# Databázový soubor
├── analyza/
│ └── analyza.py 	# Analýza textu článků
├── hlaseni/
│ └── hlaseni.py 	# Generování HTML reportu
└── main.py 		# Hlavní spustitelný skript (entrypoint)

---

# Workflow aplikace

Sběr dat (sber/sber.py)
	Stahuje články z veřejně dostupných RSS feedů
	U každého článku ukládá: zdroj, URL, titulek, datum publikace, autora (pokud je uveden), rubriku, plný text
Čištění a deduplikace (cisteni/cisteni.py)
	Odstranění HTML balastu a nadbytečných mezer
	Odstranění duplicitních článků
Uložení do databáze (database/database.py)
	Vytvoření SQLite databáze
	Zápis všech článků do tabulky articles
Analýza textu (analyza/analyza.py)
	Výpočet základních jazykových charakteristik:
	průměrná délka vět
	průměrná délka slov
	podíl dlouhých slov (6+ znaků)
	poměr unikátních slov k celkovému počtu slov
	Výpočet skóre obtížnosti textu
Generování reportu (hlaseni/hlaseni.py)
	Vytvoření HTML tabulky s výsledky analýzy
	Možnost srovnání zdrojů a zobrazení článků s nejvyšším skóre

---

# Struktura databáze

Tabulka articles:

Sloupec	Typ						Popis
id		INTEGER PRIMARY KEY		Jedinečný identifikátor
source	TEXT					RSS zdroj
url		TEXT UNIQUE				URL článku
title	TEXT					Titulek článku
date	TEXT					Datum publikace
author	TEXT					Autor článku
section	TEXT					Rubrika článku
text	TEXT					Plný text článku