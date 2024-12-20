import nextcord
from datetime import datetime
import pytz

def create_legend_embed(player_name, player_tag, date, legend_data):
    attacks = legend_data.get('new_attacks', [])
    defenses = legend_data.get('new_defenses', [])

    german_tz = pytz.timezone('Europe/Berlin')

    total_attack_trophies = sum(attack['change'] for attack in attacks)
    total_defense_trophies = sum(defense['change'] for defense in defenses)

    attack_details = "\n".join(
        [f"<:sword:1251199323006308367> {attack['change']} ({datetime.fromtimestamp(attack['time'], german_tz).strftime('%H:%M')})" for attack in attacks]
    )
    defense_details = "\n".join(
        [f"<:shield:1251198941198946364> {defense['change']} ({datetime.fromtimestamp(defense['time'], german_tz).strftime('%H:%M')})" for defense in defenses]
    )

    formatted_date = datetime.strptime(date, '%Y-%m-%d').astimezone(german_tz).strftime('%d.%m.%Y')

    if not attacks and not defenses:
        start_trophies = legend_data.get('start_trophies', 'Unbekannt')
        end_trophies = start_trophies
        trophies_diff = 0
        trophies_diff_emoji = ""
    else:
        all_changes = attacks + defenses
        latest_change = max(all_changes, key=lambda x: x['time'])
        current_trophies = latest_change['trophies']
        start_trophies = legend_data.get('start_trophies', current_trophies - total_attack_trophies + total_defense_trophies)
        end_trophies = current_trophies
        trophies_diff = end_trophies - start_trophies
        trophies_diff_emoji = "<:green_up:1233469177118068846>" if trophies_diff >= 0 else "<:red_down:1233469221619499079>"

    embed = nextcord.Embed(title=f"Legend-Log für\n{player_name} ({player_tag})", color=0x00ff00)
    embed.description = f"{formatted_date}\n[Profil](https://link.clashofclans.com/de?action=OpenPlayerProfile&tag={player_tag.replace('#', '')})"
    embed.add_field(name=f"Angriffe +{total_attack_trophies} <:throphy:1251446229548925068> <:sword:1251199323006308367>({len(attacks)}/8)", value=attack_details or "Keine Angriffe", inline=False)
    embed.add_field(name=f"Verteidigungen -{total_defense_trophies} <:throphy:1251446229548925068> <:shield:1251198941198946364>({len(defenses)}/8)", value=defense_details or "Keine Verteidigungen", inline=False)
    embed.add_field(name="Start", value=f"<:throphy:1251446229548925068> {start_trophies}", inline=False)
    embed.add_field(name="Trophäen-Differenz", value=f"{trophies_diff_emoji} {trophies_diff} <:throphy:1251446229548925068>", inline=False)
    embed.add_field(name="Aktueller Stand", value=f"<:throphy:1251446229548925068> {end_trophies}", inline=False)
    embed.set_footer(text="Daten von der ClashKing API, Angaben können ungenau sein.")

    return embed