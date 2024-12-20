#<@&{IMMORTALITY_ROLE_ID}>
import nextcord
from datetime import datetime, timedelta
from bot.setup.discord.user_ids import IMMORTALITY_ROLE_ID
from bot.setup.discord.has_permissions import has_permission
from assets.emojis.reactions_emojis import reactions_emojis

LOG_FILE_PATH = "datenbank/logs/cw_date/im_cw_announcement_dates.txt"  # Pfad zur Log-Datei

def save_announcement_date(message_id, date):
    with open(LOG_FILE_PATH, 'a') as file:
        file.write(f"{message_id}:{date.strftime('%d.%m.%Y')}\n")

async def send_announcement(bot, interaction: nextcord.Interaction, wochentag: str):
    user = interaction.user
    if has_permission(user, 'owner') or has_permission(user, 'imvize'):
        await interaction.response.defer(ephemeral=True)

        heute = datetime.now()
        wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        wochentag_nummer = wochentage.index(wochentag)
        tage_bis_wochentag = (wochentag_nummer - heute.weekday() + 7) % 7
        naechster_wochentag = heute + timedelta(days=tage_bis_wochentag)

        message_text = f"Hallo zusammen <@&{IMMORTALITY_ROLE_ID}> !"
        embed_description = (
            f"Wir würden gerne am **{wochentag}**, den {naechster_wochentag.strftime('%d.%m.%Y')} Abends um ca. **21:00 Uhr** einen CW starten!\n\n"
            f"{reactions_emojis['ja']}   {reactions_emojis['arrow']}  wenn du **dabei** sein willst\n"
            f"{reactions_emojis['nein']}   {reactions_emojis['arrow']}  wenn du **nicht** dabei sein willst\n"
            f"{reactions_emojis['fueller']} {reactions_emojis['arrow']}  wenn du dich als **Auffüller** zur Verfügung stellen willst\n\n"
            "Bei mehreren Accounts bitte Bescheid geben welcher Account mitgenommen werden soll. Es werden Standardmäßig alle verlinkten Accounts mitgenommen.\n\n"
            "__Es werden Leute zum Befüllen der Burgen ausgewählt.__\n\n"
            "Liebe Grüße,\n\n"
            "euer <@&893503791532503101> Team ⚜️"
        )
        embed = nextcord.Embed(title="Clankrieg Ankündigung", description=embed_description, color=255)
        message = await interaction.channel.send(content=message_text, embed=embed)

        emojis = [reactions_emojis["ja"], reactions_emojis["nein"], reactions_emojis["fueller"]]
        for emoji in emojis:
            await message.add_reaction(emoji)

        save_announcement_date(message.id, naechster_wochentag)  # Speichert Message-ID und Datum

        await interaction.followup.send("Clankrieg Ankündigung wurde gesendet!", ephemeral=True)
    else:
        await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)