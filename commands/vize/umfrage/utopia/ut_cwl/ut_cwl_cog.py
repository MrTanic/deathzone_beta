import nextcord
from nextcord.ext import commands
from bot.setup.discord.server_ids import SERVER
from bot.setup.discord.has_permissions import has_permission
from .ut_cwl_logic import save_and_evaluate_ut_cwl
from .ut_cwl_announcement import announce_ut_cwl

class UTCWLCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='ut_cwl', description='Verwalte Utopia CWL Operationen', guild_ids=SERVER)
    async def ut_cwl(self, interaction: nextcord.Interaction):
        pass  # Hauptbefehl, der als Container für die Sub-Befehle dient

    @ut_cwl.subcommand(name='announcement', description='Sendet eine Ankündigung für die kommende CWL')
    async def ut_cwl_announcement(self, interaction: nextcord.Interaction):
        if not has_permission(interaction.user, 'utvize') and not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
            return

        await announce_ut_cwl(self.bot, interaction)
        await interaction.response.send_message("CWL Ankündigung wurde manuell im Kanal gesendet.", ephemeral=True)

    @ut_cwl.subcommand(name='auswertung', description='Zeigt die Auswertung der Reaktionen auf die CWL-Ankündigung')
    async def ut_cwl_auswertung(self, interaction: nextcord.Interaction, message_id: str):
        if not has_permission(interaction.user, 'utvize') and not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
            return

        await interaction.response.defer()
        await save_and_evaluate_ut_cwl(self.bot, interaction, message_id)

def setup(bot):
    bot.add_cog(UTCWLCommand(bot))