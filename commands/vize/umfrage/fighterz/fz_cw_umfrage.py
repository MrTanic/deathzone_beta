import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta
from bot.setup.discord.server_ids import SERVER
from bot.setup.discord.has_permissions import has_permission

class FzAnnouncementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_file_path = "datenbank/logs/cw_date/fz_cw_announcement_log.txt"

    def save_cw_date_to_log(self, message_id, cw_date):
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f"{message_id}:{cw_date}\n")

    @nextcord.slash_command(name='fz_cw_announcement', description='Sendet eine Ankündigung für einen Clankrieg im Fighterz-Clan', guild_ids=SERVER)
    async def cw_announcement(self, interaction: nextcord.Interaction, 
                              wochentag: str = nextcord.SlashOption(
                                  choices=["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
                                  description="Wähle einen Wochentag für den Clankrieg"
                              )):
        user = interaction.user
        if has_permission(user, 'owner') or has_permission(user, 'fzvize'):
            await interaction.response.defer(ephemeral=True)

            heute = datetime.now()
            wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
            wochentag_nummer = wochentage.index(wochentag)
            tage_bis_wochentag = (wochentag_nummer - heute.weekday() + 7) % 7
            naechster_wochentag = heute + timedelta(days=tage_bis_wochentag)
            cw_date_str = naechster_wochentag.strftime('%d.%m.%Y')

            message_text = "Moin <@&1164594638930321578>!"
            embed_description = (
                f"Wir würden gerne am **{wochentag}, den {cw_date_str}** Abends um ca. **21:00 Uhr** einen CW starten!\n\n"
                "✅ wenn du dabei sein willst\n"
                "❌ wenn du nicht dabei sein willst\n"
                "🍻 wenn du dich als Füller anbietest\n\n"
                "Es werden NUR Leute mitgenommen, die hier den ✅ gesetzt haben.\n"
                "- Keine Helden Pflicht\n"
                "Wer nicht am CW teilnehmen möchte oder kann, bitte ich das ❌ zu setzen.\n\n"
                "Lg euer <@&1278334747386445856> Team"
            )
            embed = nextcord.Embed(description=embed_description, color=255)  # Farbe für Fighterz
            message = await interaction.channel.send(content=message_text, embed=embed)

            emojis = ['✅', '❌', '🍻']
            for emoji in emojis:
                await message.add_reaction(emoji)

            # Speichert das CW-Datum in der Log-Datei
            self.save_cw_date_to_log(message.id, cw_date_str)

            await interaction.followup.send("Clankrieg Ankündigung für Fighterz wurde gesendet!", ephemeral=True)
        else:
            await interaction.response.send_message("Du hast nicht die erforderliche Rolle oder Berechtigung, um diesen Befehl zu verwenden.", ephemeral=True)

def setup(bot):
    bot.add_cog(FzAnnouncementCog(bot))