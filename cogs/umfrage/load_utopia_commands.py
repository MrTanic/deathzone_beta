# cogs/load_utopia_commands.py
def load_utopia_commands(bot):
    bot.load_extension("commands.vize.umfrage.utopia.ut_cw.ut_cw_cog")
    bot.load_extension("commands.vize.umfrage.utopia.ut_cwl.ut_cwl_cog")