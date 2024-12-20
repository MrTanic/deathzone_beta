import nextcord
from nextcord.ext import commands
import json
from bot.setup.discord.server_ids import SERVER
from deathzone.clan_tags import clan_tags  # Import der Clan-Tags

# Funktion zum Laden der Clan-Informationen aus JSON-Dateien
def load_clan_info(clan_tag):
    try:
        clan_tag_clean = clan_tag.replace("#", "")
        with open(f"datenbank/clan/{clan_tag_clean}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

class ClanOverviewCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='overview', description='Zeigt eine Übersicht über die Mitglieder der gesamten Clanfamilie', guild_ids=SERVER)
    async def overview(self, interaction: nextcord.Interaction):
        total_members = 0
        embed = nextcord.Embed(
            title="Clan-Familienübersicht",
            description="",
            color=0x00ff00
        )

        # Clan Mitglieder zählen und in Embed einfügen
        clan_member_counts = []

        for clan_name, clan_tag in clan_tags.items():
            clan_info = load_clan_info(clan_tag)
            if clan_info:
                member_count = clan_info.get("members", 0)
                total_members += member_count
                clan_member_counts.append((clan_name, clan_tag, member_count))
            else:
                clan_member_counts.append((clan_name, clan_tag, "Informationen konnten nicht geladen werden."))

        # Gesamtmitgliederzahl hinzufügen
        embed.add_field(
            name="Gesamtmitglieder",
            value=f"Alle Mitglieder: {total_members}",
            inline=False
        )

        # Einzelne Clans hinzufügen
        for clan_name, clan_tag, member_count in clan_member_counts:
            embed.add_field(
                name=f"{clan_name} | {clan_tag}",
                value=f"Mitglieder: {member_count}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(ClanOverviewCog(bot))