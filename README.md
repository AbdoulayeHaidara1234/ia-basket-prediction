🏀 Prédiction NBA
Ce projet a pour objectif de construire une architecture système IA complète, de la collecte de données jusqu'à la prédiction des résultats de matchs de la NBA.
Il s'inscrit dans le cadre d'un projet personnel pour maîtriser les enjeux la Data Science.

🎯 Objectifs du Projet
Objectif Business : Développer un modèle capable de prédire l'issue d'un match (Classification binaire).
Données d'entraînement : Matchs d'octobre à février (Saison 2024-2025).
Cible : Prédire la victoire de l'équipe à domicile.

🏗️ Architecture Technique
Structure du projet :
ia-basket-prediction/
├── data/
│   ├── raw/            # Données brutes immuables (CSV par mois, boxscores)
│   ├── interim/        # Données intermédiaires (URLs de matchs, fichiers nettoyés)
│   └── processed/      # Dataset final unique prêt pour le Machine Learning
├── src/
│   ├── data/           # Scripts de scraping (URLs et boxscores)
│   ├── features/       # Feature engineering (Rolling averages, ratings)
│   └── models/         # Scripts d'entraînement et de prédiction
├── notebooks/          # Explorations (EDA) et tests de modèles
├── .github/workflows/  # Intégration continue (Linter Flake8)
├── .gitignore          # Exclusion des données lourdes et du venv
└── requirements.txt    # Dépendances du projet


🛠️ Installation et Configuration
Cloner le projet :
git clone https://github.com/votre-utilisateur/ia-basket-prediction.git
cd ia-basket-prediction


Créer l'environnement virtuel :
python -m venv .venv
source .venv/bin/activate  # Sur Mac/Linux
# .venv\Scripts\activate   # Sur Windows


Installer les dépendances:
pip install -r requirements.txt



📊 Pipeline de Données
1. Acquisition (Scraping)
Les données sont extraites depuis Basketball-Reference.
scraper_urls.py : Récupère les URLs de tous les boxscores de la saison.
scraper_boxscores.py : Extrait les statistiques "Team Totals" (points, rebonds, tirs, etc.) pour chaque match.

2. Feature Engineering
Pour chaque match, le modèle utilise des informations connues avant le coup d'envoi:
Statistiques glissantes (roll5) : Moyenne des 5 derniers matchs pour les points, FG%, TOV, etc.
Indicateurs d'efficacité : Offensive Rating (ORtg), Defensive Rating (DRtg) et Pace recalculés dynamiquement.
Contexte : Avantage à domicile, jours de repos, blessures des joueurs clés.

🛡️ Qualité et CI/CD
Ce projet utilise GitHub Actions comme "gardien" du code :
Linter (Flake8) : À chaque push sur la branche main, un robot vérifie automatiquement la syntaxe et la qualité du code Python.
Le workflow est défini dans .github/workflows/qualite_code.yml.

🚀 Utilisation
Collecte : python src/data/scraper_urls.py puis python src/data/scraper_boxscores.py.
Fusion : python src/features/merge_data.py.
Modélisation : Consulter les notebooks dans notebooks/ pour l'analyse exploratoire et les premiers tests de modèles.
