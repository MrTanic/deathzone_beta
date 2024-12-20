import nextcord
from nextcord.ext import commands
from bot.setup.discord.server_ids import BOT_SERVER_ID
from bot.setup.discord.has_permissions import has_permission

class TriggerUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='trigger_update', description='Stößt die Aktualisierung der Mitglieder-Datenbank manuell an', guild_ids=[BOT_SERVER_ID])
    async def trigger_update(self, interaction: nextcord.Interaction):
        # Berechtigungsüberprüfung für den Owner
        if not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du bist nicht berechtigt, diesen Befehl auszuführen.", ephemeral=True)
            return

        status_channel = self.bot.get_channel(STATUS_CHANNEL_ID)
        if status_channel:
            await status_channel.send("Manuelle Aktualisierung der Mitglieder-Datenbank gestartet...")

        # Überprüfen, ob der Task läuft und ggf. stoppen
        member_update_cog = self.bot.get_cog('MemberUpdateCog')
        if member_update_cog and member_update_cog.update_member_db.is_running():
            member_update_cog.update_member_db.stop()

        # Manuelle Ausführung des Tasks
        await member_update_cog.update_member_db()

        # Task wieder starten, falls er nicht läuft
        if member_update_cog and not member_update_cog.update_member_db.is_running():
            member_update_cog.update_member_db.start()

        if status_channel:
            await status_channel.send("Manuelle Aktualisierung der Mitglieder-Datenbank abgeschlossen.")

def setup(bot):
    bot.add_cog(TriggerUpdateCog(bot))