# cogs/load_immortality_commands.py
def load_immortality_commands(bot):
    bot.load_extension("commands.vize.umfrage.immortality.im_cwl.im_cwl_cog")
    bot.load_extension("commands.vize.umfrage.immortality.im_cw.im_cw_cog")
    
    