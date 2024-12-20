import nextcord
from nextcord.ext import commands
from bot.setup.discord.server_ids import SERVER
from .dz_announcement_logic import send_announcement
from .dz_reactions_logic import save_and_create_embed
from .dz_notify_non_responders import notify_non_responders
from .dz_choose_castle_fillers_logic import choose_castle_fillers
from .dz_istdabei_logic import show_yes_responders
from .dz_monat_logic import get_non_responders, create_non_responder_embeds
from bot.setup.discord.has_permissions import has_permission

async def check_permissions(interaction):
    user = interaction.user
    if not has_permission(user, 'owner') and not has_permission(user, 'dzvize'):
        await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
        return False
    return True

class DzAnnouncementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='dz', description='Verwalte DeathZone Clan Operationen', guild_ids=SERVER)
    async def dz(self, interaction: nextcord.Interaction):
        pass  # Hauptbefehl, der als Container für die Sub-Befehle dient

    @dz.subcommand(name='announcement', description='Sendet eine Ankündigung für einen Clankrieg')
    async def cw_announcement(self, interaction: nextcord.Interaction, 
                              wochentag: str = nextcord.SlashOption(
                                  choices=["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
                                  description="Wähle einen Wochentag für den Clankrieg"
                              )):
        if not await check_permissions(interaction):
            return
        await send_announcement(self.bot, interaction, wochentag)

    @dz.subcommand(name='auswertung', description='Erstellt ein Embed aus gespeicherten Reaktionen')
    async def cw_auswertung(self, interaction: nextcord.Interaction, message_id: str):
        if not await check_permissions(interaction):
            return
        await save_and_create_embed(self.bot, interaction, message_id)

    @dz.subcommand(name='notify', description='Benachrichtigt Mitglieder, die nicht auf die Umfrage reagiert haben')
    async def dz_notify_non_responders(self, interaction: nextcord.Interaction, message_id: str):
        if not await check_permissions(interaction):
            return
        await notify_non_responders(self.bot, interaction, message_id)

    @dz.subcommand(name='castle', description='Wählt zufällig Mitglieder aus, die mit "Ja" reagiert haben')
    async def dz_choose_castle_fillers(self, interaction: nextcord.Interaction, message_id: str, number_of_fillers: int):
        if not await check_permissions(interaction):
            return
        await choose_castle_fillers(self.bot, interaction, message_id, number_of_fillers)

    @dz.subcommand(name='istdabei', description='Zeigt alle User, die mit "Ja" reagiert haben, und deren Spieler Account Namen')
    async def dz_istdabei(self, interaction: nextcord.Interaction, message_id: str):
        if not await check_permissions(interaction):
            return
        await show_yes_responders(self.bot, interaction, message_id)

    @dz.subcommand(name='monat', description='Zeigt, wer im ausgewählten Monat und Jahr nicht reagiert hat.')
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
    bot.add_cog(DzAnnouncementCog(bot))