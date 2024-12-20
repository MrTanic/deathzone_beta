import nextcord
from nextcord.ext import commands
from bot.setup.discord.server_ids import SERVER
from .clan_data import load_clan_info, clans
from .clan_embed import create_clan_embed, ClanProfileButtons, create_clan_members_embed

class ClanInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='clan', description='Hauptkommando für Clan-Informationen', guild_ids=SERVER)
    async def clan(self, interaction: nextcord.Interaction):
        pass

    @clan.subcommand(name='info', description='Zeigt Informationen über einen Clan')
    async def clan_info(self, interaction: nextcord.Interaction, clan: str = nextcord.SlashOption(name="clan", choices=list(clans.keys()))):
        clan_tag = clans[clan]
        clan_info = load_clan_info(clan_tag)
        if not clan_info:
            await interaction.response.send_message("Clan-Informationen konnten nicht geladen werden.", ephemeral=True)
            return

        embed = create_clan_embed(clan_info)
        view = ClanProfileButtons(clan_tag, clan.replace(" ", "%20").replace("⚜", ""))

        await interaction.response.send_message(embed=embed, view=view)

    @clan.subcommand(name='member', description='Zeigt die Mitglieder eines Clans')
    async def clan_member(self, interaction: nextcord.Interaction, clan: str = nextcord.SlashOption(name="clan", choices=list(clans.keys()))):
        clan_tag = clans[clan]
        clan_info = load_clan_info(clan_tag)
        members = clan_info.get("memberList", [])
        if not members:
            await interaction.response.send_message("Clan-Mitglieder konnten nicht geladen werden.", ephemeral=True)
            return

        embed = create_clan_members_embed(members)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(ClanInfoCommand(bot))