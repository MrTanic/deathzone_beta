import nextcord
from nextcord.ext import commands
import sqlite3
import os
from bot.setup.discord.has_permissions import has_permission

class UmfrageAuswertungCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join("datenbank", "umfrage", "deathzone", "dz_cw_umfrage.db")

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @nextcord.slash_command(name='dz_monat_auswertung', description='Zeigt, wer im ausgewählten Monat und Jahr nicht reagiert hat.')
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
        if not (has_permission(interaction.user, 'owner') or has_permission(interaction.user, 'dzvize')):
            await interaction.response.send_message("Du hast nicht die erforderliche Berechtigung, diesen Befehl auszuführen.", ephemeral=True)
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT coc_name, user_id, COUNT(*) AS nicht_reagiert_count
            FROM cw_umfragen
            WHERE reaction = 'nicht reagiert' AND strftime('%Y.%m', umfrage_datum) = ?
            GROUP BY coc_name, user_id
            ''',
            (f"{jahr}.{monat}",)
        )
        results = cursor.fetchall()
        conn.close()

        if results:
            response = f"Benutzer, die im {monat}.{jahr} nicht reagiert haben:\n"
            for coc_name, user_id, count in results:
                response += f"CoC Name: {coc_name}\nUser ID: <@{user_id}>\nNicht reagiert: {count} x\n\n"
        else:
            response = "Keine Daten für den ausgewählten Monat und Jahr gefunden."

        await interaction.response.send_message(response)

def setup(bot):
    bot.add_cog(UmfrageAuswertungCog(bot))