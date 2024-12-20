
import nextcord

# Funktion zum Erstellen des Embeds für den Clan
def create_clan_embed(clan_info):
    tag = clan_info.get("tag", "N/A")
    name = clan_info.get("name", "N/A")
    clan_level = clan_info.get("clanLevel", "N/A")
    clan_points = clan_info.get("clanPoints", "N/A")
    clan_builder_base_points = clan_info.get("clanBuilderBasePoints", "N/A")
    clan_capital_points = clan_info.get("clanCapitalPoints", "N/A")
    capital_league = clan_info.get("capitalLeague", {}).get("name", "N/A")
    war_wins = clan_info.get("warWins", "N/A")
    war_ties = clan_info.get("warTies", "N/A")
    war_losses = clan_info.get("warLosses", "N/A")
    war_win_streak = clan_info.get("warWinStreak", "N/A")
    war_league = clan_info.get("warLeague", {}).get("name", "N/A")
    badge_url = clan_info.get("badgeUrls", {}).get("large", "")

    embed = nextcord.Embed(
        description=(
            f"**Clan Level:** {clan_level}\n"
            f"**Clan Punkte:** {clan_points}\n"
            f"**Builder Base Punkte:** {clan_builder_base_points}\n"
        ),
        color=0x00ff00
    )

    # Capital and Clan War information
    embed.add_field(
        name="Clan Capital",
        value=(
            f"**Punkte:** {clan_capital_points}\n"
            f"**League:** {capital_league}"
        ),
        inline=False
    )

    embed.add_field(
        name="Clan War",
        value=(
            f"**Gewonnen:** {war_wins}\n"
            f"**Verloren:** {war_losses}\n"
            f"**Unentschieden:** {war_ties}\n"
            f"**Sieges Serie:** {war_win_streak}\n"
            f"**Warleague:** {war_league}"
        ),
        inline=False
    )

    if badge_url:
        embed.set_author(name=f"{name} {tag}", icon_url=badge_url)

    return embed


# Funktion zum Erstellen des Embeds für Clan-Mitglieder
def create_clan_members_embed(members):
    members = sorted(members, key=lambda x: x.get("clanRank", 100))
    embed = nextcord.Embed(
        title="Clan Mitglieder",
        color=0x00ff00
    )
    
    member_details = []
    for member in members:
        league_icon = member.get("league", {}).get("iconUrls", {}).get("tiny", "")
        league_name = member.get("league", {}).get("name", "N/A")
        member_details.append(
            f"**Name:** {member['name']} {member['tag']}\n"
            f"**Rolle:** {member['role']}\n"
            f"**TH Level:** {member['townHallLevel']}\n"
            f"**XP Level:** {member['expLevel']}\n"
            f"**Trophäen:** {member['trophies']}\n"
            f"**Builder Base Trophäen:** {member['builderBaseTrophies']}\n"
            f"**Spenden:** {member['donations']}\n"
            f"**Erhaltene Spenden:** {member['donationsReceived']}\n"
            f"**Liga:** {league_name} {league_icon}\n"
            f"**Rang im Clan:** {member['clanRank']}\n"
            f"**Vorheriger Rang:** {member['previousClanRank']}\n"
            "\n"
        )
    
    embed.description = "\n".join(member_details)
    return embed

# Funktion zum Erstellen der Buttons
class ClanProfileButtons(nextcord.ui.View):
    def __init__(self, clan_tag, clan_name):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Clanprofil anzeigen", url=f"https://link.clashofclans.com/de?action=OpenClanProfile&tag={clan_tag}"))
        self.add_item(nextcord.ui.Button(label="Clash of Stats", url=f"https://www.clashofstats.com/clans/{clan_name}-{clan_tag}/summary"))