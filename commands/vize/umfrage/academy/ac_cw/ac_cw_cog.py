import nextcord
from nextcord.ext import commands
from bot.setup.discord.has_permissions import has_permission
from bot.setup.discord.server_ids import SERVER
from .ac_cw_logic import save_and_create_ac_embed
from .ac_cw_announcement import send_ac_announcement
from .ac_cw_fillers import choose_castle_fillers
from .ac_notify_non_responders import notify_non_responders
from .ac_istdabei_logic import show_yes_responders
from .ac_monat_logic import get_non_responders, create_non_responder_embeds

async def check_permissions(interaction):
    user = interaction.user
    if not has_permission(user, 'owner') and not has_permission(user, 'acvize'):
        await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
        return False
    return True

class ACCWCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='ac', description='Verwalte Academy Clan Operationen', guild_ids=SERVER)
    async def ac_cw(self, interaction: nextcord.Interaction):
        pass  # Hauptbefehl, der als Container für die Sub-Befehle dient

    @ac_cw.subcommand(name='announcement', description='Sendet eine Ankündigung für einen Clankrieg')
    async def cw_announcement(self, interaction: nextcord.Interaction, 
                              wochentag: str = nextcord.SlashOption(
                                  choices=["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
                                  description="Wähle einen Wochentag für den Clankrieg"
                              )):
        user = interaction.user
        if has_permission(user, 'owner') or has_permission(user, 'acvize'):
            await send_ac_announcement(self.bot, interaction, wochentag)
        else:
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)

    @ac_cw.subcommand(name='auswertung', description='Zeigt die Auswertung der Reaktionen auf die CW-Ankündigung')
    async def cw_auswertung(self, interaction: nextcord.Interaction, message_id: str):
        user = interaction.user
        if has_permission(user, 'owner') or has_permission(user, 'acvize'):
            await save_and_create_ac_embed(self.bot, interaction, message_id)
        else:
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)

    @ac_cw.subcommand(name='castle', description='Wählt zufällig Mitglieder aus, die die Burgen füllen sollen')
    async def cw_fillers(self, interaction: nextcord.Interaction, message_id: str, number_of_fillers: int):
        user = interaction.user
        if has_permission(user, 'owner') or has_permission(user, 'acvize'):
            await choose_castle_fillers(self.bot, interaction, message_id, number_of_fillers)
        else:
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)

    @ac_cw.subcommand(name='notify', description='Benachrichtigt Mitglieder, die nicht auf die Umfrage reagiert haben')
    async def notify_non_responders(self, interaction: nextcord.Interaction, message_id: str):
        user = interaction.user
        if has_permission(user, 'owner') or has_permission(user, 'acvize'):
            await notify_non_responders(self.bot, interaction, message_id)
        else:
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            
    @ac_cw.subcommand(name='istdabei', description='Zeigt die Mitglieder an, die mit "Ja" auf die Umfrage reagiert haben')
    async def show_yes_responders(self, interaction: nextcord.Interaction, message_id: str):
        user = interaction.user
        if has_permission(user, 'owner') or has_permission(user, 'acvize'):
            await show_yes_responders(self.bot, interaction, message_id)
        else:
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)

    @ac_cw.subcommand(name='monat', description='Zeigt, wer im ausgewählten Monat und Jahr nicht reagiert hat.')
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
    bot.add_cog(ACCWCommand(bot))