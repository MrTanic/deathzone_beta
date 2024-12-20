import nextcord
from nextcord.ext import commands
import json
import os
from bot.setup.discord.server_ids import SERVER
from assets.emojis.warleague_emoji import warleague_emoji  # Import des Emoji-Dictionarys

# Funktion zum Laden der Clan-Informationen aus JSON-Dateien
def load_clan_info(clan_tag):
    try:
        with open(f"datenbank/clan/{clan_tag}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def get_clan_leader(members):
    for member in members:
        if member.get("role") == "Leader":
            return member.get("name", "Unbekannt")
    return "Unbekannt"

class ClanFamilyCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='clanfamilie', description='Zeigt Informationen über unsere Clanfamilie', guild_ids=SERVER)
    async def clanfamilie(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="DeathZone Clanfamilie",
            description="",
            color=0x00ff00
        )

        # Normale Clans
        normal_clans = {
            "~DeathZone~": "2JLQVYQ8",
            "DZ⚜Academy": "2P82CQQJL",
            "DZ⚜Immortality": "2P28YJ9L2",
            "DZ⚜Utopia": "28VYRC2R8"
        }

        # CWL-Clans
        cwl_clans = {
            "DZ⚜Afterlife": "22UYU90JL",
            "DZ⚜FighterZ": "2LRPVRCJ0"
        }

        # Event-Clan
        event_clan = {
            "~DeathZone~": "2LP29CJC9"
        }

        # Normale Clans hinzufügen
        for clan_name, clan_tag in normal_clans.items():
            clan_info = load_clan_info(clan_tag)
            if clan_info:
                war_league = clan_info.get("warLeague", {}).get("name", "Unbekannt")
                clan_level = clan_info.get("clanLevel", "Unbekannt")
                members = clan_info.get("memberList", [])
                leader = get_clan_leader(members)
                warleague_icon = warleague_emoji.get(war_league, "")
                embed.add_field(
                    name=f"{clan_name} | #{clan_tag}",
                    value=f"Clan Level: {clan_level}\nLeader: {leader}\n{warleague_icon} Liga: {war_league}\n[Clanprofil anzeigen](https://link.clashofclans.com/de?action=OpenClanProfile&tag={clan_tag})",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"{clan_name} | #{clan_tag}",
                    value="Informationen konnten nicht geladen werden.",
                    inline=False
                )

        # Überschrift für CWL-Clans mit angepassten Abständen
        embed.add_field(
            name="\u200b",
            value="**CWL-Clans**",
            inline=False
        )

        # CWL-Clans hinzufügen
        for clan_name, clan_tag in cwl_clans.items():
            clan_info = load_clan_info(clan_tag)
            if clan_info:
                war_league = clan_info.get("warLeague", {}).get("name", "Unbekannt")
                clan_level = clan_info.get("clanLevel", "Unbekannt")
                members = clan_info.get("memberList", [])
                leader = get_clan_leader(members)
                warleague_icon = warleague_emoji.get(war_league, "")
                embed.add_field(
                    name=f"{clan_name} | #{clan_tag}",
                    value=f"Clan Level: {clan_level}\nLeader: {leader}\n{warleague_icon} Liga: {war_league}\n[Clanprofil anzeigen](https://link.clashofclans.com/de?action=OpenClanProfile&tag={clan_tag})",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"{clan_name} | #{clan_tag}",
                    value="Informationen konnten nicht geladen werden.",
                    inline=False
                )

        # Überschrift für Event-Clan mit angepassten Abständen
        embed.add_field(
            name="\u200b",
            value="**Event-Clan**",
            inline=False
        )

        # Event-Clan hinzufügen
        for clan_name, clan_tag in event_clan.items():
            clan_info = load_clan_info(clan_tag)
            if clan_info:
                war_league = clan_info.get("warLeague", {}).get("name", "Unbekannt")
                clan_level = clan_info.get("clanLevel", "Unbekannt")
                members = clan_info.get("memberList", [])
                leader = get_clan_leader(members)
                warleague_icon = warleague_emoji.get(war_league, "")
                embed.add_field(
                    name=f"{clan_name} | #{clan_tag}",
                    value=f"Clan Level: {clan_level}\nLeader: {leader}\n{warleague_icon} Liga: {war_league}\n[Clanprofil anzeigen](https://link.clashofclans.com/de?action=OpenClanProfile&tag={clan_tag})",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"{clan_name} | #{clan_tag}",
                    value="Informationen konnten nicht geladen werden.",
                    inline=False
                )

        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(ClanFamilyCommand(bot))