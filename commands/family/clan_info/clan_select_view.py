# clan_select_view.py
import nextcord
from .clan_data import clans, load_clan_info
from .clan_embed import create_clan_embed

class ClanSelectView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        options = [
            nextcord.SelectOption(label=name, value=tag) for name, tag in clans.items()
        ]

        if len(options) > 25:
            options = options[:25]  # Begrenzen Sie die Anzahl der Optionen auf 25

        self.add_item(nextcord.ui.Select(
            placeholder="Wähle einen Clan...",
            options=options,
            custom_id="clan_select"
        ))

    @nextcord.ui.select(custom_id="clan_select")
    async def clan_select(self, select: nextcord.ui.Select, interaction: nextcord.Interaction):
        clan_tag = select.values[0]
        clan_info = load_clan_info(clan_tag)

        if not clan_info:
            await interaction.response.send_message("Clan-Informationen konnten nicht geladen werden.", ephemeral=True)
            return

        embed = create_clan_embed(clan_info)
        await interaction.response.edit_message(embed=embed, view=self)