import nextcord
import sqlite3
import httpx
import os
from dotenv import load_dotenv
from bot.setup.discord.has_permissions import has_permission
from bot.setup.discord.channel_ids import DZ_ANNOUNCEMENT_CHANNEL

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv("bot/secret/webhook.env")

WEBHOOK_URL = os.getenv("DZ_RESPONDERS")

async def notify_non_responders(bot, interaction: nextcord.Interaction, message_id: str):
    user = interaction.user
    if not (has_permission(user, 'owner') or has_permission(user, 'dzvize')):
        await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
        return

    # Deferred response um Zeit für die Verarbeitung zu gewinnen
    await interaction.response.defer(ephemeral=True)

    db_path = "datenbank/umfrage/deathzone/dz_cw_umfrage.db"
    conn = sqlite3.connect(db_path)
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
    async with httpx.AsyncClient() as client:
        payload = {"content": content}
        await client.post(WEBHOOK_URL, json=payload)

    # Bestätigungsnachricht an den Befehlsgeber senden
    await interaction.followup.send("Die Benachrichtigung wurde erfolgreich gesendet.", ephemeral=True)