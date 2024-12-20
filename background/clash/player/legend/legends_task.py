import httpx
import os
import json
import asyncio

base_path = "datenbank/player/legends"

def remove_hero_gear(data):
    for day_data in data.get('legends', {}).values():
        for attack in day_data.get('new_attacks', []):
            if 'hero_gear' in attack:
                del attack['hero_gear']
    return data

def add_current_trophies(data):
    for day_data in data.get('legends', {}).values():
        all_changes = day_data.get('new_attacks', []) + day_data.get('new_defenses', [])
        if all_changes:
            latest_change = max(all_changes, key=lambda x: x['time'])
            day_data['current_trophies'] = latest_change['trophies']
        day_data['total_attacks'] = sum(attack['change'] for attack in day_data.get('new_attacks', []))
        day_data['total_defenses'] = sum(defense['change'] for defense in day_data.get('new_defenses', []))
    return data

def save_data_to_file(player_tag, season, data):
    data = remove_hero_gear(data)  # Entferne hero_gear aus den Daten
    data = add_current_trophies(data)  # Füge aktuelle Trophäenanzahl und zusammengefasste Werte hinzu
    season_folder = os.path.join(base_path, season)
    os.makedirs(season_folder, exist_ok=True)
    print(f"Speichere Daten in Ordner: {season_folder}")
    
    player_tag_clean = player_tag.replace("#", "")  # Entfernt das '#' Zeichen
    file_path = os.path.join(season_folder, f"{player_tag_clean}.json")
    print(f"Speicherpfad für {player_tag}: {file_path}")
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Daten erfolgreich gespeichert für {player_tag}")

async def fetch_legends_data(player_tag, season):
    player_tag_encoded = player_tag.replace("#", "%23")  # Kodiert das '#' Zeichen
    url = f"https://api.clashking.xyz/player/{player_tag_encoded}/legends?season={season}"
    print(f"Rufe Daten ab von URL: {url}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            if 'legends' not in data:
                raise ValueError(f"Ungültige Antwortdaten für {player_tag}: {data}")
            save_data_to_file(player_tag, season, data)
            return True, player_tag  # Erfolgreich
        except httpx.HTTPStatusError as e:
            print(f"HTTP-Fehler beim Abrufen der Daten für {player_tag}: {e.response.status_code} {e.response.text}")
            return False, f"HTTP-Fehler beim Abrufen der Daten für {player_tag}: {e}"
        except ValueError as e:
            print(f"Datenfehler für {player_tag}: {e}")
            return False, f"Datenfehler für {player_tag}: {e}"
        except Exception as e:
            print(f"Ein allgemeiner Fehler ist aufgetreten für {player_tag}: {e}")
            return False, f"Ein allgemeiner Fehler ist aufgetreten für {player_tag}: {e}"

async def fetch_multiple_players(player_tags, season):
    results = []
    for i in range(0, len(player_tags), 20):
        tasks = [fetch_legends_data(tag, season) for tag in player_tags[i:i+20]]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
        await asyncio.sleep(1)  # Wartezeit von 1 Sekunde nach jeder Gruppe von 20 Anfragen
    return results