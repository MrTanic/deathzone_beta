from nextcord.ext import commands

def load_owner_commands(bot):
    bot.load_extension("commands.owner.legend.player_tags_command")