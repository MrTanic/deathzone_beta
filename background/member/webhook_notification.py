import httpx
import nextcord

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1318634968141926490/7FHMMa9zZ5bEW8lhZBFPzVdvfeCCX_IVewTMlJTjpLyQZXXZbo-kbU0AOSOXlXsVZ2Hx"  # Ersetze dies mit der URL deines Webhooks

class WebhookNotification:
    async def send_webhook_notification(self, content=None, embed=None):
        async with httpx.AsyncClient() as client:
            payload = {}
            if content:
                payload['content'] = content
            if embed:
                payload['embeds'] = [embed.to_dict()]
            await client.post(WEBHOOK_URL, json=payload)