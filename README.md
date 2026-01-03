# 🏀 Prédiction NBA
<br>
Ce projet a pour objectif de construire une architecture système IA complète, de la collecte de données jusqu'à la prédiction des résultats de matchs de la NBA.
Il s'inscrit dans le cadre d'un projet personnel pour maîtriser les enjeux la Data Science.

🎯 Objectifs du Projet
<br>
Objectif Business : Développer un modèle capable de prédire l'issue d'un match (Classification binaire).
Données d'entraînement : Matchs d'octobre à février (Saison 2024-2025).
Cible : Prédire la victoire de l'équipe à domicile.

# 🏗️ Architecture Technique
<br>
Structure du projet :
<br>
<img width="629" height="283" alt="image" src="https://github.com/user-attachments/assets/cbd4d129-d0ca-4760-b97e-e59df7ec2430" />
<br>

# 🛠️ Installation et Configuration
<br>
Cloner le projet :
<br>
git clone https://github.com/votre-utilisateur/ia-basket-prediction.git
<br>
cd ia-basket-prediction


Créer l'environnement virtuel :
<br>
python -m venv .venv
<br>
source .venv/bin/activate  # Sur Mac/Linux
<br>
.venv\Scripts\activate   # Sur Windows

<br>
Installer les dépendances:
<br>
pip install -r requirements.txt



📊 Pipeline de Données
<br>
1. Acquisition (Scraping)<br>
Les données sont extraites depuis Basketball-Reference.<br>
scraper_urls.py : Récupère les URLs de tous les boxscores de la saison.<br>
scraper_boxscores.py : Extrait les statistiques "Team Totals" (points, rebonds, tirs, etc.) pour chaque match.<br>

2. Feature Engineering<br>
Pour chaque match, le modèle utilise des informations connues avant le coup d'envoi:<br>
Statistiques glissantes (roll5) : Moyenne des 5 derniers matchs pour les points, FG%, TOV, etc.<br>
Indicateurs d'efficacité : Offensive Rating (ORtg), Defensive Rating (DRtg) et Pace recalculés dynamiquement.<br>
Contexte : Avantage à domicile, jours de repos, blessures des joueurs clés.<br>

🛡️ Qualité et CI/CD<br>
Ce projet utilise GitHub Actions comme "gardien" du code :<br>
Linter (Flake8) : À chaque push sur la branche main, un robot vérifie automatiquement la syntaxe et la qualité du code Python.<br>
Le workflow est défini dans .github/workflows/qualite_code.yml.<br>

🚀 Utilisation<br>
Collecte : python src/data/scraper_urls.py puis python src/data/scraper_boxscores.py.<br>
Fusion : python src/features/merge_data.py.<br>
Modélisation : Consulter les notebooks dans notebooks/ pour l'analyse exploratoire et les premiers tests de modèles.
