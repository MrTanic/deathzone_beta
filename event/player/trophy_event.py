import coc
import nextcord
import requests
import json
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der webhook.env Datei
load_dotenv('bot/secret/webhook.env')

# Pfad zur Datei, in der die Player-Tags gespeichert werden
PLAYER_TAGS_FILE = "deathzone/player_tags.py"

class TrophyEventsHandlers:
    def __init__(self, bot):
        self.bot = bot
        self.webhook_url = os.getenv('LEGEND_HOOK')
        if not self.webhook_url:
            raise ValueError("Webhook URL is not set in webhook.env")
        self.player_tags = self.load_player_tags()

    def load_player_tags(self):
        if not os.path.exists(PLAYER_TAGS_FILE):
            raise FileNotFoundError(f"No such file or directory: '{PLAYER_TAGS_FILE}'")
        
        with open(PLAYER_TAGS_FILE, 'r') as file:
            content = file.read()
            start = content.find("[")
            end = content.find("]")
            tags = content[start:end+1].replace("\n", "").replace(" ", "")
            return eval(tags)  # Verwenden Sie eval() vorsichtig und nur wenn Sie die Quelle kontrollieren

    def register_trophy_events(self, client):
        @coc.PlayerEvents.trophies(tags=self.player_tags)
        async def on_player_trophy_change(old_player, new_player):
            await self.handle_trophy_change(old_player, new_player, self.webhook_url)
        client.add_events(on_player_trophy_change)
        self.on_player_trophy_change = on_player_trophy_change

    async def handle_trophy_change(self, old_player, new_player, webhook_url):
        trophy_change = new_player.trophies - old_player.trophies
        change_symbol = "<:sword:1251199323006308367>" if trophy_change > 0 else "<:shield:1251198941198946364>"
        change_sign = "+" if trophy_change > 0 else "-"
        color = nextcord.Color.green() if trophy_change > 0 else nextcord.Color.red()
        
        player_profile_url = f"https://link.clashofclans.com/en?action=OpenPlayerProfile&tag={new_player.tag.strip('#')}"

        embed = nextcord.Embed(
            description=f"{change_symbol} {change_sign}{abs(trophy_change)} trophies | [Profil]({player_profile_url})",
            color=color,
            timestamp=nextcord.utils.utcnow()
        )
        embed.set_author(
            name=f"{new_player.name} | {new_player.tag}"
        )
        embed.set_footer(text=f"🏆 {new_player.trophies}")

        data = {
            "embeds": [embed.to_dict()]
        }

        response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if response.status_code != 204:
            print(f"Failed to send webhook for player {new_player.tag}: {response.status_code}, {response.text}")