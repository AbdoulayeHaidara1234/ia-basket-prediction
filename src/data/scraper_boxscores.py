import pandas as pd
from curl_cffi import requests as requests_impersonate
from bs4 import BeautifulSoup
import time
import random
import re
from pathlib import Path

# --- CONFIGURATION ---
INPUT_FILE = Path(__file__).resolve().parents[2] / "data" / "interim" / "games_url.txt"
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "boxscores"
OUTPUT_CSV = OUTPUT_DIR / "all_boxscores_totals.csv"

def get_random_browser():
    """Retourne un user-agent aléatoire."""

    browser_version = [
        "chrome99", "chrome100", "chrome101", "chrome107", "chrome110", "chrome116", "chrome119", "chrome120", "chrome123", "chrome124",

        "edge99", "edge101",
        
        "safari15_3", "safari15_5", "safari17_0",

        "firefox133", "firefox135"
    ]
    
    return random.choice(browser_version)

def parse_boxscore(url, request_count):
    """Extrait les 'Team Totals' d'une page de boxscore."""
    try:
        browser = get_random_browser()
        response = requests_impersonate.get(url, impersonate=browser, timeout=20)
        request_count += 1
        
        if response.status_code != 200:
            print(f"Erreur HTTP {response.status_code} avec {browser} : {url}")
            return  [], request_count

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Trouver les tables de stats basiques (ex: id="box-LAL-game-basic")
        tables = soup.find_all('table', id=re.compile('box-.*-game-basic'))
        
        match_data = []
        
        for table in tables:
            # Extraction du nom de l'équipe depuis l'ID de la table
            table_id = table.get('id')
            team_code = table_id.split('-')[1] # ex: 'LAL'
            
            # Extraction des headers (MP, FG, FGA...)
            thead = table.find('thead')
            headers = [th.text.strip() for th in thead.find_all('tr')[-1].find_all('th')][1:] # On ignore le 1er header vide
            
            # Extraction du Footer (Team Totals)
            tfoot = table.find('tfoot')
            if not tfoot:
                continue
                
            footer_row = tfoot.find('tr')
            cells = footer_row.find_all('td')
            values = [td.text.strip() for td in cells]
            
            # Création d'un dictionnaire pour cette équipe
            row_dict = {col: val for col, val in zip(headers, values)}
            row_dict['Team'] = team_code
            
            
            match_data.append(row_dict)
            
        return match_data, request_count

    except Exception as e:
        print(f"Exception sur {url} : {e}")
        return None

def main():
    # Vérification de l'existence du fichier d'entrée
    if not INPUT_FILE.exists():
        print(f"Fichier introuvable : {INPUT_FILE}")
        return

    # Chargement des URLs
    with open(INPUT_FILE, "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    print(f"{len(urls)} matchs à traiter...")


    all_stats = []

    request_count = 0

    columns = ['MP', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Team']
    
    # Boucle de scraping
    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] Scraping : {url}")

        data, request_count = parse_boxscore(url, request_count)
        if data:
            all_stats.extend(data)
        
         # Pause respectueuse pour éviter le ban IP
        if request_count % 5 == 0:
        # Pause aléatoire de 25 à 40 secondes toutes les 5 requêtes
            pause_longue = random.uniform(25, 40)
            time.sleep(pause_longue)
        else:
        # Pause courte de 8 à 15 secondes entre chaque requête normale
            pause_courte = random.uniform(8, 15)
            time.sleep(pause_courte)

    # Sauvegarde finale
    if all_stats:
        final_df = pd.DataFrame(all_stats, columns=columns)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        final_df.to_csv(OUTPUT_CSV, index=False)
        print(f"Terminé ! Données sauvegardées dans : {OUTPUT_CSV}")
    else:
        print("Aucune donnée récupérée.")

if __name__ == "__main__":
    main()