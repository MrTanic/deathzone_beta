import nextcord
from nextcord.ext import commands
from datetime import datetime
from bot.setup.discord.server_ids import SERVER
from .utils import get_player_tag_by_name, load_players, find_legend_data, find_season_legend_data, fetch_player_history
from .legend_day_embed import create_legend_embed
from .legend_season_embed import create_season_embed
from .legend_history_embed import create_history_embed

class LegendStatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = load_players()

    @nextcord.slash_command(name='legend', description='Verwalte Legend-Statistiken', guild_ids=SERVER)
    async def legend(self, interaction: nextcord.Interaction):
        pass

    @legend.subcommand(name='day', description='Zeigt Legend-Statistiken eines Spielers für einen bestimmten Tag an.')
    async def legend_day(self, interaction: nextcord.Interaction, player_name: str, date: str = None):
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        player_tag = get_player_tag_by_name(player_name, self.players)
        if not player_tag:
            await interaction.response.send_message("Spieler nicht gefunden.", ephemeral=True)
            return

        legend_data, data = find_legend_data(player_tag, date)
        if not legend_data:
            await interaction.response.send_message(f"Keine Daten für den angegebenen Tag: {date}", ephemeral=True)
            return

        embed = create_legend_embed(player_name, player_tag, date, legend_data)
        await interaction.response.send_message(embed=embed)

    @legend.subcommand(name='season', description='Zeigt Legend-Statistiken eines Spielers für eine bestimmte Saison an.')
    async def legend_season(self, interaction: nextcord.Interaction, player_name: str, season: str = None):
        if not season:
            season = datetime.now().strftime('%Y-%m')

        player_tag = get_player_tag_by_name(player_name, self.players)
        if not player_tag:
            await interaction.response.send_message("Spieler nicht gefunden.", ephemeral=True)
            return

        season_data = find_season_legend_data(player_tag, season)
        if not season_data:
            await interaction.response.send_message(f"Keine Daten für die angegebene Saison: {season}", ephemeral=True)
            return

        embed = create_season_embed(player_name, player_tag, season, season_data)
        await interaction.response.send_message(embed=embed)

    @legend.subcommand(name='history', description='Zeigt die Historie der Saison-Statistiken eines Spielers an.')
    async def legend_history(self, interaction: nextcord.Interaction, player_name: str):
        player_tag = get_player_tag_by_name(player_name, self.players)
        if not player_tag:
            await interaction.response.send_message("Spieler nicht gefunden.", ephemeral=True)
            return

        history_data = await fetch_player_history(player_tag)
        if not history_data:
            await interaction.response.send_message(f"Keine historischen Daten für den Spieler: {player_name}", ephemeral=True)
            return

        embed = create_history_embed(player_name, player_tag, history_data)
        await interaction.response.send_message(embed=embed)

    @legend_day.on_autocomplete('player_name')
    @legend_season.on_autocomplete('player_name')
    @legend_history.on_autocomplete('player_name')
    async def autocomplete_player_name(self, interaction: nextcord.Interaction, current: str):
        suggestions = [player['name'] for player in self.players if current.lower() in player['name'].lower()]
        await interaction.response.send_autocomplete(suggestions)

def setup(bot):
    bot.add_cog(LegendStatsCog(bot))