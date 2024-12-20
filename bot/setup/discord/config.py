import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True
intents.messages = False
intents.reactions = True
intents.guilds = True
bot = commands.Bot(intents=intents)