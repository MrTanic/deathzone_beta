import nextcord
from nextcord.ext import commands
import sqlite3
from datetime import datetime, timedelta
from bot.setup.discord.has_permissions import has_permission
from bot.setup.discord.channel_ids import UT_ANNOUNCEMENT_CHANNEL
from bot.setup.discord.server_ids import SERVER
from .ut_save_reaction import SaveReactions

LOG_FILE_PATH = "datenbank/logs/cw_date/ut_cw_announcement_log.txt"

class UtCreateEmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "datenbank/umfrage/utopia/ut_cw_umfrage.db"
        self.member_db_path = "datenbank/member/utopia_member.db"
        self.save_reactions = SaveReactions(self.db_path, self.member_db_path)

    def load_member_info(self):
        member_info = {}
        conn = sqlite3.connect(self.member_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, coc_name FROM members")
        for row in cursor.fetchall():
            member_info[row[0]] = {"coc_name": row[1]}
        conn.close()
        return member_info

    @nextcord.slash_command(name='ut_auswertung', description='Erstellt ein Embed aus gespeicherten Reaktionen für Utopia', guild_ids=SERVER)
    async def create_embed(self, interaction: nextcord.Interaction, message_id: str):
        user = interaction.user
        if not has_permission(user, 'owner') and not has_permission(user, 'utvize'):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung.", ephemeral=True)
            return

        announcements_channel = self.bot.get_channel(UT_ANNOUNCEMENT_CHANNEL)
        if announcements_channel is None:
            await interaction.response.send_message("Ankündigungskanal nicht gefunden.", ephemeral=True)
            return

        try:
            message = await announcements_channel.fetch_message(message_id)
            if message is None:
                await interaction.response.send_message("Nachricht nicht gefunden.", ephemeral=True)
                return

            all_member_info = self.save_reactions.load_all_member_info()
            reacted_member_ids = set()
            umfrage_datum = self.save_reactions.get_cw_date_from_log(message_id, LOG_FILE_PATH) or datetime.now().strftime("%d.%m.%Y")

            for reaction in message.reactions:
                async for user in reaction.users():
                    if user != self.bot.user:
                        reacted_member_ids.add(str(user.id))
                        reaction_type = self.save_reactions.get_reaction_type(str(reaction.emoji))
                        coc_name = all_member_info.get(str(user.id), "Unbekannt")
                        self.save_reactions.save_reaction_to_database(message_id, str(user.id), coc_name, reaction_type, umfrage_datum)

            # Mitglieder erfassen, die nicht reagiert haben
            non_reacted_members = {member_id for member_id in all_member_info if member_id not in reacted_member_ids}
            for member_id in non_reacted_members:
                coc_name = all_member_info.get(member_id, "Unbekannt")
                self.save_reactions.save_reaction_to_database(message_id, member_id, coc_name, 'nicht reagiert', umfrage_datum)

        except Exception as e:
            await interaction.response.send_message(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)
            return

        # Reaktionen aus der Datenbank abrufen und das Embed erstellen
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, reaction, umfrage_datum FROM ut_cw_umfrage WHERE message_id = ?", (message_id,))
        reactions_data = cursor.fetchall()
        conn.close()

        if not reactions_data:
            await interaction.response.send_message("Keine Daten für die angegebene Nachrichten-ID gefunden.", ephemeral=True)
            return

        member_info = self.save_reactions.load_all_member_info()

        # Umwandlung des Datumsformats und Berechnung des Ankündigungsdatums
        cw_start_datum = datetime.strptime(reactions_data[0][2], '%d.%m.%Y')
        ankündigungs_datum = (cw_start_datum - timedelta(days=2)).strftime('%d.%m.%Y')
        cw_start_datum_str = cw_start_datum.strftime('%d.%m.%Y')

        embed_description = (
            f"Auswertung der Reaktionen auf die Ankündigung vom {ankündigungs_datum}\n"
            f"CW-Start ist am {cw_start_datum_str}"
        )
        embed = nextcord.Embed(title="Reaktionsauswertung Utopia", description=embed_description, color=15623433)  # Farbe für Utopia
        reactions = {'ja': [], 'nein': [], 'füller': [], 'nicht reagiert': []}

        for user_id, reaction, _ in reactions_data:
            coc_name = member_info.get(user_id, "Unbekannt")
            reactions[reaction].append(coc_name)

        for reaction, names in reactions.items():
            embed.add_field(name=reaction.capitalize(), value=", ".join(names) if names else "Niemand", inline=False)

        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(UtCreateEmbedCog(bot))