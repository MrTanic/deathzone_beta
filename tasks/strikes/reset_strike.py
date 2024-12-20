import nextcord
from nextcord.ext import tasks, commands
from datetime import datetime, timedelta
import logging
from bot.setup.datenbank.strikes.warning_strikes import WarningStrikesManager
from commands.vize.strikes.warning_notification import send_strike_notification  # Importiere die Funktion

logger = logging.getLogger(__name__)

class ResetStrikesAndWarningsTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = WarningStrikesManager()
        self.reset_strikes_and_warnings_task = tasks.loop(minutes=10)(self.reset_strikes_and_warnings)
        self.reset_strikes_and_warnings_task.before_loop(self.before_reset_strikes_and_warnings)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.reset_strikes_and_warnings_task.is_running():
            logger.info("Bot is ready. Starting the reset_strikes_and_warnings task...")
            await self.start()

    async def start(self):
        self.reset_strikes_and_warnings_task.start()
        logger.info("reset_strikes_and_warnings task has been started successfully.")

    async def stop(self):
        self.reset_strikes_and_warnings_task.cancel()
        logger.info("reset_strikes_and_warnings task has been stopped.")

    async def reset_strikes_and_warnings(self):
        now = datetime.utcnow()
        logger.info(f"reset_strikes_and_warnings task running at {now.isoformat()}...")

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            # Lösche Strikes, die älter als 1 Stunde sind
            one_hour_ago = now - timedelta(hours=1)
            cursor.execute("SELECT user_id, clan_name, reason, timestamp FROM member_warnings WHERE strikes > 0 AND timestamp <= ?", (one_hour_ago,))
            expired_strikes = cursor.fetchall()

            cursor.execute("DELETE FROM member_warnings WHERE strikes > 0 AND timestamp <= ?", (one_hour_ago,))
            deleted_strikes = cursor.rowcount

            # Benachrichtige über gelöschte Strikes
            for user_id, clan_name, reason, timestamp in expired_strikes:
                duration = "1 Stunde"
                await send_strike_notification(self.bot, 884325196104884248, user_id, clan_name, "Strike entfernt", reason, duration)

            # Lösche Verwarnungen, die älter als 2 Stunden sind
            two_hours_ago = now - timedelta(hours=2)
            cursor.execute("SELECT user_id, clan_name, reason, timestamp FROM member_warnings WHERE strikes = 0 AND timestamp <= ?", (two_hours_ago,))
            expired_warnings = cursor.fetchall()

            cursor.execute("DELETE FROM member_warnings WHERE strikes = 0 AND timestamp <= ?", (two_hours_ago,))
            deleted_warnings = cursor.rowcount

            # Benachrichtige über gelöschte Verwarnungen
            for user_id, clan_name, reason, timestamp in expired_warnings:
                duration = "2 Stunden"
                await send_strike_notification(self.bot, 884325196104884248, user_id, clan_name, "Verwarnung entfernt", reason, duration)

            conn.commit()
            conn.close()

            if deleted_strikes > 0 or deleted_warnings > 0:
                logger.info(f"Deleted {deleted_strikes} strikes and {deleted_warnings} warnings.")
            else:
                logger.info("No strikes or warnings to delete this cycle.")
        except Exception as e:
            logger.error(f"An error occurred during reset_strikes_and_warnings: {e}")

    async def before_reset_strikes_and_warnings(self):
        logger.info("Waiting for bot to be ready before starting reset_strikes_and_warnings task...")
        await self.bot.wait_until_ready()
        logger.info("Bot is ready. Starting reset_strikes_and_warnings task now.")

# Setup-Funktion für den Cog
def setup(bot):
    bot.add_cog(ResetStrikesAndWarningsTask(bot))