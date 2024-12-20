from nextcord.ext import commands

def load_family_commands(bot):
    bot.load_extension("commands.family.overview.clan_overview")
    bot.load_extension("commands.family.leaderboard.top_spieler")
    bot.load_extension("commands.family.clan_info.clan_info_command")
    bot.load_extension("commands.player.legend.legend_stats_cog")
    bot.load_extension("commands.family.overview.family_overview")