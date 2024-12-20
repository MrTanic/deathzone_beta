import coc
import nextcord
from nextcord.ext import commands
import requests
import json
import os

class TrophyEventsHandlers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook = self.load_webhook()
        self.register_trophy_event_handler()

    def load_webhook(self):
        webhooks_dir = 'events/player/webhooks'
        webhook_file = 'webhook_2.json'
        webhook_path = os.path.join(webhooks_dir, webhook_file)
        
        if not os.path.exists(webhook_path):
            raise FileNotFoundError(f"No such file or directory: '{webhook_path}'")
        
        with open(webhook_path, 'r') as f:
            webhook = json.load(f)
        
        return webhook

    def register_trophy_events(self, client):
        client.add_events(self.on_player_trophy_change)

    def register_trophy_event_handler(self):
        @coc.PlayerEvents.trophies(tags=self.webhook['player_tags'])
        async def on_player_trophy_change(old_player, new_player):
            if new_player.trophies > 4900:
                await self.handle_trophy_change(old_player, new_player, self.webhook['webhook_url'])
        self.on_player_trophy_change = on_player_trophy_change

    async def handle_trophy_change(self, old_player, new_player, webhook_url):
        if new_player.trophies <= 4900:
            return
        
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

def setup(bot):
    bot.add_cog(TrophyEventsHandlers(bot))