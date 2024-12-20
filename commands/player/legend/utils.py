import httpx
import os
import json

def load_players():
    with open('deathzone/players.json', 'r') as file:
        return json.load(file)

def get_player_tag_by_name(player_name: str, players):
    for player in players:
        if player_name.lower() == player['name'].lower():
            return player['tag']
    return None

def find_legend_data(player_tag: str, date: str):
    player_tag_clean = player_tag.replace("#", "")
    possible_folders = [f"datenbank/player/legends/{d}" for d in os.listdir("datenbank/player/legends") if os.path.isdir(f"datenbank/player/legends/{d}")]
    
    for folder in possible_folders:
        file_path = os.path.join(folder, f"{player_tag_clean}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                if date in data['legends']:
                    return data['legends'][date], data
    return None, None

def find_season_legend_data(player_tag: str, season: str):
    player_tag_clean = player_tag.replace("#", "")
    folder = f"datenbank/player/legends/{season}"
    file_path = os.path.join(folder, f"{player_tag_clean}.json")

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get('legends', {})
    return None

async def fetch_player_history(player_tag: str):
    player_tag_encoded = player_tag.replace("#", "%23")
    url = f"https://api.clashking.xyz/player/{player_tag_encoded}/legend_rankings?limit=24"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP-Fehler beim Abrufen der historischen Daten für {player_tag}: {e.response.status_code} {e.response.text}")
            return None
        except Exception as e:
            print(f"Ein allgemeiner Fehler ist aufgetreten für {player_tag}: {e}")
            return None