import coc
from nextcord.ext import commands, tasks
from client.import_client import abstractClient
from .clan_data_api import format_clan_data
from .clan_data_storage import save_clan_data
from deathzone.clan_tags import clan_tags
from utility.webhook_notifier import send_webhook_notification, GERMAN_TIMEZONE

class ClanData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook_url = "https://discord.com/api/webhooks/1224304677957537874/mE085D7Ljy3LyquLj7yuIetldi3V4F9gzq9hrczsP2x4_nnxhGDhTdNcn9FkZbhKoLq-"
        self.update_clan_data.start()

    @tasks.loop(minutes=5)
    async def update_clan_data(self):
        coc_client = await abstractClient.get_client()
        success_messages = []
        error_messages = []

        for tag in clan_tags.values():
            try:
                clan = await coc_client.get_clan(tag)
                clan_data = format_clan_data(clan)
                save_clan_data(clan_data)
                print(f"Clan data for {clan.name} successfully saved.")
                success_messages.append(f"- {clan.name}")
            except coc.errors.NotFound:
                print(f"Clan with tag {tag} not found.")
                error_messages.append(f"Clan with tag {tag} not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
                error_messages.append(f"An error occurred for clan with tag {tag}: {e}")

        next_run_time = self.update_clan_data.next_iteration.astimezone(GERMAN_TIMEZONE).strftime("%d-%m-%Y | %H:%M:%S")
        if success_messages:
            send_webhook_notification(self.webhook_url, "Clan Data Saved", "\n".join(success_messages), success=True, next_run_time=next_run_time)
        if error_messages:
            send_webhook_notification(self.webhook_url, "Errors Occurred", "\n".join(error_messages), success=False, next_run_time=next_run_time)

    @update_clan_data.before_loop
    async def before_update_clan_data(self):
        await self.bot.wait_until_ready()

    @update_clan_data.error
    async def update_clan_data_error(self, error):
        print(f"An error occurred in the update_clan_data loop: {error}")
        next_run_time = self.update_clan_data.next_iteration.astimezone(GERMAN_TIMEZONE).strftime("%d-%m-%Y | %H:%M:%S")
        send_webhook_notification(self.webhook_url, "Loop Error", f"An error occurred in the update_clan_data loop: {error}", success=False, next_run_time=next_run_time)

def setup(bot):
    bot.add_cog(ClanData(bot))