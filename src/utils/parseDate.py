from datetime import datetime

def parse_date(date_string):
    """Convertit différents formats de date en format YYYY-MM-DD."""
    if not date_string:
        return None
    
    date_string = date_string.strip()
    
    # Liste des formats possibles
    formats = [
        "%a %b %d %Y",        # "Wed Oct 23 2024"
        "%B %d, %Y",          # "October 25, 2024"
    ]
    
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_string, fmt)
            return date_obj.strftime("%Y-%m-%d")  # Retourne "2024-10-25"
        except ValueError:
            continue
    
    # Si aucun format ne correspond
    print(f"Format de date non reconnu : {date_string}")
    return date_string

if __name__ == "__main__":
    print(parse_date("Wed Oct 23 2024"))
    print(parse_date("October 25, 2024"))