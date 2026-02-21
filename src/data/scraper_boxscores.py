import pandas as pd
from curl_cffi import requests as requests_impersonate
from bs4 import BeautifulSoup
import time
import random
import re
from pathlib import Path
from src.utils.parseDate import parse_date

INPUT_FILE = Path(__file__).resolve().parents[2] / "data" / "interim" / "games_url.txt"
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "boxscores"
OUTPUT_CSV = OUTPUT_DIR / "all_boxscores_totals.csv"

def get_random_browser():
    """Retourne un user-agent aléatoire."""
    browser_version = [
        "chrome99", "chrome100", "chrome101", "chrome107", "chrome110",
        "chrome116", "chrome119", "chrome120", "chrome123", "chrome124",
        "edge99", "edge101",
        "safari15_3", "safari15_5", "safari17_0",
        "firefox133", "firefox135"
    ]
    return random.choice(browser_version)


def parse_boxscore(url, request_count, max_retries=3):
    """Extrait les 'Team Totals' d'une page de boxscore, avec retry sur erreurs 502/504."""
    for attempt in range(1, max_retries + 1):
        try:
            browser = get_random_browser()
            response = requests_impersonate.get(url, impersonate=browser, timeout=20)
            request_count += 1

            # Retry sur erreurs temporaires du serveur (gateway timeout/bad gateway)
            if response.status_code in (502, 504):
                wait = random.uniform(15, 30) * attempt
                print(f"Erreur HTTP {response.status_code} (tentative {attempt}/{max_retries}) — attente {wait:.0f}s : {url}")
                time.sleep(wait)
                continue  # réessayer

            if response.status_code != 200:
                print(f"Erreur HTTP {response.status_code} avec {browser} : {url}")
                return [], request_count

            # --- Parsing de la page ---
            soup = BeautifulSoup(response.content, "html.parser")

            h1 = soup.find('h1')
            game_date = None
            if h1:
                title_text = h1.text.strip()
                if ", " in title_text:
                    game_date = title_text.split(", ", 1)[1]  # "October 25, 2024"
                    game_date = parse_date(game_date)          # → "2024-10-25"

            # Trouver les tables de stats basiques (ex: id="box-LAL-game-basic")
            tables = soup.find_all('table', id=re.compile('box-.*-game-basic'))

            match_data = []

            for table in tables:
                table_id = table.get('id')
                team_code = table_id.split('-')[1]  # ex: 'LAL'

                thead = table.find('thead')
                headers = [th.text.strip() for th in thead.find_all('tr')[-1].find_all('th')][1:]

                tfoot = table.find('tfoot')
                if not tfoot:
                    continue

                footer_row = tfoot.find('tr')
                cells = footer_row.find_all('td')
                values = [td.text.strip() for td in cells]

                row_dict = {col: val for col, val in zip(headers, values)}
                row_dict['Team'] = team_code
                row_dict['Date'] = game_date

                match_data.append(row_dict)

            return match_data, request_count  # succès

        except Exception as e:
            print(f"Exception (tentative {attempt}/{max_retries}) sur {url} : {e}")
            if attempt < max_retries:
                wait = random.uniform(15, 30) * attempt
                print(f"Nouvelle tentative dans {wait:.0f}s...")
                time.sleep(wait)

    # Toutes les tentatives ont échoué
    print(f"URL abandonnée après {max_retries} tentatives : {url}")
    return [], request_count


def main():
    if not INPUT_FILE.exists():
        print(f"Fichier introuvable : {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    print(f"{len(urls)} matchs à traiter...")

    all_stats = []
    request_count = 0
    columns = ['MP', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB', 'TRB',
               'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Team', 'Date']

    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] Scraping : {url}")

        data, request_count = parse_boxscore(url, request_count)
        if data:
            all_stats.extend(data)

        # Pause respectueuse pour éviter le ban IP
        if request_count % 5 == 0:
            pause = random.uniform(25, 40)
        else:
            pause = random.uniform(8, 15)
        time.sleep(pause)

    if all_stats:
        final_df = pd.DataFrame(all_stats, columns=columns)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        final_df.to_csv(OUTPUT_CSV, index=False)
        print(f"Terminé ! Données sauvegardées dans : {OUTPUT_CSV}")
    else:
        print("Aucune donnée récupérée.")


if __name__ == "__main__":
    main()