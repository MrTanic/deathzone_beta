from nextcord.ext import tasks, commands
from datetime import datetime
import pytz
from utility.leaderboard.read_clan_data import read_all_clan_data
from utility.leaderboard.embed_creator import create_leaderboard_embed
from bot.setup.discord.channel_ids import LEADERBOARD_CHANNEL  # Import der Channel ID

class LeaderBoardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_hour = 7
        self.target_minute = 0
        self.channel_id = LEADERBOARD_CHANNEL  # Nutzung der importierten Channel ID
        self.already_sent_today = False
        self.daily_task.start()

    def cog_unload(self):
        self.daily_task.cancel()

    @tasks.loop(minutes=1)
    async def daily_task(self):
        # Zeitzone für Deutschland festlegen
        tz = pytz.timezone('Europe/Berlin')
        now = datetime.now(tz)

        # Überprüfe, ob die aktuelle Zeit der Zielzeit entspricht und der Task heute noch nicht ausgeführt wurde
        if now.hour == self.target_hour and now.minute == self.target_minute and not self.already_sent_today:
            sorted_players = read_all_clan_data()
            embed = await create_leaderboard_embed(sorted_players, "Top 25 Spieler von DeathZone")

            channel = self.bot.get_channel(self.channel_id)
            if channel:
                await channel.send(embed=embed)

            self.already_sent_today = True

        # Zurücksetzen der Flagge um Mitternacht in der deutschen Zeitzone
        if now.hour == 0 and now.minute == 0:
            self.already_sent_today = False

    @daily_task.before_loop
    async def before_daily_task(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(LeaderBoardCog(bot))