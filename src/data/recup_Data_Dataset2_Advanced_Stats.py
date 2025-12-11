import os
import pandas as pd
from curl_cffi import requests as requests_impersonate
from bs4 import BeautifulSoup
import random
import re

def get_path_file():
    """Retourne le chemin vers le dossier de données."""
    script_dir = os.path.dirname(__file__)
    path_file = os.path.join(script_dir, "..", "data", "raw", "games_url.txt")
    return path_file

team_name = []

team_stats = []

browser_version = [
        "chrome99", "chrome100", "chrome101", "chrome104", "chrome107", "chrome110", "chrome116", "chrome119", "chrome120", "chrome123", "chrome124", "chrome131", "chrome133a", "chrome136",

        "safari153", "safari155", "safari170", "safari180", "safari184", "safari260",

        "firefox133", "firefox135"
    ]




path_file = get_path_file()

print(path_file)

with open(path_file, "r") as f:
    """for url in f:
        random_browser = random.choice(browser_version)

        try: 
            response = requests_impersonate(url, impersonate=random_browser, timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

            team_name = soup.findAll(name="h2", string=re.compile("Basic and Advanced Stats"))
        
        except Exception as e:
            print("Erreur")"""
    url = f.readline()
    print(url[-1])

    response = requests_impersonate.get(url[:-1], impersonate="chrome101", timeout=15)   

    

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")


        # 1. Trouver toutes les tables qui finissent par "-game-basic"
        # Cela permet de trouver NYK et BOS sans connaître les noms à l'avance
        tables = soup.find_all('table', id=re.compile('box-.*-game-basic'))

        data_result = []

        list_df = []

        for table in tables:
            # Récupérer le nom de l'équipe depuis l'ID (ex: box-NYK-game-basic -> NYK)
            table_id = table.get('id')
            team_name = table_id.split('-')[1]
    
            # --- Récupération des En-têtes (Headers) ---
            # On cherche la dernière ligne du thead pour avoir les vrais noms de colonnes (MP, FG, FGA...)
            thead = table.find('thead')
            header_row = thead.find_all('tr')[-1] # La dernière ligne contient les titres exacts
            headers = [th.text.strip() for th in header_row.find_all('th')]
    
            # --- Récupération du Footer (Team Totals) ---
            tfoot = table.find('tfoot')
            if tfoot:
                footer_row = tfoot.find('tr')
        
                # Le premier élément est souvent le titre "Team Totals" (dans un th)
                first_th = footer_row.find('th').text.strip()
        
                # Les données sont dans les td
                cells = footer_row.find_all('td')
                values = [td.text.strip() for td in cells]
        
                # On combine tout : [Nom Equipe, Team Totals, 240, 43, ...]
                full_row = [team_name, first_th] + values
        
                data_result.append(full_row)

     
        
                # Affichage propre pour vérification
                print(f"--- Stats pour {team_name} ---")
                # On saute la première colonne header ('Starters/Reserves') pour l'alignement
                col_names = headers[1:] 
                for col, val in zip(col_names, values):
                    print(f"{col}: {val}")
                print("\n")


                # mettre val entre [] sinon pd.DataFrame ne fonctionne pas
                dico = {col : [val] for col, val in zip(col_names, values) }

                dico['NAME'] = [team_name]

                df = pd.DataFrame(dico)


                columns = ['MP', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'NAME']

                nv_df = df[columns].copy()

                #nv_df['NAME'] = team_name


                list_df.append(nv_df)

        
        final_df = pd.concat(list_df, ignore_index=True)

        


    else:
        print("Probleme")


    

        


