import nextcord

def create_season_embed(player_name, season, season_data):
    attacks_won = 0
    defenses_won = 0

    day_stats = []

    for day, (date, data) in enumerate(season_data.items(), start=1):
        num_attacks = data.get('num_attacks', 0)
        daily_defenses = len(data.get('defenses', []))
        daily_attack_trophies = sum(attack['change'] for attack in data.get('new_attacks', []))
        daily_defense_trophies = sum(defense['change'] for defense in data.get('new_defenses', []))
        attacks_won += len([attack for attack in data.get('new_attacks', []) if attack['change'] > 0])
        defenses_won += len([defense for defense in data.get('new_defenses', []) if defense['change'] > 0])

        if num_attacks > 0 or daily_defenses > 0:
            trophies = data.get('new_attacks', [])[-1]['trophies'] if data.get('new_attacks') else 'Unknown'
            day_stats.append(f"Day {day:2}  {daily_attack_trophies}⁶  {daily_defense_trophies}⁷  {trophies}")

    embed = nextcord.Embed(
        title=f"Saison {season} - {player_name}",
        description=f"**Attacks Won:** {attacks_won} | **Def Won:** {defenses_won}",
        color=0x00ff00
    )
    
    embed.add_field(name="Tagesstatistik", value="```\n" + "\n".join(day_stats) + "\n```", inline=False)

    return embed