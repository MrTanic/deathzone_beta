import nextcord
from nextcord.ext import commands
import os
import logging
import asyncio
import uvicorn
from dotenv import load_dotenv
from Bot.Setup.Discord.config import bot
from Bot.Setup.Logging.log_config import setup_logging
from Bot.Setup.Server.app import app  # Stelle sicher, dass dieser Importpfad zu deiner FastAPI-Anwendungsdatei passt

# Konfiguriere den Bot
load_dotenv(dotenv_path="secret.env")
TOKEN = os.getenv("token")

# Konfiguriere das Logging
logger = setup_logging()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    logger.info(f'Bot gestartet als {bot.user}')
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Deine Webseite oder Bot-Funktionalität"))

async def start_fastapi():
    config = uvicorn.Config("Bot.Setup.Server.app:app", host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Bot Extensions laden
    bot.load_extension("Commands.Help.Vize.vize_help")
    # Hier weitere bot.load_extension Aufrufe hinzufügen

    # Starte FastAPI als Task
    asyncio.create_task(start_fastapi())

    # Starte den Discord-Bot
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())