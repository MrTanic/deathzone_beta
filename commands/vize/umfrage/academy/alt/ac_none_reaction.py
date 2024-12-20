import nextcord
from nextcord.ext import commands
import sqlite3
import os
import httpx
from bot.setup.discord.has_permissions import has_permission
from bot.setup.discord.channel_ids import AC_ANNOUNCEMENT_CHANNEL
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der webhook.env Datei
load_dotenv("bot/secret/webhook.env")

class AcNonResponderNotifierCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "datenbank/umfrage/academy/ac_cw_umfrage.db"
        self.member_db_path = "datenbank/member/academy_member.db"
        self.webhook_url = os.getenv("AC_RESPONDERS")

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def get_all_members(self):
        conn = sqlite3.connect(self.member_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM members")
        all_members = [row[0] for row in cursor.fetchall()]
        conn.close()
        return all_members

    async def send_webhook_notification(self, content):
        async with httpx.AsyncClient() as client:
            payload = {'content': content}
            await client.post(self.webhook_url, json=payload)

    @nextcord.slash_command(name='ac_notify_non_responders', description='Benachrichtigt Mitglieder, die nicht auf die Umfrage reagiert haben')
    async def notify_non_responders(self, interaction: nextcord.Interaction, message_id: str):
        user = interaction.user
        if not (has_permission(user, 'owner') or has_permission(user, 'acvize')):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return

        # Deferred response um Zeit für die Verarbeitung zu gewinnen
        await interaction.response.defer(ephemeral=True)

        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Mitglieder abrufen, die nicht auf die Umfrage reagiert haben
        cursor.execute("SELECT user_id FROM ac_cw_umfrage WHERE message_id = ? AND reaction = 'nicht reagiert'", (message_id,))
        non_responders = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not non_responders:
            await interaction.followup.send("Alle Mitglieder haben auf die Umfrage reagiert.", ephemeral=True)
            return

        # Nachricht mit erwähnten Mitgliedern erstellen
        mention_str = " ".join([f"<@{member_id}>" for member_id in non_responders])
        message_content = (
            f"Bitte auf die Umfrage reagieren: \n{mention_str}\n"
            f"Hier ist der Link zur Umfrage: \nhttps://discord.com/channels/{interaction.guild.id}/{AC_ANNOUNCEMENT_CHANNEL}/{message_id}"
        )

        # Nachricht an den Webhook senden
        await self.send_webhook_notification(content=message_content)

        # Bestätigungsnachricht an den Befehlsgeber senden
        await interaction.followup.send("Die Benachrichtigung wurde erfolgreich gesendet.", ephemeral=True)

def setup(bot):
    bot.add_cog(AcNonResponderNotifierCog(bot))