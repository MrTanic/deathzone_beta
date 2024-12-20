import json
import os

def read_all_clan_data(folder="datenbank/clan"):
    all_players = []
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    if "memberList" in data:
                        all_players.extend(data["memberList"])
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filename}: {e}")
                except Exception as e:
                    print(f"Unexpected error reading file {filename}: {e}")
    # Sortiere alle Spieler nach Trophäen absteigend und beschränke auf die Top 25
    sorted_players = sorted(all_players, key=lambda x: x.get("trophies", 0), reverse=True)[:25]
    return sorted_players
