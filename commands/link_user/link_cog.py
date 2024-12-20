import nextcord
from nextcord.ext import commands
from bot.setup.discord.server_ids import SERVER
from .link_logic import link_user_with_tag, list_linked_users, delete_user, clans

class LinkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='link', description='Verwalte Verknüpfungen von Discord IDs mit Spieler Tags', guild_ids=SERVER)
    async def link(self, interaction: nextcord.Interaction):
        pass  # Hauptbefehl, der als Container für die Sub-Befehle dient

    @link.subcommand(name='create', description='Verknüpft eine Discord ID mit einem Spieler Tag')
    async def link_users(self, interaction: nextcord.Interaction, 
                         discord_id: str = nextcord.SlashOption(description="Die Discord ID oder @Erwähnung"),
                         player_tag: str = nextcord.SlashOption(description="Der Spieler Tag")):
        await link_user_with_tag(self.bot, interaction, discord_id, player_tag)

    @link.subcommand(name='list', description='Listet verknüpfte Spieler auf')
    async def list_link(self, interaction: nextcord.Interaction, 
                        clan: str = nextcord.SlashOption(
                            name="clan",
                            description="Wähle einen Clan aus",
                            choices=list(clans.keys())
                        )):
        clan_tag = clans[clan]
        await list_linked_users(self.bot, interaction, clan_tag)

    @link.subcommand(name='delete', description='Löscht eine Verknüpfung eines Spieler Tags')
    async def link_delete(self, interaction: nextcord.Interaction,
                          player_tag: str = nextcord.SlashOption(description="Der Spieler Tag")):
        await delete_user(self.bot, interaction, player_tag)

def setup(bot):
    bot.add_cog(LinkCog(bot))