import sqlite3
import os
import nextcord

db_path = os.path.join("datenbank", "umfrage", "utopia", "ut_cw_umfrage.db")

def get_db_connection():
    return sqlite3.connect(db_path)

def get_non_responders(jahr, monat):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT coc_name, user_id, COUNT(*) AS nicht_reagiert_count
        FROM ut_cw_umfrage
        WHERE reaction = 'nicht reagiert' AND substr(umfrage_datum, 4, 2) = ? AND substr(umfrage_datum, 7, 4) = ?
        GROUP BY coc_name, user_id
        ''',
        (monat, jahr)
    )
    results = cursor.fetchall()
    conn.close()
    return results

def create_non_responder_embeds(results, jahr, monat):
    max_results_per_embed = 20
    embeds = []
    current_embed_content = ""
    count = 0

    for index, (coc_name, user_id, nicht_reagiert_count) in enumerate(results):
        if index % max_results_per_embed == 0 and index != 0:
            embed = nextcord.Embed(description=current_embed_content)
            embeds.append(embed)
            current_embed_content = ""
        current_embed_content += (
            f"**CoC Name:** {coc_name}\n"
            f"**User ID:** <@{user_id}>\n"
            f"**Nicht reagiert:** {nicht_reagiert_count} x\n\n"
        )

    if current_embed_content:
        embed = nextcord.Embed(description=current_embed_content)
        embeds.append(embed)
    
    return embeds