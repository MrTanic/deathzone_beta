import nextcord
from nextcord.ext import commands
import json
from Bot.Setup.Discord.server_ids import BOT_SERVER_ID
from Bot.Setup.Discord.has_permissions import has_permission
import os

class ModuleButton(nextcord.ui.Button):
    def __init__(self, module_name, help_cog):
        super().__init__(label=module_name, style=nextcord.ButtonStyle.grey)
        self.module_name = module_name
        self.help_cog = help_cog

    async def callback(self, interaction: nextcord.Interaction):
        embed = self.help_cog.create_embed(self.module_name)
        await interaction.response.edit_message(embed=embed, view=self.view)

class TimeoutView(nextcord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.message = None

    async def on_timeout(self):
        if self.message:
            await self.message.edit(view=None)

class OwnerHelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('Commands/Help/Owner/owner_info.json', 'r') as file:
            self.commands_info = json.load(file)

    def create_embed(self, module_name):
        embed = nextcord.Embed(title=f"{module_name} Commands", description="")
        if module_name in self.commands_info:
            for cmd_name, desc in self.commands_info[module_name].items():
                embed.add_field(name=f"/{cmd_name}", value=desc, inline=False)
        else:
            embed.description = "Alle hier aufgeführten Commands sind ausschließlich für den Bot Eigentümer und auch nur au dem Bot Server verfügbar."
        return embed

    @nextcord.slash_command(name="owner_help", description="Zeigt Informationen über alle verfügbaren Slash-Commands.", guild_ids=[BOT_SERVER_ID])
    async def help_command(self, interaction: nextcord.Interaction):
        user = interaction.user

        if not (has_permission(user, 'owner')):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
            return

        initial_embed = self.create_embed("General Information")
        view = TimeoutView(timeout=180)
        view.add_item(ModuleButton("Update", self))
        

        message = await interaction.response.send_message(embed=initial_embed, view=view)
        view.message = message


def setup(bot):
    bot.add_cog(OwnerHelpCog(bot))