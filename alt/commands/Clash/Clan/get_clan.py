import nextcord
from nextcord.ext import commands
import requests
from COC.Api.api_header import api_header 


class GetClanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_clan_data(self, clan_tag):
        url = f"https://api.clashofclans.com/v1/clans/%23{clan_tag.replace('#', '')}"
        headers = api_header()  # Verwende die importierte Funktion
        response = requests.get(url, headers=headers)
        return response.json()

    @nextcord.slash_command(name='clan', description='Erhalte Informationen zu einem Clan')
    async def get_clan(self, interaction: nextcord.Interaction, clan_tag: str):
        try:
            clan_data = self.get_clan_data(clan_tag)

            embed = nextcord.Embed(title=f"Clan: {clan_data.get('name', 'N/A')}", color=0x00ff00)
            embed.add_field(name="Clan-Level", value=clan_data.get("clanLevel", "N/A"), inline=True)
            embed.add_field(name="Mitglieder", value=f"{clan_data.get('members', 'N/A')}/50", inline=True)
            embed.add_field(name="Clan-Punkte", value=clan_data.get("clanPoints", "N/A"), inline=True)
            embed.add_field(name="Clan-Kriege gewonnen", value=clan_data.get("warWins", "N/A"), inline=True)
            embed.add_field(name="Clan-Kriegs-Siegessträhne", value=clan_data.get("warWinStreak", "N/A"), inline=True)
            embed.add_field(name="Clan-Kriegs-Liga", value=clan_data.get("warLeague", {}).get("name", "N/A"), inline=True)
            embed.add_field(name="Beschreibung", value=clan_data.get("description", "Keine Beschreibung vorhanden"), inline=False)
            embed.set_thumbnail(url=clan_data.get("badgeUrls", {}).get("large"))

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Ein Fehler ist aufgetreten: {e}")

def setup(bot):
    bot.add_cog(GetClanCog(bot))