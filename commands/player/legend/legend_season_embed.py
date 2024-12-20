import nextcord

# Mapping for superscript numbers
SUPERSCRIPT_NUMBERS = {
    0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴',
    5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹'
}

def to_superscript(number):
    return ''.join(SUPERSCRIPT_NUMBERS[int(digit)] for digit in str(number))

def create_season_embed(player_name, player_tag, season, season_data):
    day_stats = []
    total_attacks = 0
    total_defenses = 0

    for day, (date, data) in enumerate(season_data.items(), start=1):
        num_attacks = len(data.get('attacks', []))
        num_defenses = len(data.get('defenses', []))
        daily_attack_trophies = sum(data.get('attacks', []))
        daily_defense_trophies = sum(data.get('defenses', []))
        trophies = data.get('current_trophies', 'None')

        if num_attacks > 0 or num_defenses > 0:
            total_attacks += num_attacks
            total_defenses += num_defenses
            day_stats.append(
                f"Day {day:2}   {daily_attack_trophies}{to_superscript(num_attacks)}   {daily_defense_trophies}{to_superscript(num_defenses)}   {trophies}"
            )

    embed = nextcord.Embed(
        description=f"**Total Attacks:** {total_attacks} | **Total Defenses:** {total_defenses}",
        color=0x00ff00
    )
    
    embed.set_author(name=f"{player_name} ({player_tag})")
    embed.add_field(name="Tagesstatistik", value="```\n" + "\n".join(day_stats) + "\n```", inline=False)
    embed.set_footer(text=f"{season} Season")

    return embed