import nextcord

NOTIFICATION_CHANNEL_ID = 1268457507836137524  # Ersetze diese Zahl durch die tatsächliche Kanal-ID

async def send_strike_notification(bot: nextcord.Client, guild_id: int, user_id: str, clan_name: str, action: str, reason: str, duration: str):
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(NOTIFICATION_CHANNEL_ID)
    
    if channel:
        user = guild.get_member(int(user_id))
        user_name = user.display_name if user else "Unbekannter Nutzer"
        embed = nextcord.Embed(
            title=f"{action}",
            description=f"**Benutzer:** {user_name} ({user_id})\n"
                        f"**Clan:** {clan_name}\n"
                        f"**Aktion:** {action}\n"
                        f"**Grund:** {reason}\n"
                        f"**Dauer:** {duration}",
            color=nextcord.Color.orange() if action == "Strike entfernt" else nextcord.Color.green()
        )
        await channel.send(embed=embed)