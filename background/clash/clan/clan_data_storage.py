import json
import os

def save_clan_data(clan_data):
    clan_tag = clan_data['tag'].replace('#', '')  # Entferne das '#' Symbol vom Tag
    directory = "datenbank/clan/"
    os.makedirs(directory, exist_ok=True)  # Erstelle das Verzeichnis, falls es nicht existiert
    file_path = os.path.join(directory, f"{clan_tag}.json")
    
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(clan_data, f, indent=4, ensure_ascii=False)