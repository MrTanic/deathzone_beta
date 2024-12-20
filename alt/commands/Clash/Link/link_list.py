import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
import requests
from COC.Api.api_header import api_header
import sqlite3
from Bot.Setup.Discord.has_permissions import has_permission

SERVER_ID = 884325196104884248

class PaginatorButton(nextcord.ui.Button):
    def __init__(self, label, style, direction, paginator_view):
        super().__init__(label=label, style=style)
        self.direction = direction
        self.paginator_view = paginator_view

    async def callback(self, interaction: nextcord.Interaction):
        if self.direction == "back" and self.paginator_view.current_page > 0:
            self.paginator_view.current_page -= 1
        elif self.direction == "next" and self.paginator_view.current_page < len(self.paginator_view.pages) - 1:
            self.paginator_view.current_page += 1
        self.paginator_view.update_buttons()
        await interaction.response.edit_message(embed=self.paginator_view.pages[self.paginator_view.current_page], view=self.paginator_view)

class PaginatorView(nextcord.ui.View):
    def __init__(self, pages, total_members):
        super().__init__()
        self.pages = pages
        self.current_page = 0
        self.total_members = total_members
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        if self.current_page > 0:
            self.add_item(PaginatorButton(label="Zurück", style=nextcord.ButtonStyle.grey, direction="back", paginator_view=self))
        if self.current_page < len(self.pages) - 1:
            self.add_item(PaginatorButton(label="Weiter", style=nextcord.ButtonStyle.grey, direction="next", paginator_view=self))
        self.update_footer()

    def update_footer(self):
        footer_text = f"Seite {self.current_page + 1}/{len(self.pages)} - Mitglieder: {self.total_members}"
        for page in self.pages:
            page.set_footer(text=footer_text)

class LinkListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_clan_data(self, clan_tag):
        url = f"https://api.clashofclans.com/v1/clans/%23{clan_tag.replace('#', '')}"
        headers = api_header()
        response = requests.get(url, headers=headers)
        return response.json()

    def get_clan_members(self, clan_tag):
        url = f"https://api.clashofclans.com/v1/clans/%23{clan_tag.replace('#', '')}/members"
        headers = api_header()
        response = requests.get(url, headers=headers)
        return response.json()
    
    
    @nextcord.slash_command(name='link_list', description='Listet die Mitglieder eines Clans auf')
    async def get_clan_members_command(self, interaction: nextcord.Interaction, clan_tag: str = nextcord.SlashOption(
        choices={
            "Deathzone": "#2JLQVYQ8",
            "Academy": "#2P82CQQJL",
            "Immortality": "#2P28YJ9L2",
            "Utopia": "#28VYRC2R8"
        },
        description="Wähle einen Clan aus"
    )):
     user = interaction.user
     if not (has_permission(user, 'owner') or has_permission(user, 'dzvize') or 
            has_permission(user, 'acvize') or has_permission(user, 'imvize') or
            has_permission(user, 'utvize')):
        await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
        return

     try:
        guild = self.bot.get_guild(SERVER_ID)
        if not guild:
            await interaction.response.send_message("Server nicht gefunden.")
            return

        clan_data = self.get_clan_data(clan_tag)
        members_data = self.get_clan_members(clan_tag)
        if 'items' in members_data:
            conn = sqlite3.connect('Datenbank/CoC_Accounts/Deathzone_Accounts.db')
            cursor = conn.cursor()
            pages = []
            members = members_data['items']
            for i in range(0, len(members), 10):
                embed = nextcord.Embed(title=f"Clan: {clan_data.get('name', 'N/A')}", description="Mitgliederliste", color=0x00ff00)
                embed.set_thumbnail(url=clan_data.get("badgeUrls", {}).get("large"))
                for member in members[i:i + 10]:
                    coc_tag = member.get("tag")
                    cursor.execute('SELECT user_id FROM member_links WHERE coc_tag = ?', (coc_tag,))
                    result = cursor.fetchone()
                    if result:
                        discord_member = guild.get_member(int(result[0]))
                        discord_nickname = discord_member.display_name if discord_member else "Unbekannter Nutzer"
                    else:
                        discord_nickname = "Nicht verknüpft"
                    embed.add_field(name=member['name'], value=f"Tag: {coc_tag}, Discord: {discord_nickname}", inline=True)
                pages.append(embed)
            paginator = PaginatorView(pages, len(members))
            await interaction.response.send_message(embed=pages[0], view=paginator)
            conn.close()
        else:
            await interaction.response.send_message("Konnte keine Clanmitglieder finden.")
     except Exception as e:
        await interaction.response.send_message(f"Ein Fehler ist aufgetreten: {e}")
            

def setup(bot):
    bot.add_cog(LinkListCog(bot))