from collections import OrderedDict

def format_clan_data(clan):
    def format_badge(badge):
        return {
            "small": badge.small,
            "medium": badge.medium,
            "large": badge.large
        } if badge else None

    def format_league(league):
        return {
            "id": league.id,
            "name": league.name
        } if league else None

    def format_player_house_elements(elements):
        return [{"type": elem.type.value, "id": elem.id} for elem in elements]

    clan_data = OrderedDict({
        "tag": clan.tag,
        "name": clan.name,
        "type": clan.type,
        "description": clan.description,
        "location": {
            "id": clan.location.id,
            "name": clan.location.name,
            "isCountry": clan.location.is_country,
            "countryCode": clan.location.country_code
        } if clan.location else None,
        "isFamilyFriendly": clan.family_friendly,
        "badgeUrls": format_badge(clan.badge),
        "clanLevel": clan.level,
        "clanPoints": clan.points,
        "clanBuilderBasePoints": clan.builder_base_points,
        "clanCapitalPoints": getattr(clan, 'capital_points', None),
        "capitalLeague": format_league(clan.capital_league),
        "requiredTrophies": clan.required_trophies,
        "warFrequency": clan.war_frequency,
        "warWinStreak": clan.war_win_streak,
        "warWins": clan.war_wins,
        "warTies": clan.war_ties,
        "warLosses": clan.war_losses,
        "isWarLogPublic": clan.public_war_log,
        "warLeague": format_league(clan.war_league),
        "members": clan.member_count,
        "memberList": [{
            "tag": member.tag,
            "name": member.name,
            "role": str(member.role),
            "townHallLevel": member.town_hall,
            "expLevel": member.exp_level,
            "league": {
                "id": member.league.id,
                "name": member.league.name,
                "iconUrls": {
                    "small": member.league.icon.small,
                    "tiny": member.league.icon.tiny,
                    "medium": member.league.icon.medium
                }
            } if member.league else None,
            "trophies": member.trophies,
            "builderBaseTrophies": member.builder_base_trophies,
            "clanRank": member.clan_rank,
            "previousClanRank": member.clan_previous_rank,
            "donations": member.donations,
            "donationsReceived": member.received,
            "playerHouse": {
                "elements": format_player_house_elements(member.player_house_elements)
            } if hasattr(member, 'player_house_elements') else None,
            "builderBaseLeague": format_league(member.builder_base_league)
        } for member in clan.members]
    })
    return clan_data