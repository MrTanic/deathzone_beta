import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta
from bot.setup.discord.server_ids import SERVER
from bot.setup.discord.has_permissions import has_permission

class UtAnnouncementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_file_path = "datenbank/logs/cw_date/ut_cw_announcement_log.txt"

    def save_cw_date_to_log(self, message_id, cw_date):
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f"{message_id}:{cw_date}\n")

    @nextcord.slash_command(name='ut_cw_announcement', description='Sendet eine Ankündigung für einen Clankrieg im Utopia-Clan', guild_ids=SERVER)
    async def cw_announcement(self, interaction: nextcord.Interaction, 
                              wochentag: str = nextcord.SlashOption(
                                  choices=["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
                                  description="Wähle einen Wochentag für den Clankrieg"
                              )):
        user = interaction.user
        if has_permission(user, 'owner') or has_permission(user, 'utvize'):
            await interaction.response.defer(ephemeral=True)

            heute = datetime.now()
            wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
            wochentag_nummer = wochentage.index(wochentag)
            tage_bis_wochentag = (wochentag_nummer - heute.weekday() + 7) % 7
            naechster_wochentag = heute + timedelta(days=tage_bis_wochentag)
            cw_date_str = naechster_wochentag.strftime('%d.%m.%Y')

            message_text = "Moin <@&988496223637999686>!"
            embed_description = (
                f"Der nächste CW startet am **{wochentag}** um ca. 21 Uhr.\n\n"
                "Setze ein ✅, wenn du dabei sein willst\n"
                "Setze ein ❌, wenn du nicht teilnimmst\n"
                "Mit 🍻 stellst du dich als Füller zur Verfügung 🤝\n\n"
                "Jeder **MUSS** eine Auswahl treffen, da diese Nachricht als **Aktivitätskontrolle** dient!\n\n"
                "Wenn ihr teilnehmt, stellt sicher, dass **ALLE** Helden zur Verfügung stehen! Weitere Infos stehen im Kanal<#1173259664687911052>.\n\n"
                "Falls weitere Fragen bestehen, fragt gerne einen der Vize, danke! <:Liebe:970779407071469608>\n\n"
                "~euer VizeTeam⚜️☠️"
            )
            embed = nextcord.Embed(title="Clankrieg Ankündigung für Utopia", description=embed_description, color=15623433)  # Farbe für Utopia
            message = await interaction.channel.send(content=message_text, embed=embed)

            emojis = ['✅', '❌', '🍻']
            for emoji in emojis:
                await message.add_reaction(emoji)

            # Speichert das CW-Datum in der Log-Datei
            self.save_cw_date_to_log(message.id, cw_date_str)

            await interaction.followup.send("Clankrieg Ankündigung für Utopia wurde gesendet!", ephemeral=True)
        else:
            await interaction.response.send_message("Du hast nicht die erforderliche Rolle oder Berechtigung, um diesen Befehl zu verwenden.", ephemeral=True)

def setup(bot):
    bot.add_cog(UtAnnouncementCog(bot))