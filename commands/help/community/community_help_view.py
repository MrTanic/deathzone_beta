import nextcord
import json
from .community_help_select import CommunityHelpSelect

class CommunityHelpView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        with open('commands/help/data/community_help_info.json', 'r') as f:
            community_info = json.load(f)

        options = [
            nextcord.SelectOption(label=opt['name']) 
            for opt in community_info['optionen']
        ]
        
        self.add_item(CommunityHelpSelect(options))