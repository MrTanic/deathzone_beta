import nextcord
from datetime import datetime, timedelta
from bot.setup.discord.user_ids import ACADEMY_ROLE_ID
from assets.emojis.reactions_emojis import reactions_emojis

LOG_FILE_PATH = "datenbank/logs/cw_date/ac_cw_announcement_log.txt"

def save_cw_date_to_log(message_id, date_str):
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write(f"{message_id}:{date_str}\n")

async def send_ac_announcement(bot, interaction: nextcord.Interaction, wochentag: str):
    await interaction.response.defer(ephemeral=True)

    heute = datetime.now()
    wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    wochentag_nummer = wochentage.index(wochentag)
    tage_bis_wochentag = (wochentag_nummer - heute.weekday() + 7) % 7
    naechster_wochentag = heute + timedelta(days=tage_bis_wochentag)
    cw_date_str = naechster_wochentag.strftime('%d.%m.%Y')

    message_text = f"Servus zusammen <@&{ACADEMY_ROLE_ID}> !"
    embed_description = (
        f"Wir würden gerne am **{wochentag}**, den {cw_date_str} Abends um ca. **21:00 Uhr** einen CW starten!\n\n"
        "✅ wenn du **dabei** sein willst\n"
        "❌ wenn du **nicht** dabei sein willst\n\n"
        "Bei mehreren Accounts bitte Bescheid geben welcher Account mitgenommen werden soll. Es werden Standardmäßig alle verlinkten Accounts mitgenommen.\n\n"
            "__Es werden Leute zum Befüllen der Burgen ausgewählt.__\n\n"
        "LG ~euer <@&893503792602042448> Team~⚜️🍻"
    )
    embed = nextcord.Embed(title="Clankrieg Ankündigung", description=embed_description, color=255)
    message = await interaction.channel.send(content=message_text, embed=embed)

    save_cw_date_to_log(str(message.id), cw_date_str)

    emojis = ['✅', '❌']
    for emoji in emojis:
        await message.add_reaction(emoji)

    await interaction.followup.send("Clankrieg Ankündigung wurde gesendet!", ephemeral=True)