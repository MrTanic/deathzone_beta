import nextcord
from nextcord.ext import commands, tasks
import sqlite3
import os
from datetime import datetime
from Bot.Setup.Discord.server_ids import BOT_SERVER_ID
from Bot.Setup.Discord.has_permissions import has_permission

intents = nextcord.Intents.default()
intents.members = True
intents.messages = False
intents.reactions = True
intents.guilds = True
bot = commands.Bot(intents=intents)

SERVER_ID = 884325196104884248  # Ersetze dies durch deine Guild-ID
STATUS_CHANNEL_ID = 1222211607539617893 # Ersetze dies durch die Channel-ID deines Statuskanals
CLAN_ROLES = {
    "Deathzone": 893503796569858059,
    "Academy": 893503799736545291,
    "Immortality": 893503798704742450,
    "Utopia": 988496223637999686,
    "Fighterz": 1164594638930321578
}

LOG_FILE_PATH = "Datenbank/Member_DB/member_update_log.txt"  # Pfad zur Log-Datei

class MemberUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_paths = {clan: os.path.join("Datenbank/Member_DB", f"{clan}_Member.db") for clan in CLAN_ROLES.keys()}
        self.update_member_db.start()

    def cog_unload(self):
        self.update_member_db.cancel()

    def get_db_connection(self, clan):
        return sqlite3.connect(self.db_paths[clan])

    def log_to_file(self, message):
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f"{datetime.now()}: {message}\n")

    @tasks.loop(minutes=60)
    async def update_member_db(self):
        status_channel = self.bot.get_channel(STATUS_CHANNEL_ID)
        if not status_channel:
            self.log_to_file("Statuskanal nicht gefunden")
            return

        try:
            await status_channel.send("Aktualisiere Mitglieder-Datenbank...")

            guild = self.bot.get_guild(SERVER_ID)
            if guild is None:
                await status_channel.send("Guild nicht gefunden")
                return

            await status_channel.send(f"Verarbeitung der Mitglieder des Servers: {guild.name}")

            for clan, role_id in CLAN_ROLES.items():
                conn = self.get_db_connection(clan)
                cursor = conn.cursor()

                guild_member_ids_with_role = {member.id for member in guild.members if role_id in [role.id for role in member.roles]}
                cursor.execute("SELECT user_id FROM members")
                all_member_ids_in_db = {row[0] for row in cursor.fetchall()}
                members_to_remove = all_member_ids_in_db - guild_member_ids_with_role

                for member_id in members_to_remove:
                    self.log_to_file(f"Mitglied {member_id} aus {clan} entfernt")
                    cursor.execute("DELETE FROM members WHERE user_id = ?", (member_id,))
                conn.commit()

                for member in guild.members:
                    if member.bot or role_id not in [role.id for role in member.roles]:
                        continue

                    coc_name = member.nick or member.display_name
                    cursor.execute("INSERT INTO members (user_id, coc_name, clan_name) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET coc_name = ?, clan_name = ?", (str(member.id), coc_name, clan, coc_name, clan))
                    self.log_to_file(f"Mitglied {member.id} ({coc_name}) zu {clan} hinzugefügt/aktualisiert")
                conn.commit()
                conn.close()

            await status_channel.send("Aktualisierung der Mitgliederdatenbank abgeschlossen.\n------------------------------------------")
        except Exception as e:
            self.log_to_file(f"Fehler bei der Aktualisierung der Mitgliederdatenbank: {str(e)}")
            await status_channel.send(f"Fehler bei der Aktualisierung der Mitgliederdatenbank: {str(e)}")

    @update_member_db.before_loop
    async def before_update_member_db(self):
        await self.bot.wait_until_ready()

    @nextcord.slash_command(name='trigger_update', description='Stößt die Aktualisierung der Mitglieder-Datenbank manuell an', guild_ids=[BOT_SERVER_ID])
    async def trigger_update(self, interaction: nextcord.Interaction):
        if not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du bist nicht berechtigt, diesen Befehl auszuführen.", ephemeral=True)
            return

        status_channel = self.bot.get_channel(STATUS_CHANNEL_ID)
        if status_channel:
            await status_channel.send("Manuelle Aktualisierung der Mitglieder-Datenbank gestartet...")
        
        if self.update_member_db.is_running():
            self.update_member_db.stop()

        await self.update_member_db()

        if not self.update_member_db.is_running():
            self.update_member_db.start()

        if status_channel:
            await status_channel.send("Manuelle Aktualisierung der Mitglieder-Datenbank abgeschlossen.")

def setup(bot):
    bot.add_cog(MemberUpdateCog(bot))