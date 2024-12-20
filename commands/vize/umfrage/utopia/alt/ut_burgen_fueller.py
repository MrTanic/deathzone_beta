import nextcord
from nextcord.ext import commands
import sqlite3
import random
import os
from dotenv import load_dotenv
import httpx
from bot.setup.discord.has_permissions import has_permission

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv("bot/secret/webhook.env")

WEBHOOK_URL = os.getenv("UT_CASTLE_FILLER")

class UtRandomCastleFillerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "datenbank/umfrage/utopia/ut_cw_umfrage.db"

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    async def send_webhook_notification(self, content):
        async with httpx.AsyncClient() as client:
            payload = {"content": content}
            await client.post(WEBHOOK_URL, json=payload)

    @nextcord.slash_command(name='ut_choose_castle_fillers', description='Wählt zufällig Mitglieder aus, die mit "Ja" reagiert haben')
    async def choose_castle_fillers(self, interaction: nextcord.Interaction, message_id: str, number_of_fillers: int):
        user = interaction.user
        if not (has_permission(user, 'owner') or has_permission(user, 'utvize')):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return

        # Deferred response um Zeit für die Verarbeitung zu gewinnen
        await interaction.response.defer(ephemeral=True)
        
        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Mitglieder abrufen, die mit "Ja" reagiert haben
        cursor.execute("SELECT user_id FROM ut_cw_umfrage WHERE message_id = ? AND reaction = 'ja'", (message_id,))
        members_who_said_yes = cursor.fetchall()
        conn.close()

        if not members_who_said_yes:
            await interaction.followup.send("Keine Mitglieder gefunden, die mit 'Ja' reagiert haben.", ephemeral=True)
            return

        # Zufällig Mitglieder auswählen
        selected_members = random.sample(members_who_said_yes, min(number_of_fillers, len(members_who_said_yes)))
        selected_member_ids = [member[0] for member in selected_members]

        # Nachricht mit erwähnten Mitgliedern erstellen
        mention_str = " ".join([f"<@{member_id}>" for member_id in selected_member_ids])
        content = f"Bitte die Burgen füllen für den CW: \n{mention_str}"

        # Nachricht an den Webhook senden
        await self.send_webhook_notification(content)

        # Bestätigungsnachricht an den Befehlsgeber senden
        await interaction.followup.send("Die Mitglieder wurden erfolgreich benachrichtigt.", ephemeral=True)

def setup(bot):
    bot.add_cog(UtRandomCastleFillerCog(bot))