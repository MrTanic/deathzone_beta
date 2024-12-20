from nextcord.ext import commands

def load_academy_commands(bot):
    # Laden Sie alle Academy Commands/Cogs hier
    bot.load_extension("commands.vize.umfrage.academy.ac_cw.ac_cw_cog")
    bot.load_extension("commands.vize.umfrage.academy.ac_cwl.ac_cwl_cog")