from pathlib import Path
import pandas as pd
from src.utils.parseDate import parse_date
from src.utils.TeamNames import get_team_code

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "interim" / "schedule"
OUTPUT_CSV = OUTPUT_DIR / "all_schedule_totals.csv"

def get_data_directory():
    """Retourne le chemin vers le dossier de données."""
    return Path(__file__).resolve().parents[2] / "data" / "raw" / "schedule"


def charger_tous_les_csv(data_dir):
    """Charge tous les fichiers CSV d'un dossier et les retourne dans une liste."""
    dataframes = []
    data_path = Path(data_dir)

    for fichier in sorted(data_path.iterdir()):
        if fichier.is_file() and fichier.suffix == '.csv':
            try:
                df = pd.read_csv(fichier)
                dataframes.append(df)
            except FileNotFoundError as e:
                print(f"Erreur avec {fichier.name}: {e}")
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

    df_intermediaire.columns = ["Date", "away_team", "away_score", "home_team", "home_score", "home_win"]

    nv_ordre = ["Date", "home_team", "home_score","away_team", "away_score", "home_win"]


    df_final = df_intermediaire[nv_ordre]

    df_final['Date'] = df_final['Date'].apply(parse_date)
    df_final['home_team'] = df_final['home_team'].apply(get_team_code)
    df_final['away_team'] = df_final['away_team'].apply(get_team_code)

    return df_final

df_final = restructurer_dataset_final()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df_final.to_csv(OUTPUT_CSV, index=False)