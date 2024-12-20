import nextcord
import json

class OwnerHelpSelect(nextcord.ui.Select):
    def __init__(self, options):
        super().__init__(
            placeholder="Wähle eine Kategorie...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: nextcord.Interaction):
        selected_option = self.values[0]
        with open('commands/help/data/owner_help_info.json', 'r') as f:
            owner_info = json.load(f)
        
        selected_data = next((opt for opt in owner_info['optionen'] if opt['name'] == selected_option), None)
        if not selected_data:
            await interaction.response.edit_message(content="Kategorie nicht gefunden.", embed=None, view=self.view)
            return
        
        beschreibung = selected_data['beschreibung']
        commands = selected_data.get('commands', [])
        
        embed = nextcord.Embed(
            title=selected_option,
            description=beschreibung,
            color=0xff0000
        )
        
        for command in commands:
            embed.add_field(name=command['name'], value=command['beschreibung'], inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self.view)