from nextcord.ext import commands
from events.player.trophy import TrophyEventsHandlers
from connection import COCConnectionManager

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection_manager = COCConnectionManager()
        self.coc_client = self.connection_manager.create_client()
        
        # Spieler-Tags
        self.player_tags = [
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

        # Webhook-URL
        self.webhook_url = 'https://discord.com/api/webhooks/1251192491315826792/wEkZbcpPwY9IC4je5WZGElIItlNvlUXyUTovOnBgRjRPZ9VOi7rC_iYwsHiAeOmQAG2J'

        # Initialisiere die Event-Handler mit der Webhook-URL und Spieler-Tags
        self.trophy_event_handler = TrophyEventsHandlers(bot, self.webhook_url, self.player_tags)

        self.bot.loop.create_task(self.start_coc_client())

    async def start_coc_client(self):
        try:
            await self.connection_manager.login()
            self.coc_client.add_player_updates(*self.player_tags)
            self.register_events()
            print("COC-Events wurden erfolgreich geladen und gestartet.")
        except Exception as error:
            print(f"Login or setup failed: {error}")

    def register_events(self):
        self.trophy_event_handler.register_trophy_events(self.coc_client)

    def cog_unload(self):
        self.bot.loop.create_task(self.connection_manager.logout())

def setup(bot):
    bot.add_cog(EventsCog(bot))