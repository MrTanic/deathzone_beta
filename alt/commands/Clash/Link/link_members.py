import nextcord
from nextcord.ext import commands
import requests
import sqlite3
from COC.Api.api_header import api_header
from Bot.Setup.Discord.has_permissions import has_permission


class LinkMembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def verify_coc_tag(self, coc_tag):
        url = f"https://api.clashofclans.com/v1/players/%23{coc_tag.lstrip('#')}"
        headers = api_header()
        response = requests.get(url, headers=headers)
        return response.status_code == 200

    @nextcord.slash_command(name='link', description='Verknüpft einen Discord-Account mit einem CoC-Account')
    async def linkcoc(self, interaction: nextcord.Interaction, user_id: str, coc_tag: str):
        # Berechtigungsüberprüfung
        if not (has_permission(interaction.user, 'owner') or 
                has_permission(interaction.user, 'dzvize') or 
                has_permission(interaction.user, 'acvize') or 
                has_permission(interaction.user, 'imvize') or 
                has_permission(interaction.user, 'utvize')):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung, um diesen Befehl auszuführen.", ephemeral=True)
            return

        # Überprüfen, ob der CoC-Tag gültig ist
        if not self.verify_coc_tag(coc_tag):
            await interaction.response.send_message(f"CoC-Account-Tag {coc_tag} ist ungültig.")
            return

        conn = sqlite3.connect('Datenbank/CoC_Accounts/Deathzone_Accounts.db')
        cursor = conn.cursor()

        # Überprüfen, ob der CoC-Account bereits verknüpft ist
        cursor.execute('SELECT user_id FROM member_links WHERE coc_tag = ?', (coc_tag,))
        if cursor.fetchone():
            await interaction.response.send_message(f"CoC-Account {coc_tag} ist bereits verknüpft.")
            conn.close()
            return

        # Fügt den neuen Eintrag in die Datenbank ein, wenn der Account noch nicht verknüpft ist
        cursor.execute('INSERT INTO member_links (user_id, coc_tag) VALUES (?, ?)', (user_id, coc_tag))
        conn.commit()
        conn.close()

        await interaction.response.send_message(f"CoC-Account {coc_tag} wurde erfolgreich mit Discord User ID {user_id} verknüpft.")

def setup(bot):
    bot.add_cog(LinkMembersCog(bot))