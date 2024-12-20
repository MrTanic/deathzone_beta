# embed_creator.py
import nextcord

async def create_leaderboard_embed(sorted_players, clan_name="DeathZone Legend Ranking"):
    if not sorted_players:
        return None

    description_text = ""
    for index, player in enumerate(sorted_players, start=1):
        player_name = player.get('name', 'Unbekannter Spieler')
        trophies = player.get('trophies', 0)
        description_text += f"{index}. 🏆 {trophies} - {player_name}\n"

    embed = nextcord.Embed(title=clan_name, description=description_text.strip(), color=nextcord.Color.dark_gold())
    

    return embed