import sqlite3
import random
import httpx
import os
from dotenv import load_dotenv
from bot.setup.discord.has_permissions import has_permission

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv("bot/secret/webhook.env")

WEBHOOK_URL = os.getenv("DZ_CASTLE_FILLER")  # Ersetzen Sie dies mit dem Namen der Umgebungsvariablen für Ihren Webhook

def get_db_connection(db_path):
    return sqlite3.connect(db_path)

async def send_webhook_notification(content):
    async with httpx.AsyncClient() as client:
        payload = {"content": content}
        await client.post(WEBHOOK_URL, json=payload)

async def choose_castle_fillers(bot, interaction, message_id, number_of_fillers):
    user = interaction.user
    if not (has_permission(user, 'owner') or has_permission(user, 'dzvize')):
        await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
        return

    # Deferred response um Zeit für die Verarbeitung zu gewinnen
    await interaction.response.defer(ephemeral=True)

    db_path = "datenbank/umfrage/deathzone/dz_cw_umfrage.db"
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Mitglieder abrufen, die mit "Ja" reagiert haben
    cursor.execute("SELECT user_id FROM cw_umfragen WHERE message_id = ? AND reaction = 'ja'", (message_id,))
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
    await send_webhook_notification(content)

    # Bestätigungsnachricht an den Befehlsgeber senden
    await interaction.followup.send("Die Nachricht wurde erfolgreich gesendet.", ephemeral=True)