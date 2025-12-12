# Script de scraping pour récupérer les URLs des box scores NBA
# Récupère l'url du box score de chaque match
# On va boucler sur tout les matchs d'octobre à fevrier

from bs4 import BeautifulSoup
import re
import random
import os
import time
from curl_cffi import requests as requests_impersonate


def safe_scraper():
    """
    Configure un scraper sécurisé en simulant différents navigateurs.
    Retourne une fonction qui choisit aléatoirement un navigateur pour éviter la détection.
    """
    # Liste des versions de navigateurs disponibles pour l'impersonation
    # Permet de varier les user-agents et contourner les protections anti-bot
    browser_version = [
        "chrome99", "chrome100", "chrome101", "chrome104", "chrome107", "chrome110", "chrome116", "chrome119", "chrome120", "chrome123", "chrome124", "chrome131", "chrome133a", "chrome136",

        "safari153", "safari155", "safari170", "safari180", "safari184", "safari260",

        "firefox133", "firefox135"
    ]


    def get_browser():
        """Sélectionne aléatoirement un navigateur dans la liste"""        
        return random.choice(browser_version)
       
    # Retourne la fonction pour utilisation ultérieure    
    return get_browser


def scraping():
    """
    Parcourt les pages de basketball-reference.com pour récupérer tous les liens
    des box scores des matchs NBA entre octobre et février.
    
    Returns:
        list: Liste contenant toutes les URLs des box scores trouvées
    """

    # Mois de la saison NBA (octobre à février)    
    months = [10, 11, 12, 1, 2]
    
    # URL de base du site basketball-reference.com
    base_url = "https://www.basketball-reference.com/boxscores"
    
    # Année de début de saison    
    season = "2024"

    # Liste qui stockera toutes les URLs des matchs
    games_url = []


    # Récupère la fonction de sélection de navigateur
    get_browser = safe_scraper()

    # Compteur pour gérer les pauses entre requêtes
    request_count = 0

    # Boucle sur chaque mois de la saison
    for month in months:
        # Boucle sur chaque jour du mois (1 à 31)
        for day in range(1,32):
            
            # Construction de l'URL pour un jour spécifique
            url = f"{base_url}/?month={month}&day={day}&year={season}"
            # example lien voulu https://www.basketball-reference.com/boxscores/?month=10&day=22&year=2024
            
            print(url)

            # Sélectionne un navigateur aléatoire pour cette requête
            browser = get_browser()

            try:
                # Effectue la requête HTTP en imitant le navigateur choisi
                # timeout=15 : abandon après 15 secondes sans réponse
                response = requests_impersonate.get(url, impersonate=browser, timeout=15)
                
                # Incrémente le compteur de requêtes
                request_count += 1

                # Vérifie si la requête a réussi (code 200 = OK)
                if response.status_code == 200:
                    # Parse le contenu HTML de la page avec BeautifulSoup
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Recherche tous les liens <a> contenant le texte "Box Score"
                    # href=True : ne garde que les balises avec attribut href
                    links = soup.find_all(name="a", href=True,string=re.compile("Box Score"))


                    # Parcourt chaque lien trouvé
                    for link in links:#[1:-1]: # links[1:-1] car links[1] = links[-1] = "https://www.basketball-reference.com/boxscores/" donc pas besoin
                        
                        # Vérifie que le lien est bien un box score (commence par /boxscores/ et finit par .html)                    
                        if link['href'].startswith('/boxscores/') and link['href'].endswith('.html'):
                            
                            # Construit l'URL complète du box score
                            game_url = "https://www.basketball-reference.com" + link['href']
                            print(game_url)
                            
                            # Ajoute l'URL à la liste
                            games_url.append(game_url)    
                    
        
                # Gestion des pauses pour éviter de surcharger le serveur
                # PAUSE LONGUE TOUTES LES 5 REQUÊTES
                if request_count % 5 == 0:
                    # Pause aléatoire de 25 à 40 secondes toutes les 5 requêtes
                    pause_longue = random.uniform(25, 40)
                    time.sleep(pause_longue)
                else:
                    # Pause courte de 8 à 15 secondes entre chaque requête normale
                    pause_courte = random.uniform(8, 15)
                    time.sleep(pause_courte)
            
            except Exception as e:
                # Capture toutes les erreurs (timeout, connexion, etc.)
                print("Erreur lors du scraping")

    # Retourne la liste complète des URLs collectées
    return games_url



def save_url():
    """
    Exécute le scraping et sauvegarde toutes les URLs récupérées dans un fichier texte.
    Crée l'arborescence de dossiers nécessaire si elle n'existe pas.
    """
    try:
        games_url = scraping()
        ## Probleme de chemin
        #chemin = os.path.join("./../data/raw", "games_url.txt")

        # __file__ = chemin du fichier .py actuel
        # Exemple: "/home/user/projet/src/recup_boxscore.py"

        script_dir = os.path.dirname(__file__)
        # → "/home/user/projet/src"

        data_dir = os.path.join(script_dir, "..", "..", "data", "interim")
        # → "/home/user/projet/src/../data/raw"
        # ".." = remonter d'un dossier → "/home/user/projet/data/raw"

        chemin = os.path.join(data_dir, "games_url.txt")
        # → "/home/user/projet/data/raw/games_url.txt"

        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        # os.path.dirname(chemin) = "/home/user/projet/data/raw"
        # Crée les dossiers "data" et "raw" si ils existent pas

        print(f"taille de games_url : {len(games_url)}")

        with open(chemin, "w", encoding="utf-8") as f:
            # Écrit chaque URL sur une ligne séparée
            for i, url in enumerate(games_url):
                f.write(url+"\n")
                # Affiche la progression de la sauvegarde
                print(f"URLs sauvegardées: {i+1}")
    except Exception as e:
        # Gère les erreurs potentielles lors de la sauvegarde
        print("Impossible de sauvegarder le lien") 


# Point d'entrée du script : exécute la fonction de sauvegarde
save_url()