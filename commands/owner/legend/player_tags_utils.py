import json
import os

# Datei, in der die Player-Tags gespeichert werden
PLAYER_TAGS_FILE = "deathzone/player_tags.py"
PLAYERS_FILE = "deathzone/players.json"
CLAN_DATA_DIR = "datenbank/clan"

def load_player_tags():
    if not os.path.exists(PLAYER_TAGS_FILE):
        return []

    with open(PLAYER_TAGS_FILE, 'r') as file:
        content = file.read()
        start = content.find("[")
        end = content.find("]")
        tags = content[start:end+1].replace("\n", "").replace(" ", "")
        return eval(tags)  # Verwenden Sie eval() vorsichtig und nur wenn Sie die Quelle kontrollieren

def save_player_tags(tags):
    with open(PLAYER_TAGS_FILE, 'w') as file:
        file.write(f"player_tags = {tags}")

def load_clan_files():
    clan_files = {}
    for filename in os.listdir(CLAN_DATA_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(CLAN_DATA_DIR, filename), "r") as file:
                clan_data = json.load(file)
                clan_files[filename] = clan_data
    return clan_files

def load_players_file():
    if not os.path.exists(PLAYERS_FILE):
        return []

    with open(PLAYERS_FILE, "r") as file:
        return json.load(file)

def save_players_file(players):
    with open(PLAYERS_FILE, "w") as file:
        json.dump(players, file, indent=4)