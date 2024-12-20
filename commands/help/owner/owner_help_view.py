import nextcord
import json
from .owner_help_select import OwnerHelpSelect

class OwnerHelpView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        with open('commands/help/data/owner_help_info.json', 'r') as f:
            owner_info = json.load(f)

        options = [
            nextcord.SelectOption(label=opt['name']) 
            for opt in owner_info['optionen']
        ]
        
        self.add_item(OwnerHelpSelect(options))