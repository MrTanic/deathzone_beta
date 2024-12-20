import nextcord

class WarningStrikeView(nextcord.ui.View):
    def __init__(self, cog, user_warnings, clan_name, current_page, max_pages):
        super().__init__(timeout=180)
        self.cog = cog
        self.user_warnings = user_warnings
        self.clan_name = clan_name
        self.current_page = current_page
        self.max_pages = max_pages
        self.message = None

    @nextcord.ui.button(label="Back", style=nextcord.ButtonStyle.grey)
    async def previous_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            embed = self.cog.create_warning_embeds(self.user_warnings, self.clan_name)[self.current_page]
            await interaction.response.edit_message(embed=embed, view=self)

    @nextcord.ui.button(label="Next", style=nextcord.ButtonStyle.grey)
    async def next_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            embed = self.cog.create_warning_embeds(self.user_warnings, self.clan_name)[self.current_page]
            await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        if self.message:
            await self.message.edit(view=None)