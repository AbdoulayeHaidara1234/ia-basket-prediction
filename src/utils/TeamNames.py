"""
Module pour mapper les noms des équipes NBA avec leurs codes à trois lettres.
"""

# Dictionnaire mapping nom complet -> code
TEAM_NAME_TO_CODE = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BRK",
    "Charlotte Hornets": "CHO",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHO",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS"
}

# Dictionnaire inverse code -> nom complet
CODE_TO_TEAM_NAME = {code: name for name, code in TEAM_NAME_TO_CODE.items()}


def get_team_code(team_name: str) -> str:
    """
    Retourne le code de l'équipe à partir de son nom complet.
    
    Args:
        team_name: Le nom complet de l'équipe (ex: "Boston Celtics")
    
    Returns:
        Le code à trois lettres de l'équipe (ex: "BOS")
    
    Raises:
        KeyError: Si le nom de l'équipe n'est pas trouvé
    """
    return TEAM_NAME_TO_CODE[team_name]


def get_team_name(team_code: str) -> str:
    """
    Retourne le nom complet de l'équipe à partir de son code.
    
    Args:
        team_code: Le code à trois lettres de l'équipe (ex: "BOS")
    
    Returns:
        Le nom complet de l'équipe (ex: "Boston Celtics")
    
    Raises:
        KeyError: Si le code de l'équipe n'est pas trouvé
    """
    return CODE_TO_TEAM_NAME[team_code]


def is_valid_team_name(team_name: str) -> bool:
    """
    Vérifie si le nom d'équipe est valide.
    
    Args:
        team_name: Le nom de l'équipe à vérifier
    
    Returns:
        True si le nom est valide, False sinon
    """
    return team_name in TEAM_NAME_TO_CODE


def is_valid_team_code(team_code: str) -> bool:
    """
    Vérifie si le code d'équipe est valide.
    
    Args:
        team_code: Le code de l'équipe à vérifier
    
    Returns:
        True si le code est valide, False sinon
    """
    return team_code in CODE_TO_TEAM_NAME


def get_all_team_names() -> list:
    """
    Retourne la liste de tous les noms d'équipes.
    
    Returns:
        Liste des noms complets de toutes les équipes NBA
    """
    return list(TEAM_NAME_TO_CODE.keys())


def get_all_team_codes() -> list:
    """
    Retourne la liste de tous les codes d'équipes.
    
    Returns:
        Liste de tous les codes à trois lettres des équipes NBA
    """
    return list(CODE_TO_TEAM_NAME.keys())


if __name__ == "__main__":
    # Exemples d'utilisation
    print("Exemples d'utilisation:\n")
    
    # Obtenir le code d'une équipe
    team = "Boston Celtics"
    code = get_team_code(team)
    print(f"{team} -> {code}")
    
    # Obtenir le nom d'une équipe à partir du code
    code = "LAL"
    name = get_team_name(code)
    print(f"{code} -> {name}")
    
    # Vérifier si un nom d'équipe est valide
    print(f"\n'Boston Celtics' est valide: {is_valid_team_name('Boston Celtics')}")
    print(f"'Invalid Team' est valide: {is_valid_team_name('Invalid Team')}")
    
    # Afficher toutes les équipes
    print(f"\nNombre total d'équipes NBA: {len(TEAM_NAME_TO_CODE)}")
    print("\nToutes les équipes:")
    for name, code in sorted(TEAM_NAME_TO_CODE.items()):
        print(f"  {code}: {name}")