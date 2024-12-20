import nextcord
from nextcord.ext import commands
from bot.setup.discord.has_permissions import has_permission
from bot.setup.discord.server_ids import SERVER
from .dz_cwl_logic import save_and_evaluate_cwl
from .dz_cwl_announcement_logic import announce_cwl
from .dz_cwl_response import notify_non_responders  # Import der notify Funktion

class DzCWLCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='dz_cwl_announcement', description='Sendet eine Ankündigung für die kommende CWL', guild_ids=SERVER)
    async def cwl_announcement(self, interaction: nextcord.Interaction):
        if not has_permission(interaction.user, 'dzvize') and not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
            return

        await announce_cwl(self.bot, interaction)
        await interaction.response.send_message("CWL Ankündigung wurde manuell im Kanal gesendet.", ephemeral=True)

    @nextcord.slash_command(name='dz_cwl_evaluate', description='Erstellt ein Embed aus den CWL-Reaktionen', guild_ids=SERVER)
    async def cwl_evaluate(self, interaction: nextcord.Interaction, message_id: str):
        if not has_permission(interaction.user, 'dzvize') and not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
            return

        await interaction.response.defer()
        await save_and_evaluate_cwl(self.bot, interaction, message_id)

    @nextcord.slash_command(name='dz_cwl_notify', description='Benachrichtigt Mitglieder, die nicht auf die CWL-Umfrage reagiert haben', guild_ids=SERVER)
    async def cwl_notify(self, interaction: nextcord.Interaction, message_id: str):
        if not has_permission(interaction.user, 'dzvize') and not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
            return

        await notify_non_responders(self.bot, interaction, message_id)

def setup(bot):
    bot.add_cog(DzCWLCommand(bot))