import asyncio
import httpx
from .legends_task import fetch_multiple_players
from deathzone.player_tags import player_tags

async def get_current_season():
    url = "https://api.clashking.xyz/list/seasons?last=12"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        seasons = response.json()
        current_season = seasons[0]
        print(f"Aktuelle Saison: {current_season}")
        return current_season

async def scheduler():
    season = await get_current_season()
    results = await fetch_multiple_players(player_tags, season)
    return results  # Wir geben die Ergebnisse zurück, damit der Aufrufer diese weiter verarbeiten kann.