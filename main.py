import nextcord
from nextcord.ext import commands
import os
import logging
import asyncio
import uvicorn
import threading
from dotenv import load_dotenv
from bot.setup.discord.config import bot
from bot.setup.logging.log_config import setup_logging
from bot.setup.server.app import app
from cogs.family.load_family_commands import load_family_commands
from cogs.umfrage.load_deathzone_commands import load_deathzone_commands
from cogs.umfrage.load_academy_commands import load_academy_commands
from cogs.umfrage.load_immortality_commands import load_immortality_commands
from cogs.umfrage.load_utopia_commands import load_utopia_commands
from cogs.owner.load_owner_commands import load_owner_commands
from cogs.strikes.load_strikes_commands import load_strikes_commands

# Konfiguriere den Bot
load_dotenv(dotenv_path="bot/secret/discord.env")
token = os.getenv("token")

# Konfiguriere das Logging
logger = setup_logging()
logging.basicConfig(level=logging.INFO)

intents = nextcord.Intents.default()
#intents.members = True
#intents.messages = False
#intents.reactions = True
#intents.guilds = True
bot = commands.Bot(intents=intents)
	
def run_fastapi():
    config = uvicorn.Config("bot.setup.server.app:app", host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    server.run()

# EVENTS ---------------------
bot.load_extension("event.on_ready")
#bot.load_extension("event.on_button_click")
#bot.load_extension("event.events_setup")
# BACKGROUND -----------------
bot.load_extension("background.member.update_member")
#bot.load_extension("background.clash.clan.clan_data_cog")
#bot.load_extension("background.clash.player.legend.legends_cog")
# TASKS ----------------------
#bot.load_extension("tasks.leaderboard.leaderboard")
#bot.load_extension("tasks.cwl_ankuendigung.dz_cwl_task")
#bot.load_extension("tasks.cwl_ankuendigung.ac_cwl_task")
#bot.load_extension("tasks.cwl_ankuendigung.im_cwl_task")
#bot.load_extension("tasks.cwl_ankuendigung.ut_cwl_task")
# Strike Taks
#bot.load_extension("tasks.strikes.reset_strike")
# Commands -------------------
#bot.load_extension("commands.link_user.link_cog")
#bot.load_extension("commands.help.help_command")

if __name__ == "__main__":
    # Starte den FastAPI-Server in einem separaten Thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    # Laden der Commands (Umfrage)
    #load_deathzone_commands(bot)
    #load_academy_commands(bot)
    #load_immortality_commands(bot)
    load_utopia_commands(bot)
    #load_fighterz_commands(bot)
    # Laden der Commands (Family)
    #load_family_commands(bot)
    # Laden der Commands (Owner)
    #load_owner_commands(bot)
    #load_strikes_commands(bot)
    
	# Starte den bot 
    bot.run(os.environ['token'])