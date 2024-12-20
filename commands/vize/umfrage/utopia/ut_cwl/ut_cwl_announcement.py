import nextcord
from bot.setup.discord.channel_ids import UT_CWL_CHANNEL
from bot.setup.discord.user_ids import UTOPIA_ROLE_ID

async def announce_ut_cwl(bot, interaction):
    channel = bot.get_channel(UT_CWL_CHANNEL)  # ID des Ankündigungskanals aus channel.py
    if not channel:
        await interaction.response.send_message("Ankündigungskanal nicht gefunden.", ephemeral=True)
        return

    message_content = f"Hallo zusammen <@&{UTOPIA_ROLE_ID}> !"
    embed = nextcord.Embed(
        title="CWL Ankündigung",
        description=(
            "Dies ist die **Umfrage**, für die **kommende CWL**.\n\n"
            "Bitte alle eigenständig Abstimmen, somit können wir Vize vorausschauender und besser planen.\n\nAnmeldung ist nun bis zum 28. des Monats geöffnet!\n\n"
            "<:ja:961978768765911110> <:arrow2:920341386757279824> wenn du **dabei** sein willst\n"
            "<:nein:961978783483699251> <:arrow2:920341386757279824> wenn du **nicht** dabei sein willst\n"
            "<:zap:1204471668198875156> <:arrow2:920341386757279824> wenn du **mehrere** Accounts anmelden willst\n\n"
            "Alle die sich anmelden, werden auf unsere Clanfamilie aufgeteilt. "
            "Gerne können Präferenzen mitgeteilt werden, wo ihr gerne spielen wollt.\n\n*Hinweis:\nDamit es korrekt ausgewertet werden kann wird nur eine Reaktion erwartet.*\n\n"
            "~ euer <@&1267820039524843530> Team ⚜️"
        ),
        color=16711680
    )
    message = await channel.send(content=message_content, embed=embed)
    emojis = ["<:ja:961978768765911110>", "<:nein:961978783483699251>", "<:zap:1204471668198875156>"]
    for emoji in emojis:
        await message.add_reaction(emoji)