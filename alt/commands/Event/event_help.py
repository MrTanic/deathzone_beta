import nextcord
from nextcord.ext import commands

class EventAnmeldungHilfeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ziel_kanal_id = 1221000825262833714
        self.event_manager_rolle_id = 1189594120335933530

    @nextcord.slash_command(name='anmeldung_hilfe', description='Sendet die Event-Anmeldehilfe in den festgelegten Kanal.')
    async def sende_event_anmeldung_hilfe(self, interaction: nextcord.Interaction):
        # Überprüfe, ob der ausführende Benutzer die Event Manager Rolle hat
        if self.event_manager_rolle_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message('Du hast nicht die erforderliche Berechtigung, um diesen Befehl auszuführen.', ephemeral=True)
            return
        
        ziel_kanal = self.bot.get_channel(self.ziel_kanal_id)
        if not ziel_kanal:
            await interaction.response.send_message("Der Zielkanal wurde nicht gefunden.", ephemeral=True)
            return

        embed = nextcord.Embed(title="Event-Anmeldung",
                               description="Hier ist, wie du dich für unsere Events anmelden kannst:",
                               color=0x3498db)
        embed.add_field(name="Information", value="- Sobald die Anmeldephase für das nächste event begonnen hat, wird hier drunter ein embed stehen. Das die Anmelde Phase begonnen hat.\n- Wenn die Anmeldephase beendet ist wird auch ein embed gesendet.", inline=False)
        embed.add_field(name="Schritt 1", value="Verwende den `/register_event` Befehl!", inline=False)
        embed.add_field(name="Schritt 2", value="Es wird dann ein Modul geöffnet in welches das #Spielertag eingetragen werden muss.", inline=False)
        embed.add_field(name="Schritt 3", value="Absenden", inline=False)
        embed.add_field(name="Hinweis", value="Stelle sicher, dass du deinen korrekten Spieler-Tag verwendest, damit die Anmeldung erfolgreich ist.", inline=False)
        embed.set_footer(text="Bei Fragen wende dich an das Event-Management-Team.")

        await ziel_kanal.send(embed=embed)
        await interaction.response.send_message(f"Event-Anmeldehilfe wurde im Kanal <#{self.ziel_kanal_id}> gesendet.", ephemeral=True)

def setup(bot):
    bot.add_cog(EventAnmeldungHilfeCog(bot))