import nextcord
from nextcord.ext import commands

class HelpEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction: nextcord.Interaction):
        command_name = interaction.custom_id
        await interaction.response.send_message(f"/{command_name} ", ephemeral=True)

def setup(bot):
    bot.add_cog(HelpEvent(bot))