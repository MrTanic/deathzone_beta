import nextcord
from nextcord.ext import commands
from bot.setup.discord.server_ids import SERVER
from .vize.vize_help_view import VizeHelpView
from .owner.owner_help_view import OwnerHelpView
from .community.community_help_view import CommunityHelpView
from bot.setup.discord.has_permissions import has_permission
import json

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='help', description='Zeigt verschiedene Hilfsinformationen an', guild_ids=SERVER)
    async def help(self, interaction: nextcord.Interaction):
        pass

    @help.subcommand(name='vize', description='Zeigt Informationen für Vizes an.')
    async def help_vize(self, interaction: nextcord.Interaction):
        user = interaction.user
        if not (has_permission(user, 'owner') or 
                has_permission(user, 'dzvize') or 
                has_permission(user, 'acvize') or 
                has_permission(user, 'imvize') or 
                has_permission(user, 'utvize') or 
                has_permission(user, 'fzvize')):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return
        
        with open('commands/help/data/vize_help_info.json', 'r') as f:
            vize_info = json.load(f)

        einleitung = vize_info['einleitung']
        
        embed = nextcord.Embed(
            title="Vize Informationen",
            description=einleitung,
            color=0x32fcf6
        )
        
        view = VizeHelpView()
        await interaction.response.send_message(embed=embed, view=view)

    @help.subcommand(name='owner', description='Zeigt Informationen für Owner an.')
    async def help_owner(self, interaction: nextcord.Interaction):
        user = interaction.user
        if not has_permission(user, 'owner'):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return

        with open('commands/help/data/owner_help_info.json', 'r') as f:
            owner_info = json.load(f)

        einleitung = owner_info['einleitung']
        
        embed = nextcord.Embed(
            title="Owner Informationen",
            description=einleitung,
            color=0xff0000
        )

        view = OwnerHelpView()
        await interaction.response.send_message(embed=embed, view=view)

    @help.subcommand(name='community', description='Zeigt Informationen für die Community an.')
    async def help_community(self, interaction: nextcord.Interaction):
        with open('commands/help/data/community_help_info.json', 'r') as f:
            community_info = json.load(f)

        einleitung = community_info['einleitung']
        
        embed = nextcord.Embed(
            title="Community Informationen",
            description=einleitung,
            color=0x00ff00
        )

        view = CommunityHelpView()
        await interaction.response.send_message(embed=embed, view=view)

def setup(bot):
    bot.add_cog(HelpCommand(bot))