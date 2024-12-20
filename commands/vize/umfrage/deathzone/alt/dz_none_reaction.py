import nextcord
from nextcord.ext import commands
import sqlite3
import httpx
import os
from dotenv import load_dotenv
from bot.setup.discord.has_permissions import has_permission
from bot.setup.discord.channel_ids import DZ_ANNOUNCEMENT_CHANNEL

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv("bot/secret/webhook.env")

WEBHOOK_URL = os.getenv("DZ_RESPONDERS")  # Ersetzen Sie dies mit dem Namen der Umgebungsvariablen für Ihren Webhook

class DzNonResponderNotifierCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "datenbank/umfrage/deathzone/dz_cw_umfrage.db"
        self.member_db_path = "datenbank/member/deathzone_member.db"

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
            payload = {"content": content}
            await client.post(WEBHOOK_URL, json=payload)

    @nextcord.slash_command(name='dz_notify_non_responders', description='Benachrichtigt Mitglieder, die nicht auf die Umfrage reagiert haben')
    async def notify_non_responders(self, interaction: nextcord.Interaction, message_id: str):
        user = interaction.user
        if not (has_permission(user, 'owner') or has_permission(user, 'dzvize')):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return

        # Deferred response um Zeit für die Verarbeitung zu gewinnen
        await interaction.response.defer(ephemeral=True)

        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Mitglieder abrufen, die nicht auf die Umfrage reagiert haben
        cursor.execute("SELECT user_id FROM cw_umfragen WHERE message_id = ? AND reaction = 'nicht reagiert'", (message_id,))
        non_responders = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not non_responders:
            await interaction.followup.send("Alle Mitglieder haben auf die Umfrage reagiert.", ephemeral=True)
            return

        # Nachricht mit erwähnten Mitgliedern erstellen
        mention_str = " ".join([f"<@{member_id}>" for member_id in non_responders])
        content = (
            f"Bitte auf die Umfrage reagieren: \n{mention_str}\n"
            f"Hier ist der Link zur Umfrage: \nhttps://discord.com/channels/{interaction.guild.id}/{DZ_ANNOUNCEMENT_CHANNEL}/{message_id}"
        )

        # Nachricht an den Webhook senden
        await self.send_webhook_notification(content)

        # Bestätigungsnachricht an den Befehlsgeber senden
        await interaction.followup.send("Die Benachrichtigung wurde erfolgreich gesendet.", ephemeral=True)

def setup(bot):
    bot.add_cog(DzNonResponderNotifierCog(bot))