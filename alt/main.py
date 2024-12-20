import nextcord
from nextcord.ext import commands
import os
import logging
import asyncio
import uvicorn
import threading
from Bot.Setup.Discord.config import bot
from dotenv import load_dotenv
from Bot.Setup.Discord.config import bot
from Bot.Setup.Logging.log_config import setup_logging
from Bot.Setup.Server.app import app

# Konfiguriere den Bot
load_dotenv(dotenv_path="secret.env")
token = os.getenv("token")

# Konfiguriere das Logging
logger = setup_logging()
logging.basicConfig(level=logging.INFO)

intents = nextcord.Intents.default()
intents.members = True
intents.messages = False
intents.reactions = True
intents.guilds = True
bot = commands.Bot(intents=intents)
	
def run_fastapi():
    config = uvicorn.Config("Bot.Setup.Server.app:app", host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    server.run()

bot.load_extension("Commands.Ankuendigung.Umfrage.Deathzone.dz_cwl_umfrage")
bot.load_extension("Commands.Ankuendigung.Umfrage.Academy.ac_cwl_umfrage")
bot.load_extension("Commands.Ankuendigung.Umfrage.Immortality.im_cwl_umfrage")
bot.load_extension("Tasks.Member.update_member")
bot.load_extension("Tasks.Clash.Clan.clan_data_cog")
bot.load_extension("Tasks.Leaderboard.clan_member")
bot.load_extension("Tasks.Leaderboard.daily_task")
bot.load_extension("events.events_setup")

if __name__ == "__main__":
    # Starte den FastAPI-Server in einem separaten Thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    # Events
    bot.load_extension("Bot.Setup.Event.on_ready")
    
    # Help Commands
    bot.load_extension("Commands.Help.Vize.vize_help")
    
    # Deathzone Commands 
    bot.load_extension("Commands.Ankuendigung.Umfrage.Deathzone.dz_cw_umfrage")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Deathzone.dz_save_reaction")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Deathzone.dz_auswertung")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Deathzone.dz_ja_reaction")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Deathzone.dz_burgen_fueller")
    
    bot.load_extension("Commands.Ankuendigung.Umfrage.Deathzone.dz_monat_auswertung")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Deathzone.dz_cw_none_reaction")
    # Acadamy Commands
    bot.load_extension("Commands.Ankuendigung.Umfrage.Academy.ac_cw_umfrage")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Academy.ac_save_reaction")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Academy.ac_auswertung")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Academy.ac_ja_reaction")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Academy.ac_burgen_fueller")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Academy.ac_none_reaction")
    # Immortality Commands
    bot.load_extension("Commands.Ankuendigung.Umfrage.Immortality.im_cw_umfrage")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Immortality.im_save_reaction")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Immortality.im_auswertung")
    #bot.load_extension("Commands.Ankuendigung.Umfrage.Immortality.ja_reaction")
	# Utopia Commands
    bot.load_extension("Commands.Ankuendigung.Umfrage.Utopia.ut_cw_umfrage")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Utopia.ut_save_reaction")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Utopia.ut_auswertung")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Utopia.ut_ja_reaction")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Utopia.ut_burgen_fueller")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Utopia.ut_cwl_umfrage")
	# FighterZ Commands
    bot.load_extension("Commands.Ankuendigung.Umfrage.Fighterz.fz_cw_umfrage")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Fighterz.fz_save_reaction")
    bot.load_extension("Commands.Ankuendigung.Umfrage.Fighterz.fz_auswertung")
    # Owner Commands
    bot.load_extension("Commands.Help.Owner.owner_help")
    
    #bot.load_extension("Cogs.Commands.Add_Member.log_managment")
	# Leaderboard
    
	# Event Commands
    bot.load_extension("Commands.Event.event_registration")
    bot.load_extension("Commands.Event.event_download")
    bot.load_extension("Commands.Event.event_help")
    bot.load_extension("Commands.Event.event_phasen")
	# Verwarnung
    bot.load_extension("Commands.Ankuendigung.Strikes.verwarnung")

    
	
	

	# Starte den bot 
    bot.run(os.environ['token'])
    logger.info(f'{bot.user} wurde gestoppt')