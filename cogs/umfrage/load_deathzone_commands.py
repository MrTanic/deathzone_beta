# cogs/load_deathzone_commands.py
def load_deathzone_commands(bot):
    bot.load_extension("commands.vize.umfrage.deathzone.dz_cw.dz_cw_cog")
    bot.load_extension("commands.vize.umfrage.deathzone.dz_cwl.dz_cwl_cog")