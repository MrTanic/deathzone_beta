import nextcord
from nextcord.ext import commands
import sqlite3
import random
import httpx
from dotenv import load_dotenv
import os
from bot.setup.discord.server_ids import SERVER
from bot.setup.discord.has_permissions import has_permission

# Laden der Webhook-URL aus der .env Datei
load_dotenv('bot/secret/webhook.env')
WEBHOOK_URL = os.getenv('AC_CASTLE_FILLER')



class AcRandomCastleFillerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "datenbank/umfrage/academy/ac_cw_umfrage.db"  # Pfad zur Datenbank für Academy anpassen

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    async def send_webhook_notification(self, content=None, embed=None):
        async with httpx.AsyncClient() as client:
            payload = {}
            if content:
                payload['content'] = content
            if embed:
                payload['embeds'] = [embed.to_dict()]
            await client.post(WEBHOOK_URL, json=payload)

    @nextcord.slash_command(name='ac_castle_fillers', description='Wählt zufällig Mitglieder aus, die mit "Ja" reagiert haben')
    async def choose_castle_fillers(self, interaction: nextcord.Interaction, message_id: str, number_of_fillers: int):
        user = interaction.user
        if not (has_permission(user, 'owner') or has_permission(user, 'acvize')):  # Berechtigungen für Academy anpassen
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return

        # Deferred response um Zeit für die Verarbeitung zu gewinnen
        await interaction.response.defer(ephemeral=True)
        
        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Mitglieder abrufen, die mit "Ja" reagiert haben
        cursor.execute("SELECT user_id FROM ac_cw_umfrage WHERE message_id = ? AND reaction = 'ja'", (message_id,))
        members_who_said_yes = cursor.fetchall()
        conn.close()

        if not members_who_said_yes:
            await interaction.followup.send("Keine Mitglieder gefunden, die mit 'Ja' reagiert haben.", ephemeral=True)
            return

        # Zufällig Mitglieder auswählen
        selected_members = random.sample(members_who_said_yes, min(number_of_fillers, len(members_who_said_yes)))
        selected_member_ids = [member[0] for member in selected_members]

        # Nachricht mit erwähnten Mitgliedern senden
        mention_str = " ".join([f"<@{member_id}>" for member_id in selected_member_ids])
        await self.send_webhook_notification(content=f"Bitte die Burgen füllen für den CW: \n{mention_str}")

        # Bestätigungsnachricht an den Befehlsgeber senden
        await interaction.followup.send("Die Mitglieder wurden erfolgreich benachrichtigt.", ephemeral=True)

def setup(bot):
    bot.add_cog(AcRandomCastleFillerCog(bot))