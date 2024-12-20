import nextcord
from nextcord.ext import commands
from bot.setup.discord.server_ids import SERVER
from .im_announcement_logic import send_announcement
from .im_reactions_logic import save_and_create_embed
from .im_notify_non_responders import notify_non_responders
from .im_choose_castle_fillers_logic import choose_castle_fillers
from .im_istdabei_logic import show_yes_responders
from .im_monat_logic import get_non_responders, create_non_responder_embeds
from bot.setup.discord.has_permissions import has_permission

async def check_permissions(interaction):
    user = interaction.user
    if not has_permission(user, 'owner') and not has_permission(user, 'imvize'):
        await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
        return False
    return True

class ImAnnouncementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='im', description='Verwalte Immortality Clan Operationen', guild_ids=SERVER)
    async def im(self, interaction: nextcord.Interaction):
        pass  # Hauptbefehl, der als Container für die Sub-Befehle dient

    @im.subcommand(name='announcement', description='Sendet eine Ankündigung für einen Clankrieg')
    async def cw_announcement(self, interaction: nextcord.Interaction, 
                              wochentag: str = nextcord.SlashOption(
                                  choices=["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
                                  description="Wähle einen Wochentag für den Clankrieg"
                              )):
        if not await check_permissions(interaction):
            return
        await send_announcement(self.bot, interaction, wochentag)

    @im.subcommand(name='auswertung', description='Erstellt ein Embed aus gespeicherten Reaktionen')
    async def cw_auswertung(self, interaction: nextcord.Interaction, message_id: str):
        if not await check_permissions(interaction):
            return
        await save_and_create_embed(self.bot, interaction, message_id)

    @im.subcommand(name='notify', description='Benachrichtigt Mitglieder, die nicht auf die Umfrage reagiert haben')
    async def im_notify_non_responders(self, interaction: nextcord.Interaction, message_id: str):
        if not await check_permissions(interaction):
            return
        await notify_non_responders(self.bot, interaction, message_id)

    @im.subcommand(name='castle', description='Wählt zufällig Mitglieder aus, die mit "Ja" reagiert haben')
    async def im_choose_castle_fillers(self, interaction: nextcord.Interaction, message_id: str, number_of_fillers: int):
        if not await check_permissions(interaction):
            return
        await choose_castle_fillers(self.bot, interaction, message_id, number_of_fillers)

    @im.subcommand(name='istdabei', description='Zeigt alle User, die mit "Ja" reagiert haben, und deren Spieler Account Namen')
    async def im_istdabei(self, interaction: nextcord.Interaction, message_id: str):
        if not await check_permissions(interaction):
            return
        await show_yes_responders(self.bot, interaction, message_id)

    @im.subcommand(name='monat', description='Zeigt, wer im ausgewählten Monat und Jahr nicht reagiert hat.')
    async def umfrage_auswertung(self, interaction: nextcord.Interaction,
                                 jahr: str = nextcord.SlashOption(
                                     name="jahr",
                                     description="Wähle ein Jahr aus"),
                                 monat: str = nextcord.SlashOption(
                                     name="monat",
                                     description="Wähle einen Monat aus",
                                     choices={
                                         "Januar": "01",
                                         "Februar": "02",
                                         "März": "03",
                                         "April": "04",
                                         "Mai": "05",
                                         "Juni": "06",
                                         "Juli": "07",
                                         "August": "08",
                                         "September": "09",
                                         "Oktober": "10",
                                         "November": "11",
                                         "Dezember": "12",
                                     })):
        if not await check_permissions(interaction):
            return

        results = get_non_responders(jahr, monat)

        if not results:
            await interaction.response.send_message("Keine Daten für den ausgewählten Monat und Jahr gefunden.")
            return

        embeds = create_non_responder_embeds(results, jahr, monat)

        await interaction.response.send_message("Hier sind die Ergebnisse:")
        for embed in embeds:
            await interaction.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(ImAnnouncementCog(bot))