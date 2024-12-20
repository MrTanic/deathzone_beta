import nextcord
from nextcord.ext import commands
import json
import os
from bot.setup.discord.server_ids import SERVER
from bot.setup.discord.has_permissions import has_permission  # Import der has_permission-Funktion
from deathzone.player_tags import player_tags  # Import der player_tags

# Basisverzeichnis für Clan-JSON-Dateien
CLAN_DATA_DIR = "datenbank/clan"

# Datei, in der die Spielernamen aktualisiert werden sollen
PLAYERS_FILE = "deathzone/players.json"

# Funktion zum Laden der Clan-JSON-Dateien
def load_clan_files():
    clan_files = {}
    for filename in os.listdir(CLAN_DATA_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(CLAN_DATA_DIR, filename), "r") as file:
                clan_data = json.load(file)
                clan_files[filename] = clan_data
    return clan_files

# Funktion zum Laden der players.json-Datei
def load_players_file():
    with open(PLAYERS_FILE, "r") as file:
        return json.load(file)

# Funktion zum Speichern der players.json-Datei
def save_players_file(players):
    with open(PLAYERS_FILE, "w") as file:
        json.dump(players, file, indent=4)

# Funktion zum Aktualisieren der Spielerdaten in der players.json
def update_player_names():
    clan_files = load_clan_files()
    players = load_players_file()
    
    tag_name_map = {}

    for clan_data in clan_files.values():
        for member in clan_data.get("memberList", []):
            if member['tag'] in player_tags:  # Hier werden die player_tags aus der Datei verwendet
                tag_name_map[member['tag']] = member['name']

    for player in players:
        if player['tag'] in tag_name_map:
            player['name'] = tag_name_map[player['tag']]
    
    save_players_file(players)
    print("Spielernamen erfolgreich aktualisiert.")

class UpdatePlayerNamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='update_players', description='Aktualisiert die Spielernamen basierend auf den Clan-Daten.', guild_ids=SERVER)
    async def update_players(self, interaction: nextcord.Interaction):
        if has_permission(interaction.user, 'owner'):
            update_player_names()
            await interaction.response.send_message("Spielernamen erfolgreich aktualisiert.")
        else:
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

def setup(bot):
    bot.add_cog(UpdatePlayerNamesCog(bot))