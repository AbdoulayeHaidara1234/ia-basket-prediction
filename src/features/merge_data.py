import os
import pandas as pd

def get_data_directory():
    """Retourne le chemin vers le dossier de données."""
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, "..", "..", "data", "raw", "schedule")



def charger_tous_les_csv(data_dir):
    """Charge tous les fichiers CSV d'un dossier et les retourne dans une liste."""
    dataframes = []
    for fichier in sorted(os.listdir(data_dir)):
        chemin = os.path.join(data_dir, fichier)
        if os.path.isfile(chemin):
            try:
                df = pd.read_csv(chemin)
                dataframes.append(df)
            except FileNotFoundError as e:
                print(f"✗ Erreur avec {fichier}: {e}")
    return dataframes



def concatener_dataframes(dataframes):
    """Concatène une liste de DataFrames."""
    return pd.concat(dataframes, ignore_index=True)

def filtrer_colonnes(df, colonnes_voulues):
    """Filtre le DataFrame pour ne garder que les colonnes existantes."""
    colonnes_existantes = [col for col in colonnes_voulues if col in df.columns]
    return df[colonnes_existantes]


def preparer_dataset_final():
    """Fonction principale qui orchestre tout le processus."""
    # Définir les colonnes à conserver
    colonnes_voulues = ["Date", "Visitor/Neutral", "PTS", "Home/Neutral", "PTS.1"]
    
    # Charger les données
    data_dir = get_data_directory()
    dataframes = charger_tous_les_csv(data_dir)
    
    if not dataframes:
        print("Aucun fichier chargé!")
        return None
    
    # Concatener
    df_intermediaire = concatener_dataframes(dataframes)
    
    # Filtrer les colonnes
    df_final = filtrer_colonnes(df_intermediaire, colonnes_voulues)
    
    return df_final

def restructurer_dataset_final():

    df_intermediaire = preparer_dataset_final()

    df_intermediaire["Home_win"] = df_intermediaire["PTS.1"] > df_intermediaire["PTS"] 

    df_intermediaire.columns = ["date", "away_team", "away_score", "home_team", "home_score", "home_win"]

    nv_ordre = ["date", "home_team", "home_score","away_team", "away_score", "home_win"]

    df_final = df_intermediaire[nv_ordre]

    return df_final

print(restructurer_dataset_final())