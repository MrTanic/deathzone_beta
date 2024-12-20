import nextcord
from nextcord.ext import commands, tasks
from .scheduler import scheduler
import asyncio
import httpx

class LegendsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_legends_data.start()
        self.webhook_url = "https://discord.com/api/webhooks/1257195578446581812/RMofG-fefzuCN1xVH6w1wjID0Sk9kU0z22opBq4SRkSkjS7iz8MnYRYQptjrR_N3fj6s"

    @tasks.loop(minutes=5)
    async def update_legends_data(self):
        try:
            results = await scheduler()
            success_messages = []
            error_messages = []
            for success, message in results:
                if success:
                    success_messages.append(f"{message} erfolgreich gespeichert.")
                else:
                    error_messages.append(message)
            if success_messages:
                await self.send_webhook_notification("\n".join(success_messages))
            if error_messages:
                await self.send_webhook_error("\n".join(error_messages))
        except Exception as e:
            await self.send_webhook_error(f"Fehler beim Speichern der Daten: {e}")

    @update_legends_data.before_loop
    async def before_update_legends_data(self):
        await self.bot.wait_until_ready()

    async def send_webhook_notification(self, message):
        embed = nextcord.Embed(title="Erfolg", description=message, color=nextcord.Color.green())
        async with httpx.AsyncClient() as client:
            response = await client.post(self.webhook_url, json={"embeds": [embed.to_dict()]})
            if response.status_code != 204:
                print(f"Fehler beim Senden der Erfolgsnachricht: {response.text}")

    async def send_webhook_error(self, error_message):
        embed = nextcord.Embed(title="Fehler", description=error_message, color=nextcord.Color.red())
        async with httpx.AsyncClient() as client:
            response = await client.post(self.webhook_url, json={"embeds": [embed.to_dict()]})
            if response.status_code != 204:
                print(f"Fehler beim Senden der Fehlermeldung: {response.text}")

def setup(bot):
    bot.add_cog(LegendsCog(bot))