from nextcord.ext import commands
from event.player.trophy_event import TrophyEventsHandlers
from client.connection import COCConnectionManager

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection_manager = COCConnectionManager()
        self.coc_client = self.connection_manager.create_client()

        # Initialisiere die Event-Handler
        self.trophy_event_handler = TrophyEventsHandlers(bot)
        
        self.bot.loop.create_task(self.start_coc_client())

    async def start_coc_client(self):
        try:
            await self.connection_manager.login()
            # Lade und registriere die Events
            self.trophy_event_handler.register_trophy_events(self.coc_client)
            print("COC-Events wurden erfolgreich geladen und gestartet.")
        except Exception as error:
            print(f"Login or setup failed: {error}")

    def cog_unload(self):
        self.bot.loop.create_task(self.connection_manager.logout())

def setup(bot):
    bot.add_cog(EventsCog(bot))