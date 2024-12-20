# cogs/load_fighterz_commands.py
def load_fighterz_commands(bot):
    bot.load_extension("commands.ankuendigung.umfrage.fighterz.fz_cw_umfrage")
    bot.load_extension("commands.ankuendigung.umfrage.fighterz.fz_auswertung")
    
    