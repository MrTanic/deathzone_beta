import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta
from bot.setup.discord.server_ids import SERVER
from bot.setup.discord.has_permissions import has_permission

LOG_FILE_PATH = "datenbank/logs/cw_date/ac_cw_announcement_log.txt"


class AcAnnouncementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def save_cw_date_to_log(self, message_id, date_str):
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f"{message_id}:{date_str}\n")

    @nextcord.slash_command(name='ac_cw_announcement', description='Sendet eine Ankündigung für einen Clankrieg im Academy-Clan', guild_ids=SERVER)
    async def cw_announcement(self, interaction: nextcord.Interaction, 
                              wochentag: str = nextcord.SlashOption(
                                  choices=["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
                                  description="Wähle einen Wochentag für den Clankrieg"
                              )):
        user = interaction.user
        if has_permission(user, 'owner') or has_permission(user, 'acvize'):
            await interaction.response.defer(ephemeral=True)

            heute = datetime.now()
            wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
            wochentag_nummer = wochentage.index(wochentag)
            tage_bis_wochentag = (wochentag_nummer - heute.weekday() + 7) % 7
            naechster_wochentag = heute + timedelta(days=tage_bis_wochentag)
            cw_date_str = naechster_wochentag.strftime('%d.%m.%Y')

            message_text = "Servus zusammen <@&893503799736545291>!"
            embed_description = (
                f"Wir würden gerne am **{wochentag}**, den {cw_date_str} Abends um ca. **21:00 Uhr** einen CW starten!\n\n"
                "✅ wenn du **dabei** sein willst\n"
                "❌ wenn du **nicht** dabei sein willst\n\n"
                "Es werden NUR Leute mitgenommen, die hier den ✅ gesetzt haben. Das benötigt aktive Helden und einen absolvierten Probefight auf einen gleichstarken Gegner.\n\n"
                "Wer nicht am CW teilnehmen möchte oder kann, bitte ich das ❌ zu setzen. Dies dient zur Aktivitätskontrolle, also bitte ich JEDEN bei dieser Abstimmung teilzunehmen. Bei wiederholter Nichtteilnahme folgt eine Verwarnung und gegebenenfalls der Rauswurf aus dem Clan.\n\n"
                "Bei Fragen diesbezüglich könnt ihr mich gerne privat anschreiben oder auch gerne im <#893503899275776030> Channel nachfragen.\n\n"
                "Wenn ihr Hilfe bei den Angriffen benötigt, könnt entweder im <#1067856136797163621> Channel oder im <#893503899275776030> Channel nachfragen, wir helfen euch gerne.\n\n"
                "LG ~euer Vize Team~⚜️🍻"
            )
            embed = nextcord.Embed(title="Clankrieg Ankündigung", description=embed_description, color=2141262)
            message = await interaction.channel.send(content=message_text, embed=embed)

            self.save_cw_date_to_log(str(message.id), cw_date_str)

            emojis = ['✅', '❌']
            for emoji in emojis:
                await message.add_reaction(emoji)

            await interaction.followup.send("Clankrieg Ankündigung wurde gesendet!", ephemeral=True)
        else:
            await interaction.response.send_message("Du hast nicht die erforderliche Rolle oder Berechtigung, um diesen Befehl zu verwenden.", ephemeral=True)
            

def setup(bot):
    bot.add_cog(AcAnnouncementCog(bot))