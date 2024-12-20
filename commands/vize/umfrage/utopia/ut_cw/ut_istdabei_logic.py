import sqlite3
import json
import os
import nextcord

db_path = 'datenbank/umfrage/utopia/ut_cw_umfrage.db'
link_db_path = 'datenbank/link/discord_users.db'

def get_yes_responders(message_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT user_id FROM ut_cw_umfrage WHERE message_id = ? AND reaction = 'ja'
    ''', (message_id,))
    yes_responders = cursor.fetchall()
    conn.close()
    return [row[0] for row in yes_responders]

def get_linked_users():
    conn = sqlite3.connect(link_db_path)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT discord_id, player_tag FROM users
    ''')
    users = cursor.fetchall()
    conn.close()
    return [{"discord_id": row[0], "player_tag": row[1]} for row in users]

def get_clan_data(clan_tag):
    clan_file_path = f'datenbank/clan/{clan_tag}.json'
    if os.path.exists(clan_file_path):
        with open(clan_file_path, 'r') as f:
            return json.load(f)
    return None

async def show_yes_responders(bot, interaction, message_id):
    yes_responders = get_yes_responders(message_id)
    linked_users = get_linked_users()
    clan_data = get_clan_data('28VYRC2R8')  # Clan Tag für die Abfrage
    if not clan_data:
        await interaction.response.send_message(f'Die Clan-Datei konnte nicht gefunden werden.')
        return

    players_in_clan = {player['tag']: player for player in clan_data['memberList']}
    
    embed_description = ["**Players with 'Ja' Reactions:**"]
    no_clan_accounts = []

    for responder_id in yes_responders:
        member = interaction.guild.get_member(int(responder_id))
        if not member:
            continue
        display_name = member.display_name
        user_accounts = [user for user in linked_users if user['discord_id'] == responder_id]
        
        clan_accounts = [account for account in user_accounts if account['player_tag'] in players_in_clan]
        
        if clan_accounts:
            embed_description.append(f"<:green_tick:1255008226739486771> {display_name}")
            for account in clan_accounts:
                player_name = players_in_clan[account['player_tag']]['name']
                embed_description.append(f"    - {player_name}")
        else:
            no_clan_accounts.append(display_name)

    if no_clan_accounts:
        embed_description.append(f"\n**Users with no accounts in the Clan:**")
        for display_name in no_clan_accounts:
            embed_description.append(f"<:red_cross:1255008100231155792> {display_name}")

    embed = nextcord.Embed(description="\n".join(embed_description))
    embed.set_author(name="Clan Mitglieder mit 'Ja' Reaktionen", icon_url=clan_data['badgeUrls']['small'])
    
    await interaction.response.send_message(embed=embed)