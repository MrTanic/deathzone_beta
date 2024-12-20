import nextcord
from nextcord.ext import commands
import sqlite3
from bot.setup.discord.server_ids import SERVER
from bot.setup.discord.has_permissions import has_permission


class WarningStrikeView(nextcord.ui.View):
    def __init__(self, cog, user_warnings, clan_name, current_page, max_pages):
        super().__init__(timeout=180)
        self.cog = cog
        self.user_warnings = user_warnings
        self.clan_name = clan_name
        self.current_page = current_page
        self.max_pages = max_pages
        self.message = None

    @nextcord.ui.button(label="Back", style=nextcord.ButtonStyle.grey)
    async def previous_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            embeds = self.cog.create_warning_embeds(self.user_warnings, self.clan_name)
            embed = self.cog.create_warning_embeds(self.user_warnings, self.clan_name)[self.current_page]
            await interaction.response.edit_message(embed=embed, view=self)

    @nextcord.ui.button(label="Next", style=nextcord.ButtonStyle.grey)
    async def next_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            embeds = self.cog.create_warning_embeds(self.user_warnings, self.clan_name)
            embed = self.cog.create_warning_embeds(self.user_warnings, self.clan_name)[self.current_page]
            await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        if self.message:
            await self.message.edit(view=None)

class WarningStrikeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "datenbank/strikes/warning_strike.db"

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @nextcord.slash_command(name='add_strike', description='Fügt einem Mitglied einen Strike hinzu', guild_ids=SERVER)
    async def add_strike(self, interaction: nextcord.Interaction, 
                         user_id: str, 
                         clan_name: str = nextcord.SlashOption(required=True, choices={"Deathzone": "Deathzone", "Academy": "Academy", "Immortality": "Immortality", "Utopia": "Utopia"}, description="Wähle einen Clan aus"),
                         reason: str = nextcord.SlashOption(required=True, description="Grund für den Strike")):
        
        if not (has_permission(interaction.user, 'owner') or has_permission(interaction.user, 'dzvize') or has_permission(interaction.user, 'acvize') or has_permission(interaction.user, 'imvize') or has_permission(interaction.user, 'utvize')):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO member_warnings (user_id, clan_name, strikes, reason) VALUES (?, ?, 1, ?)", (user_id, clan_name, reason))
        conn.commit()
        conn.close()
        await interaction.response.send_message(f"Strike für User-ID {user_id} im Clan {clan_name} hinzugefügt.")

    
    @nextcord.slash_command(name='show_warnings', description='Zeigt die Verwarnungen und Strikes von Mitgliedern eines Clans an', guild_ids=SERVER)
    async def show_warnings(self, interaction: nextcord.Interaction, 
                        clan_name: str = nextcord.SlashOption(required=True, choices={"Deathzone": "Deathzone", "Academy": "Academy", "Immortality": "Immortality", "Utopia": "Utopia"}, description="Wähle einen Clan aus")):

     if not (has_permission(interaction.user, 'owner') or has_permission(interaction.user, 'dzvize') or has_permission(interaction.user, 'acvize') or has_permission(interaction.user, 'imvize') or has_permission(interaction.user, 'utvize')):
        await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
        return

     conn = self.get_db_connection()
     cursor = conn.cursor()
     cursor.execute("SELECT user_id, reason, timestamp FROM member_warnings WHERE clan_name = ?", (clan_name,))
     data = cursor.fetchall()
     conn.close()

     user_warnings = {}  # Speichert Informationen pro User
     for user_id, reason, timestamp in data:
        if user_id not in user_warnings:
            user_warnings[user_id] = {'strikes': 0, 'reasons': []}
        user_warnings[user_id]['strikes'] += 1
        user_warnings[user_id]['reasons'].append(f"{timestamp}: {reason}")

     pages = self.create_warning_embeds(user_warnings, clan_name)
     paginator = WarningStrikeView(self, user_warnings, clan_name, 0, len(pages))

     if pages:
            message = await interaction.response.send_message(embed=pages[0], view=paginator)
            paginator.message = message  # Set the message attribute here
     else:
        await interaction.response.send_message("Keine Verwarnungen oder Strikes für diesen Clan gefunden.", ephemeral=True)

    def create_warning_embeds(self, user_warnings, clan_name):
     embeds = []
     items_per_page = 5
     items = list(user_warnings.items())
     guild = self.bot.get_guild(884325196104884248) 
     for i in range(0, len(items), items_per_page):
        embed = nextcord.Embed(title=f"Warnungen und Strikes für Clan {clan_name}", color=nextcord.Color.red())
        for user_id, info in items[i:i + items_per_page]:
            warnings = info['strikes'] // 2
            remaining_strikes = info['strikes'] % 2
            reasons_str = "\n".join(info['reasons'])
            member = guild.get_member(int(user_id))
            display_name = member.display_name if member else "Unbekannter Nutzer"
            embed.add_field(name=f"User: <@{user_id}> ({display_name})", value=f"Verwarnungen: {warnings}\nStrikes: {remaining_strikes}\nGründe:\n{reasons_str}", inline=False)
        embeds.append(embed)
     return embeds

    @nextcord.slash_command(name='remove_strike', description='Entfernt den ältesten Strike von einem Mitglied', guild_ids=SERVER)
    async def remove_strike(self, interaction: nextcord.Interaction, user_id: str, clan_name: str = nextcord.SlashOption(required=True, choices={"Deathzone": "Deathzone", "Academy": "Academy", "Immortality": "Immortality", "Utopia": "Utopia"}, description="Wähle einen Clan aus")):
    
     if not (has_permission(interaction.user, 'owner') or has_permission(interaction.user, 'dzvize') or has_permission(interaction.user, 'acvize') or has_permission(interaction.user, 'imvize') or has_permission(interaction.user, 'utvize')):
        await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
        return

     conn = self.get_db_connection()
     cursor = conn.cursor()

    # Finde den ältesten Strike
     cursor.execute("SELECT id FROM member_warnings WHERE user_id = ? AND clan_name = ? ORDER BY timestamp LIMIT 1", (user_id, clan_name))
     strike_row = cursor.fetchone()

     if strike_row:
        # Entferne den ältesten Strike
        cursor.execute("DELETE FROM member_warnings WHERE id = ?", (strike_row[0],))
        conn.commit()
        await interaction.response.send_message(f"Ältester Strike für User-ID {user_id} im Clan {clan_name} entfernt.")
     else:
        await interaction.response.send_message(f"Keine Strikes für User-ID {user_id} im Clan {clan_name} gefunden.")

     conn.close()

def setup(bot):
    bot.add_cog(WarningStrikeCog(bot))