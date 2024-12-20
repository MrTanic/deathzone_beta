# nicht hinzugefügt
import nextcord
from nextcord.ext import commands
import sqlite3
import requests
import logging
from COC.Api.api_header import api_header
from Bot.Setup.Discord.has_permissions import has_permission

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO)

class PaginatorButton(nextcord.ui.Button):
    def __init__(self, label, style, direction, paginator_view):
        super().__init__(label=label, style=style)
        self.direction = direction
        self.paginator_view = paginator_view

    async def callback(self, interaction: nextcord.Interaction):
        await self.paginator_view.change_page(self.direction)

class PaginatorView(nextcord.ui.View):
    def __init__(self, embeds, timeout=300):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.current_page = 0
        self.message = None
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        if self.current_page > 0:
            self.add_item(PaginatorButton(label="Zurück", style=nextcord.ButtonStyle.grey, direction="back", paginator_view=self))
        if self.current_page < len(self.embeds) - 1:
            self.add_item(PaginatorButton(label="Weiter", style=nextcord.ButtonStyle.grey, direction="next", paginator_view=self))

    async def change_page(self, direction):
        if direction == "back" and self.current_page > 0:
            self.current_page -= 1
        elif direction == "next" and self.current_page < len(self.embeds) - 1:
            self.current_page += 1
        await self.message.edit(embed=self.embeds[self.current_page], view=self)
        self.update_buttons()

    async def on_timeout(self):
        if self.message:
            await self.message.edit(view=None)

class AcJaReactionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.umfrage_db_path = "Datenbank/Umfrage_DB/Academy/ac_cw_umfrage.db"
        self.accounts_db_path = "Datenbank/Link_DB/Deathzone_Accounts.db"
        self.clan_tag = "#2P82CQQJL"

    def get_clan_data(self, clan_tag):
        try:
            url = f"https://api.clashofclans.com/v1/clans/%23{clan_tag.replace('#', '')}"
            headers = api_header()
            response = requests.get(url, headers=headers)
            return response.json()
        except Exception as e:
            logging.exception("Fehler beim Abrufen von Clan-Daten: %s", e)
            return {}

    def get_clan_members(self, clan_tag):
        try:
            url = f"https://api.clashofclans.com/v1/clans/%23{clan_tag.replace('#', '')}/members"
            headers = api_header()
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return {member['tag']: member['name'] for member in response.json().get('items', [])}
            return {}
        except Exception as e:
            logging.exception("Fehler beim Abrufen von Clan-Mitgliedern: %s", e)
            return {}

    def get_linked_accounts(self, user_id):
        try:
            conn = sqlite3.connect(self.accounts_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT coc_tag FROM member_links WHERE user_id = ?", (user_id,))
            linked_accounts = cursor.fetchall()
            conn.close()
            return [tag[0] for tag in linked_accounts]
        except Exception as e:
            logging.exception("Fehler beim Abrufen verknüpfter Accounts: %s", e)
            return []

    @nextcord.slash_command(name='ac_ja_reaktionen', description='Zeigt Server-Nicknames und verknüpfte CoC-Namen, die mit Ja reagiert haben und im Clan sind')
    async def show_yes_reactions(self, interaction: nextcord.Interaction, message_id: str):
        if not (has_permission(interaction.user, 'owner') or has_permission(interaction.user, 'acvize')):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return

        try:
            guild = interaction.guild
            clan_members = self.get_clan_members(self.clan_tag)

            conn = sqlite3.connect(self.umfrage_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM ac_cw_umfrage WHERE message_id = ? AND reaction = 'ja'", (message_id,))
            yes_user_ids = cursor.fetchall()
            conn.close()

            if not yes_user_ids:
                await interaction.response.send_message("Keine Ja-Reaktionen für die angegebene Nachrichten-ID gefunden.", ephemeral=True)
                return

            total_discord_users = len(yes_user_ids)
            total_linked_accounts = 0
            embed_pages = []
            for i in range(0, len(yes_user_ids), 10):
                embed = nextcord.Embed(title="Ja-Reaktionen im Clan", description="Nutzer, die mit Ja reagiert haben und im Clan sind", color=2141262)
                for user_id_tuple in yes_user_ids[i:i + 10]:
                    user_id = user_id_tuple[0]
                    member = guild.get_member(int(user_id))
                    server_nickname = member.display_name if member else "Unbekannter Nutzer"
                    linked_accounts = self.get_linked_accounts(user_id)
                    total_linked_accounts += len(linked_accounts)
                    clan_account_names = [clan_members.get(account, "Unbekannter Account") for account in linked_accounts if account in clan_members]
                    accounts_list = ", ".join(clan_account_names) if clan_account_names else "Keine verknüpften Accounts im Clan"
                    embed.add_field(name=server_nickname, value=f"Verknüpfte CoC-Accounts: {accounts_list}", inline=False)
                page_info = f"Seite {i // 10 + 1}/{(len(yes_user_ids) - 1) // 10 + 1}"
                user_info = f"Discord User mit Ja: {total_discord_users}, Verknüpfte CoC-Accounts: {total_linked_accounts}"
                embed.set_footer(text=f"{page_info} - {user_info}")
                embed_pages.append(embed)

            paginator_view = PaginatorView(embed_pages)
            message = await interaction.response.send_message(embed=embed_pages[0], view=paginator_view)
            paginator_view.message = message
        except Exception as e:
            logging.exception("Fehler bei der Anzeige der Ja-Reaktionen: %s", e)
            await interaction.response.send_message("Ein Fehler ist aufgetreten. Bitte versuche es später noch einmal.", ephemeral=True)

def setup(bot):
    bot.add_cog(AcJaReactionCog(bot))