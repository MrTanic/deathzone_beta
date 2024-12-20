import nextcord
from nextcord.ext import tasks, commands
from datetime import datetime
import pytz
from bot.setup.discord.channel_ids import IM_CWL_CHANNEL, STATUS_CHANNEL_ID
from bot.setup.discord.user_ids import IMMORTALITY_ROLE_ID

class ImCWLAnnouncementTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.announcement_channel_id = IM_CWL_CHANNEL
        self.status_channel_id = STATUS_CHANNEL_ID
        self.auto_announce.start()

    def cog_unload(self):
        self.auto_announce.cancel()

    @tasks.loop(minutes=1)
    async def auto_announce(self):
        now = datetime.now(pytz.timezone("Europe/Berlin"))

        if now.day == 18 and now.hour == 20 and now.minute == 20:
            await self.announce_cwl()

    @auto_announce.before_loop
    async def before_auto_announce(self):
        await self.bot.wait_until_ready()

    async def announce_cwl(self):
        channel = self.bot.get_channel(self.announcement_channel_id)
        if not channel:
            return

        message_content = f"Hallo zusammen <@&{IMMORTALITY_ROLE_ID}> !"
        embed = nextcord.Embed(
            title="CWL Ankündigung",
            description=(
                "Dies ist die **Umfrage**, für die **kommende CWL**.\n\n"
                "Bitte alle eigenständig Abstimmen, somit können wir Vize vorausschauender und besser planen.\n\n"
                "<:ja:961978768765911110> <:arrow2:920341386757279824> wenn du **dabei** sein willst\n"
                "<:nein:961978783483699251> <:arrow2:920341386757279824> wenn du **nicht** dabei sein willst\n"
                "<:zap:1204471668198875156> <:arrow2:920341386757279824> wenn du **mehrere** Accounts anmelden willst\n\n"
                "Alle die sich anmelden, werden auf unsere Clanfamilie aufgeteilt. "
                "Gerne können Präferenzen mitgeteilt werden, wo ihr gerne spielen wollt.\n\n"
                "~ euer <@&893503791532503101> Team ⚜️"
            ),
            color=2135246
        )
        message = await channel.send(content=message_content, embed=embed)
        emojis = ["<:ja:961978768765911110>", "<:nein:961978783483699251>", "<:zap:1204471668198875156>"]
        for emoji in emojis:
            await message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(ImCWLAnnouncementTask(bot))