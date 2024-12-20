import coc
import nextcord
from nextcord.ext import commands
import requests
import json

class TrophyEventsHandlers(commands.Cog):
    def __init__(self, bot, webhook_url, player_tags):
        self.bot = bot
        self.webhook_url = webhook_url
        self.player_tags = player_tags
        self.register_trophy_event_handler()

    def register_trophy_events(self, client):
        client.add_events(
            self.on_player_trophy_change
        )

    def register_trophy_event_handler(self):
        @coc.PlayerEvents.trophies(tags=self.player_tags)
        async def on_player_trophy_change(old_player, new_player):
            await self.handle_trophy_change(old_player, new_player)
        self.on_player_trophy_change = on_player_trophy_change

    async def handle_trophy_change(self, old_player, new_player):
        trophy_change = new_player.trophies - old_player.trophies
        change_symbol = "<:sword:1251199323006308367>" if trophy_change > 0 else "<:shield:1251198941198946364>"
        change_sign = "+" if trophy_change > 0 else "-"
        color = nextcord.Color.green() if trophy_change > 0 else nextcord.Color.red()
        
        player_profile_url = f"https://link.clashofclans.com/en?action=OpenPlayerProfile&tag={new_player.tag.strip('#')}"

        embed = nextcord.Embed(
            description=f"{change_symbol} {change_sign}{abs(trophy_change)} trophies | [Profil]({player_profile_url})",
            color=color,  # Grün für positive Änderungen, Rot für negative Änderungen
            timestamp=nextcord.utils.utcnow()
        )
        embed.set_author(
            name=f"{new_player.name} | {new_player.tag}"
        )
        embed.set_footer(text=f"🏆 {new_player.trophies}")

        data = {
            "embeds": [embed.to_dict()]
        }

        response = requests.post(self.webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if response.status_code != 204:
            print(f"Failed to send webhook for player {new_player.tag}: {response.status_code}, {response.text}")

def setup(bot):
    player_tags = [
        '#2R989JJ98',
        '#9LL82P00R',
        '#LVJJPQJQR',
        '#2QUQ0JY0',
        '#2CGQVJQ9',
        '#200LC0JG8',
        '#YGVG8C2PO',
        '#9VYJLVQJ8',
        '#P9U9998C',
        
        
    ]
    bot.add_cog(TrophyEventsHandlers(bot, 'https://discord.com/api/webhooks/1251192491315826792/wEkZbcpPwY9IC4je5WZGElIItlNvlUXyUTovOnBgRjRPZ9VOi7rC_iYwsHiAeOmQAG2J', player_tags))