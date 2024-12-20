# Bot/Cogs/ready_cog.py
import nextcord
from nextcord.ext import commands

class ReadyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="dzclash.de"))

def setup(bot):
    bot.add_cog(ReadyCog(bot))