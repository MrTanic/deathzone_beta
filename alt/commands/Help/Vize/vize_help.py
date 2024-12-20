import nextcord
from nextcord.ext import commands
import json
from Bot.Setup.Discord.server_ids import SERVER
from Bot.Setup.Discord.has_permissions import has_permission

class ModuleButton(nextcord.ui.Button):
    def __init__(self, module_name, help_cog):
        super().__init__(label=module_name, style=nextcord.ButtonStyle.grey)
        self.module_name = module_name
        self.help_cog = help_cog

    async def callback(self, interaction: nextcord.Interaction):
        if self.module_name == "Dokumentation":
            embed = self.help_cog.create_documentation_embed()
        elif self.module_name == "Einleitung":
            embed = self.help_cog.create_introduction_embed()
        else:
            embed = self.help_cog.create_embed(self.module_name)
        await interaction.response.edit_message(embed=embed, view=self.view)

class TimeoutView(nextcord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.message = None

    async def on_timeout(self):
        if self.message:
            await self.message.edit(view=None)

class VizeHelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('Commands/Help/Vize/vize_info.json', 'r') as file:
            self.commands_info = json.load(file)

    def create_embed(self, module_name):
        embed = nextcord.Embed(title=f"{module_name} Commands", description="")
        if module_name in self.commands_info:
            for cmd_name, desc in self.commands_info[module_name].items():
                embed.add_field(name=f"/{cmd_name}", value=desc, inline=False)
        else:
            embed.description = "**Herzlich Willkommen** im Help Menü!\nHier findest du alle Commands. Detailliert beschrieben im jeweiligen Panel.\n- Lies dir unbedingt die **Einleitung** vorher duch! \n- Bei fragen, Poblemen oder wünschen wende dich bitte an **Mr Tanic**."
        return embed

    def create_documentation_embed(self):
        embed = nextcord.Embed(title="Dokumentation", description="Die Clan basierenden Commands funktionieren wie folgt:\n\n**cw announcement**\n- Schickt ein vordefiniertes Embed in den Kanal für eine CW Umrage, mit Reaktionen. Das Datum der Umfrage wird anhand des Wochentages in einer Log Datei gespeichert.\n**cw save reactions**\n- Speichert die Reaktionen von der CW Umfrage. (Ja, Nein, nicht Reagiert)\n**cw auswerung**\n- Holt die gespeicherten Reaktionen aus der Datenbank und schreibt sie ins Embed.\n- Zusätzlich holt er das gespeicherte Datum aus der Log Datei und Berechnet das Umfrage Datum. (Standardmäßig -2 Tage vom CW Datum)\n**cw ja reaction**\n- Zeigt nur die User an die mit Ja reagiert haben und zusätzlich die Verknüpften CoC Accounts die momentan im Clan sind. (Clantags sind bereits im Command integriert)")
        return embed

    def create_introduction_embed(self):
        embed = nextcord.Embed(title="Einleitung", description="- Jeder Command kann nur von Vize Anführern ausgeführt werden\n- Die Clan bassierendn Commands können nur von Vize Anführern des jeweiligen Clans bzw mit der Rolle ausgeführt werden.")
        return embed

    @nextcord.slash_command(name="vize", description="Zeigt Informationen über alle verfügbaren Slash-Commands.", guild_ids=SERVER)
    async def help_command(self, interaction: nextcord.Interaction):
        user = interaction.user
        if not (has_permission(user, 'owner') or has_permission(user, 'dzvize') or 
                has_permission(user, 'acvize') or has_permission(user, 'imvize') or 
                has_permission(user, 'utvize')):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
            return

        initial_embed = self.create_embed("General Information")
        view = TimeoutView(timeout=180)
        view.add_item(ModuleButton("Einleitung", self))
        view.add_item(ModuleButton("Dokumentation", self))
        view.add_item(ModuleButton("Member", self))
        view.add_item(ModuleButton("Link", self))
        view.add_item(ModuleButton("Events", self))
        view.add_item(ModuleButton("Kalender", self))
        view.add_item(ModuleButton("Strike", self))
        view.add_item(ModuleButton("Deathzone", self))
        view.add_item(ModuleButton("Academy", self))
        view.add_item(ModuleButton("Immortality", self))
        view.add_item(ModuleButton("Utopia", self))

        message = await interaction.response.send_message(embed=initial_embed, view=view)
        view.message = message

def setup(bot):
    bot.add_cog(VizeHelpCog(bot))