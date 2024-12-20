import nextcord

# Mapping für Monatsnamen
MONTH_NAMES = {
    "01": "Januar",
    "02": "Februar",
    "03": "März",
    "04": "April",
    "05": "Mai",
    "06": "Juni",
    "07": "Juli",
    "08": "August",
    "09": "September",
    "10": "Oktober",
    "11": "November",
    "12": "Dezember"
}

def create_history_embed(player_name, player_tag, history_data):
    embed = nextcord.Embed(title=f"Legenden Historie", color=0x00ff00)
    embed.set_author(name=f"{player_name} ({player_tag})")

    history_by_year = {}
    for entry in history_data:
        year = entry['season'][:4]
        month = entry['season'][5:7]
        if year not in history_by_year:
            history_by_year[year] = []
        history_by_year[year].append((month, entry))

    for year, entries in sorted(history_by_year.items(), reverse=True):
        history_details = "\n".join(
            [f"`{MONTH_NAMES[month]: <9}` | 🏆{entry['trophies']} | 🌎{entry['rank']}" for month, entry in sorted(entries)]
        )
        embed.add_field(name=f"**{year}**", value=history_details or "Keine Daten verfügbar", inline=False)

    embed.set_footer(text="Daten von der ClashKing API, können ungenau sein.")
    
    return embed