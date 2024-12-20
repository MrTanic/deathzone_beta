import nextcord
from nextcord.ext import commands
import logging
from datetime import datetime, timedelta
from bot.setup.datenbank.strikes.warning_strikes import WarningStrikesManager
from bot.setup.discord.server_ids import SERVER
from bot.setup.discord.has_permissions import has_permission
from commands.vize.strikes.warning_strike_view import WarningStrikeView
from commands.vize.strikes.warning_notification import send_strike_notification

logger = logging.getLogger(__name__)

class WarningStrikeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = WarningStrikesManager()

    @nextcord.slash_command(name='add_strike', description='Fügt einem Mitglied einen Strike hinzu', guild_ids=SERVER)
    async def add_strike(self, interaction: nextcord.Interaction, 
                         user_id: str, 
                         clan_name: str = nextcord.SlashOption(
                             required=True, 
                             choices={
                                 "~DeathZone~": "~DeathZone~", 
                                 "DZ⚜️Academy": "DZ⚜️Academy", 
                                 "DZ⚜️Immortality": "DZ⚜️Immortality", 
                                 "DZ⚜️Utopia": "DZ⚜️Utopia"
                             }, 
                             description="Wähle einen Clan aus"),
                         reason: str = nextcord.SlashOption(required=True, description="Grund für den Strike")):
        if not has_permission(interaction.user, 'owner') and not has_permission(interaction.user, f'{clan_name.lower()}vize'):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO member_warnings (user_id, clan_name, strikes, reason) VALUES (?, ?, 1, ?)", 
                       (user_id, clan_name, reason))
        conn.commit()
        conn.close()
        await interaction.response.send_message(f"Strike für User-ID {user_id} im Clan {clan_name} hinzugefügt.")

    @nextcord.slash_command(name='show_warnings', description='Zeigt die Verwarnungen und Strikes von Mitgliedern eines Clans an', guild_ids=SERVER)
    async def show_warnings(self, interaction: nextcord.Interaction, 
                            clan_name: str = nextcord.SlashOption(
                                required=True, 
                                choices={
                                    "~DeathZone~": "~DeathZone~", 
                                    "DZ⚜️Academy": "DZ⚜️Academy", 
                                    "DZ⚜️Immortality": "DZ⚜️Immortality", 
                                    "DZ⚜️Utopia": "DZ⚜️Utopia"
                                }, 
                                description="Wähle einen Clan aus")):
        if not has_permission(interaction.user, 'owner') and not has_permission(interaction.user, f'{clan_name.lower()}vize'):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, reason, timestamp, strikes FROM member_warnings WHERE clan_name = ?", (clan_name,))
        data = cursor.fetchall()
        conn.close()

        user_warnings = {}
        for user_id, reason, timestamp, strikes in data:
            if user_id not in user_warnings:
                user_warnings[user_id] = {'strikes': 0, 'reasons': [], 'timestamps': []}
            user_warnings[user_id]['strikes'] += strikes
            user_warnings[user_id]['reasons'].append(f"{timestamp}: {reason}")
            user_warnings[user_id]['timestamps'].append(timestamp)

        pages = self.create_warning_embeds(user_warnings, clan_name)
        paginator = WarningStrikeView(self, user_warnings, clan_name, 0, len(pages))

        if pages:
            message = await interaction.response.send_message(embed=pages[0], view=paginator)
            paginator.message = message
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
                
                # Berechnen des Ablaufdatums und Konvertieren in Unix-Zeit
                last_timestamp = info['timestamps'][-1]
                timestamp_datetime = datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")
                if remaining_strikes > 0:
                    expiration_time = timestamp_datetime + timedelta(hours=1)  # Ablauf nach 1 Stunde für Strikes
                else:
                    expiration_time = timestamp_datetime + timedelta(hours=2)  # Ablauf nach 2 Stunden für Verwarnungen

                unix_timestamp = int(expiration_time.timestamp())
                expiration_str = f"<t:{unix_timestamp}:R>"
                
                member = guild.get_member(int(user_id))
                display_name = member.display_name if member else "Unbekannter Nutzer"
                embed.add_field(name=f"User: <@{user_id}> ({display_name})", 
                                value=f"Verwarnungen: {warnings}\nStrikes: {remaining_strikes}\nGründe:\n{reasons_str}\n\n**Verfällt**: {expiration_str}", 
                                inline=False)
            embeds.append(embed)
        return embeds

    @nextcord.slash_command(name='remove_strike', description='Entfernt den ältesten Strike von einem Mitglied', guild_ids=SERVER)
    async def remove_strike(self, interaction: nextcord.Interaction, user_id: str, clan_name: str):
        if not has_permission(interaction.user, 'owner') and not has_permission(interaction.user, f'{clan_name.lower()}vize'):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM member_warnings WHERE user_id = ? AND clan_name = ? ORDER BY timestamp LIMIT 1", 
                       (user_id, clan_name))
        strike_row = cursor.fetchone()

        if strike_row:
            cursor.execute("DELETE FROM member_warnings WHERE id = ?", (strike_row[0],))
            conn.commit()
            await interaction.response.send_message(f"Ältester Strike für User-ID {user_id} im Clan {clan_name} entfernt.")
            await send_strike_notification(self.bot, interaction.guild.id, user_id, clan_name, "Strike entfernt")
        else:
            await interaction.response.send_message(f"Keine Strikes für User-ID {user_id} im Clan {clan_name} gefunden.")

        conn.close()

def setup(bot):
    bot.add_cog(WarningStrikeCog(bot))