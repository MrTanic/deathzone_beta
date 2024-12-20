
import nextcord
from nextcord.ext import tasks, commands
import os
from datetime import datetime
from background.member.db_connection import DBConnection
from .webhook_notification import WebhookNotification
from .log_helper import LogHelper
from .embed_helper import create_error_embed, create_success_embed
from bot.setup.discord.server_ids import DEATHZONE_SERVER_ID
from bot.setup.discord.user_ids import CLAN_ROLES

class UpdateMemberDBTask(commands.Cog, WebhookNotification, LogHelper):
    def __init__(self, bot):
        self.bot = bot
        self.db_paths = {clan: os.path.join("datenbank/member", f"{clan}_member.db") for clan in CLAN_ROLES.keys()}
        self.db_connection = DBConnection(self.db_paths)
        self.update_member_db_task.start()

    @tasks.loop(minutes=60)
    async def update_member_db_task(self):
        description = ""
        try:
            guild = self.bot.get_guild(DEATHZONE_SERVER_ID)
            if guild is None:
                description += "Guild nicht gefunden\n"
                embed = create_error_embed(description)
                await self.send_webhook_notification(content=None, embed=embed)
                return

            description += f"- Verarbeitung der Mitglieder des Servers: {guild.name}\n"

            for clan, role_id in CLAN_ROLES.items():
                conn = self.db_connection.get_db_connection(clan)
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

            description += "- Aktualisierung der Mitgliederdatenbank abgeschlossen."
            embed = create_success_embed(description)
            await self.send_webhook_notification(content=None, embed=embed)
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Mitgliederdatenbank: {e}")
            description += f"Fehler beim Aktualisieren der Mitgliederdatenbank: {e}\n"
            embed = create_error_embed(description)
            await self.send_webhook_notification(content=None, embed=embed)

    @update_member_db_task.before_loop
    async def before_update_member_db(self):
        await self.bot.wait_until_ready()

    @update_member_db_task.error
    async def update_member_db_error(self, loop, context):
        error = context.get('exception')
        description = f"Fehler in der update_member_db Schleife: {error}"
        print(description)
        embed = create_error_embed(description)
        await self.send_webhook_notification(content=None, embed=embed)

def setup(bot):
    bot.add_cog(UpdateMemberDBTask(bot))