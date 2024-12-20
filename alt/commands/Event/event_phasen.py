import nextcord
from nextcord.ext import commands

class EventPhasenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.informations_kanal_id = 1221000825262833714
        self.event_manager_role_id = 1189594120335933530
        self.zu_pingende_rolle_id = 893503806267097088

    async def is_event_manager(self, interaction: nextcord.Interaction) -> bool:
        """Überprüft, ob der Benutzer die Event-Manager-Rolle hat."""
        return any(role.id == self.event_manager_role_id for role in interaction.user.roles)

    @nextcord.slash_command(name='starte_anmeldephase', description='Markiert den Beginn der Anmeldephase für ein Event.')
    async def starte_anmeldephase(self, interaction: nextcord.Interaction, titel: str):
        if not await self.is_event_manager(interaction):
            await interaction.response.send_message('Du hast nicht die erforderliche Berechtigung, um diesen Befehl auszuführen.', ephemeral=True)
            return

        embed = nextcord.Embed(title=f"Anmeldephase gestartet: \nfür {titel}",
                               description="Die Anmeldephase ist jetzt offen. Bitte melde dich jetzt an!",
                               color=0x00ff00)  # Grün für offene Anmeldung
        rollen_ping = f"<@&{self.zu_pingende_rolle_id}>"
        kanal = self.bot.get_channel(self.informations_kanal_id)
        await kanal.send(content=rollen_ping, embed=embed)
        await interaction.response.send_message(f"Anmeldephase für **{titel}** begonnen.", ephemeral=True)

    @nextcord.slash_command(name='beende_anmeldephase', description='Markiert das Ende der Anmeldephase für ein Event.')
    async def beende_anmeldephase(self, interaction: nextcord.Interaction, titel: str):
        if not await self.is_event_manager(interaction):
            await interaction.response.send_message('Du hast nicht die erforderliche Berechtigung, um diesen Befehl auszuführen.', ephemeral=True)
            return

        embed = nextcord.Embed(title=f"Anmeldephase beendet: {titel}",
                               description="Die Anmeldephase für dieses Event ist nun geschlossen. Bleibe gespannt auf weitere Informationen!",
                               color=0xff0000)  # Rot für geschlossene Anmeldung
        kanal = self.bot.get_channel(self.informations_kanal_id)
        await kanal.send(embed=embed)
        await interaction.response.send_message(f"Anmeldephase für **{titel}** beendet.", ephemeral=True)

def setup(bot):
    bot.add_cog(EventPhasenCog(bot))