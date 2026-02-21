import os
import time
import random
import re
from pathlib import Path
from bs4 import BeautifulSoup
from curl_cffi import requests as requests_impersonate

SEASON = "2024"  # Adaptation à la saison actuelle ou cible
BASE_URL = "https://www.basketball-reference.com/boxscores"
OUTPUT_FILE = Path(__file__).resolve().parents[2] / "data" / "interim" / "games_url.txt"

def get_random_browser():
    """Retourne une version de navigateur aléatoire pour éviter le blocage."""
    browser_versions = [
        "chrome99", "chrome100", "chrome101", "chrome107", "chrome110", "chrome116", "chrome119", "chrome120", "chrome123", "chrome124",

        "edge99", "edge101"
        
        "safari15_3", "safari15_5", "safari17_0",

        "firefox133", "firefox135"
    ]
    return random.choice(browser_versions)

def fetch_game_urls():
    """Récupère les URLs de tous les boxscores de la saison."""
    months = [10, 11, 12, 1, 2] # Saison régulière typique
    games_url = []
    request_count = 0

    for month in months:
        # On ne traite que les jours pertinents
        for day in range(1, 32):
            url = f"{BASE_URL}/?month={month}&day={day}&year={SEASON}"
            print(f"{url}")

            if month == 12 and day == 17:
                continue

            try:
                browser = get_random_browser()
                response = requests_impersonate.get(url, impersonate=browser, timeout=20)

                request_count += 1

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    links = soup.find_all("a", href=True, string=re.compile("Box Score"))

                    for link in links:
                        href = link['href']
                        if href.startswith('/boxscores/') and href.endswith('.html'):
                            full_url = f"https://www.basketball-reference.com{href}"
                            games_url.append(full_url)
                            print(f"{full_url}")

                # Pause respectueuse pour éviter le ban IP
                if request_count % 5 == 0:
                    # Pause aléatoire de 25 à 40 secondes toutes les 5 requêtes
                    pause_longue = random.uniform(25, 40)
                    time.sleep(pause_longue)
                else:
                    # Pause courte de 8 à 15 secondes entre chaque requête normale
                    pause_courte = random.uniform(8, 15)
                    time.sleep(pause_courte)

            except Exception as e:
                print(f"Erreur sur {url}: {e}")

    return games_url

def save_urls(urls):
    """Sauvegarde les URLs dans le fichier cible."""
    # Création du dossier parent si inexistant
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")
    
    print(f"\n{len(urls)} URLs sauvegardées dans :")
    print(OUTPUT_FILE)

if __name__ == "__main__":
    urls = fetch_game_urls()
    save_urls(urls)