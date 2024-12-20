import requests
from COC.Api.api_header import api_header

def fetch_player_data(player_tag):
    url = f"https://api.clashofclans.com/v1/players/{player_tag.replace('#', '%23')}"
    headers = api_header()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return True, data.get('name', 'Unbekannter Spieler')
    else:
        return False, None