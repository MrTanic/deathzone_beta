# vize_help_view.py
import nextcord
import json
from .vize_help_select import VizeHelpSelect

class VizeHelpView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        with open('commands/help/data/vize_help_info.json', 'r') as f:
            vize_info = json.load(f)

        options = [
            nextcord.SelectOption(label=opt['name']) 
            for opt in vize_info['optionen']
        ]
        
        self.add_item(VizeHelpSelect(options))