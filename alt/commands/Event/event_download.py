import nextcord
from nextcord.ext import commands
import json
import csv
import os

class EventDownloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='download_registrations', description='Lade die Event-Registrierungen herunter.')
    async def download_registrations(self, interaction: nextcord.Interaction):
        event_manager_role_id = 1189594120335933530  # Die tatsächliche Rolle-ID

        if not any(role.id == event_manager_role_id for role in interaction.user.roles):
            await interaction.response.send_message('Du hast nicht die erforderliche Berechtigung, um diesen Befehl auszuführen.', ephemeral=True)
            return

        if not os.path.exists('event_registrations.json'):
            await interaction.response.send_message('Es gibt noch keine Registrierungen.', ephemeral=True)
            return

        with open('event_registrations.json', 'r', encoding='utf-8') as json_file:
            registrations = json.load(json_file)

        csv_file_path = 'event_registrations.csv'
        with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Spielername', 'Spieler-Tag', 'Discord ID'])
            for registration in registrations:
                encoded_name = registration['player_name'].encode('utf-8-sig', 'ignore').decode('utf-8-sig')
                discord_mention = f"<@{registration['discord_id']}>"
                writer.writerow([encoded_name, registration['player_tag'], discord_mention])

        with open(csv_file_path, 'rb') as csv_file:
            await interaction.response.send_message('Hier sind die Event-Registrierungen:', file=nextcord.File(csv_file, 'event_registrations.csv'))

def setup(bot):
    bot.add_cog(EventDownloadCog(bot))