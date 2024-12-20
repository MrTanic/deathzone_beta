import json
import os
from .database import add_user, get_all_users, get_user_by_player_tag, delete_user_by_player_tag
from client.import_client import abstractClient
import nextcord

clans = {
    "~DeathZone~": "2JLQVYQ8",
    "DZ⚜️Academy": "2P82CQQJL",
    "DZ⚜️Immortality": "2P28YJ9L2",
    "DZ⚜️Utopia": "28VYRC2R8",
    "DZ⚜️Afterlife": "22UYU90JL",
    "DZ⚜️FighterZ": "2LRPVRCJ0",
    "-DeathZone-": "2LP29CJC9"
}

async def link_user_with_tag(bot, interaction, discord_id, player_tag):
    # Hier wird die ID aus der Erwähnung extrahiert, falls nötig
    if discord_id.startswith('<@') and discord_id.endswith('>'):
        discord_id = discord_id[2:-1]
        if discord_id.startswith('!'):
            discord_id = discord_id[1:]

    # Überprüfen, ob der Spieler-Tag bereits verlinkt ist
    existing_user = get_user_by_player_tag(player_tag)
    if existing_user:
        await interaction.response.send_message(f'Der Spieler-Tag {player_tag} ist bereits mit einem anderen Konto verlinkt.')
        return

    # Spielerinformationen aus der Clash of Clans API abrufen
    client = await abstractClient.get_client()
    try:
        player = await client.get_player(player_tag)
    except coc.NotFound:
        await interaction.response.send_message(f'Player tag {player_tag} not found.')
        return
    except coc.Maintenance:
        await interaction.response.send_message(f'The API is currently under maintenance. Please try again later.')
        return
    except coc.PrivateWarLog:
        await interaction.response.send_message(f'The clan war log is private. Cannot fetch the data.')
        return

    # Spieler in der Datenbank speichern
    add_user(discord_id, player_tag)

    # Bestätigungsnachricht senden
    discord_user = await bot.fetch_user(discord_id)
    confirmation_message = f'**{player.name} ({player.tag})** wurde erfolgreich mit **{discord_user.name}** verknüpft.'
    await interaction.response.send_message(confirmation_message)

async def delete_user(bot, interaction, player_tag):
    # Überprüfen, ob der Spieler-Tag existiert
    existing_user = get_user_by_player_tag(player_tag)
    if not existing_user:
        await interaction.response.send_message(f'Der Spieler-Tag {player_tag} wurde nicht gefunden.')
        return

    # Spieler aus der Datenbank löschen
    delete_user_by_player_tag(player_tag)

    # Bestätigungsnachricht senden
    await interaction.response.send_message(f'Der Spieler-Tag {player_tag} wurde erfolgreich gelöscht.')

async def list_linked_users(bot, interaction, clan_tag):
    clan_file_path = f'datenbank/clan/{clan_tag}.json'

    if not os.path.exists(clan_file_path):
        await interaction.response.send_message(f'Die Clan-Datei für {clan_tag} konnte nicht gefunden werden.')
        return

    with open(clan_file_path, 'r') as f:
        clan_data = json.load(f)

    users = get_all_users()
    players_in_clan = {player['tag']: player for player in clan_data['memberList']}
    player_names_in_clan = {player['tag']: player['name'] for player in clan_data['memberList']}
    clan_badge_url = clan_data['badgeUrls']['small']  # Annahme, dass die Badge-URL im JSON ist

    linked_players = []
    not_linked_in_clan = []

    for user in users:
        if user['player_tag'] in players_in_clan:
            linked_players.append(user)
    
    for player_tag, player_name in player_names_in_clan.items():
        if player_tag not in [user['player_tag'] for user in linked_players]:
            not_linked_in_clan.append({"tag": player_tag, "name": player_name})

    embed_description = []

    embed_description.append(f"**Players in the Server: {len(linked_players)}**")
    for user in linked_players:
        member = interaction.guild.get_member(int(user['discord_id']))
        player = players_in_clan[user['player_tag']]
        if member:
            embed_description.append(f"<:green_tick:1255008226739486771> `{member.display_name} | {player['name']}`")
        else:
            embed_description.append(f"<:green_tick:1255008226739486771> `{user['discord_id']} | {player['name']}`")
    
    if not_linked_in_clan:
        embed_description.append(f"\n**Players not Linked: {len(not_linked_in_clan)}**")
        for player in not_linked_in_clan:
            embed_description.append(f"<:red_cross:1255008100231155792> `{player['name']} | {player['tag']} ‏`")

    embed = nextcord.Embed(description="\n".join(embed_description))
    embed.set_author(name=f"{list(clans.keys())[list(clans.values()).index(clan_tag)]}", icon_url=clan_badge_url)
    
    await interaction.response.send_message(embed=embed)