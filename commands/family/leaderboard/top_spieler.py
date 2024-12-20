# clan_members_cog.py
from nextcord.ext import commands
import nextcord
from bot.setup.discord.server_ids import SERVER
from utility.leaderboard.read_clan_data import read_all_clan_data
from utility.leaderboard.embed_creator import create_leaderboard_embed

class LeaderBoardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="leaderboard", description="Zeigt die Top 25 Spieler aus allen Clans.", guild_ids=SERVER)
    async def show_top_players(self, interaction: nextcord.Interaction):
        sorted_players = read_all_clan_data()
        embed = await create_leaderboard_embed(sorted_players, "Top 25 Spieler von Deathzone")
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(LeaderBoardCog(bot))