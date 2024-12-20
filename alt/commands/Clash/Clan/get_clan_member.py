import nextcord
from nextcord.ext import commands
import requests
from COC.Api.api_header import api_header
from Assets.Emojis.townhall_emojis import townhall_emojis
from Assets.Emojis.league_emojis import league_emojis


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

class GetClanMemberCog(commands.Cog):
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

    @nextcord.slash_command(name='clanmembers', description='Listet die Mitglieder eines Clans auf')
    async def get_clan_members_command(self, interaction: nextcord.Interaction, clan_tag: str):
        try:
            clan_data = self.get_clan_data(clan_tag)
            members_data = self.get_clan_members(clan_tag)
            if 'items' in members_data:
                pages = []
                members = members_data['items']
                for i in range(0, len(members), 10):
                    embed = nextcord.Embed(title=f"Clan: {clan_data.get('name', 'N/A')}", description="Mitgliederliste", color=0x00ff00)
                    embed.set_thumbnail(url=clan_data.get("badgeUrls", {}).get("large"))
                    for member in members[i:i + 10]:
                        th_level_emoji = townhall_emojis.get(member['townHallLevel'], "")
                        league_emoji = league_emojis.get(member.get('league', {}).get('name', ''), "")
                        embed.add_field(name=member['name'], value=f"{th_level_emoji} {league_emoji} {member['trophies']}", inline=True)
                    embed.set_footer(text=f"Seite {i // 10 + 1}/{(len(members) - 1) // 10 + 1} - Mitglieder: {len(members)}")
                    pages.append(embed)
                paginator = PaginatorView(pages, len(members))
                await interaction.response.send_message(embed=pages[0], view=paginator)
            else:
                await interaction.response.send_message("Konnte keine Clanmitglieder finden.")
        except Exception as e:
            await interaction.response.send_message(f"Ein Fehler ist aufgetreten: {e}")

def setup(bot):
    bot.add_cog(GetClanMemberCog(bot))