import nextcord
from nextcord.ext import commands
from bot.setup.discord.has_permissions import has_permission
from bot.setup.discord.server_ids import SERVER  # Importiere die SERVER-Liste
from .player_tags_utils import load_player_tags, save_player_tags, load_clan_files, save_players_file, load_players_file

class PlayerTagsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player_tags = load_player_tags()

    @nextcord.slash_command(name='playertags', description='Verwalte die Player-Tags', guild_ids=SERVER)
    async def player_tags(self, interaction: nextcord.Interaction):
        pass

    @player_tags.subcommand(name='add', description='Füge einen neuen Player-Tag hinzu')
    async def add_player_tag(self, interaction: nextcord.Interaction, tag: str):
        if not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)
            return

        if tag in self.player_tags:
            await interaction.response.send_message(f"Der Player-Tag {tag} ist bereits in der Liste.", ephemeral=True)
            return

        self.player_tags.append(tag)
        save_player_tags(self.player_tags)
        await interaction.response.send_message(f"Der Player-Tag {tag} wurde hinzugefügt.")

    @player_tags.subcommand(name='list', description='Zeige alle Player-Tags an')
    async def list_player_tags(self, interaction: nextcord.Interaction):
        if not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)
            return

        players = load_players_file()
        tags_list = "\n".join([f"{player['name']} ({player['tag']})" for player in players])
        await interaction.response.send_message(f"Player-Tags:\n{tags_list}")

    @player_tags.subcommand(name='delete', description='Lösche einen Player-Tag')
    async def delete_player_tag(self, interaction: nextcord.Interaction, tag: str):
        if not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)
            return

        if tag not in self.player_tags:
            await interaction.response.send_message(f"Der Player-Tag {tag} ist nicht in der Liste.", ephemeral=True)
            return

        self.player_tags.remove(tag)
        save_player_tags(self.player_tags)
        await interaction.response.send_message(f"Der Player-Tag {tag} wurde gelöscht.")

    @player_tags.subcommand(name='update', description='Aktualisiert die Spielernamen basierend auf den Clan-Daten.')
    async def update_player_names(self, interaction: nextcord.Interaction):
        if not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)
            return

        clan_files = load_clan_files()
        updated_players = []

        for tag in self.player_tags:
            player_found = False
            for clan_data in clan_files.values():
                for member in clan_data.get("memberList", []):
                    if member['tag'] == tag:
                        updated_players.append({"name": member['name'], "tag": member['tag']})
                        player_found = True
                        break
                if player_found:
                    break
            if not player_found:
                updated_players.append({"name": "Unknown", "tag": tag})  # Falls der Name nicht gefunden wird, mit "Unknown" speichern

        save_players_file(updated_players)
        await interaction.response.send_message("Spielernamen erfolgreich aktualisiert.")

def setup(bot):
    bot.add_cog(PlayerTagsCog(bot))