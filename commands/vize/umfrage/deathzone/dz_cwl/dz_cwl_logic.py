import sqlite3
import nextcord
from datetime import datetime, timedelta
from bot.setup.discord.channel_ids import CWL_CHANNEL
from .dz_cwl_save_reaction import SaveCWLReactions

db_path = "datenbank/umfrage/deathzone/dz_cwl_umfrage.db"
member_db_path = "datenbank/member/deathzone_member.db"
save_reactions = SaveCWLReactions(db_path, member_db_path)

async def save_and_evaluate_cwl(bot, interaction, message_id):
    saison_datum = (datetime.now() + timedelta(days=30)).strftime("%m.%Y")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Holen Sie die CWL-Nachricht
        cwl_channel = bot.get_channel(CWL_CHANNEL)
        message = await cwl_channel.fetch_message(message_id)
        
        # Reaktionen speichern
        all_member_info = save_reactions.load_all_member_info()
        reacted_member_ids = set()
        user_reactions = {}

        for reaction in message.reactions:
            async for user in reaction.users():
                if user != bot.user:
                    user_id = str(user.id)
                    reacted_member_ids.add(user_id)
                    reaction_type = save_reactions.get_reaction_type(str(reaction.emoji))
                    
                    if user_id not in user_reactions:
                        user_reactions[user_id] = set()
                    user_reactions[user_id].add(reaction_type)

        # Reaktionen in die Datenbank speichern
        for user_id, reactions in user_reactions.items():
            coc_name = all_member_info.get(user_id, "Unbekannt")
            save_reactions.save_reaction_to_database(message_id, user_id, coc_name, reactions, saison_datum)

        # Mitglieder erfassen, die nicht reagiert haben
        non_reacted_members = {member_id for member_id in all_member_info if member_id not in reacted_member_ids}
        for member_id in non_reacted_members:
            coc_name = all_member_info.get(member_id, "Unbekannt")
            save_reactions.save_reaction_to_database(message_id, member_id, coc_name, {'nicht reagiert'}, saison_datum)

    except Exception as e:
        await interaction.followup.send(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)
        return

    # Reaktionen aus der Datenbank abrufen und das Embed erstellen
    cursor.execute("SELECT user_id, reaction, saison_datum FROM cwl_umfragen WHERE message_id = ?", (message_id,))
    reactions_data = cursor.fetchall()
    conn.close()

    if not reactions_data:
        await interaction.followup.send("Keine Daten für die angegebene Nachrichten-ID gefunden.", ephemeral=True)
        return

    reactions = {'ja': [], 'nein': [], 'zap': [], 'nicht reagiert': []}
    for user_id, reaction, _ in reactions_data:
        coc_name = all_member_info.get(user_id, "Unbekannt")
        reactions[reaction].append(coc_name)

    embed_description = f"Saison: {saison_datum}\n"
    embed = nextcord.Embed(title="CWL Reaktionsauswertung", description=embed_description, color=16532095)

    for reaction, names in reactions.items():
        embed.add_field(name=reaction.capitalize(), value=", ".join(names) if names else "Niemand", inline=False)

    await interaction.followup.send(embed=embed)