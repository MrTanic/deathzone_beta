import nextcord
from nextcord.ext import commands
import json
from Commands.Event.player_data import fetch_player_data  # Stelle sicher, dass du diese Funktion entsprechend implementiert hast

class PlayerRegistrationModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Event Registrierung")

        self.player_tag = nextcord.ui.TextInput(
            label="Spieler-Tag",
            placeholder="Gib deinen Spieler-Tag ein (z.B. #P0LYJC8C)",
            required=True,
            max_length=15,
        )
        self.add_item(self.player_tag)

    async def callback(self, interaction: nextcord.Interaction):
        success, player_name = fetch_player_data(self.player_tag.value)
        if success:
            data_entry = {"player_name": player_name, "player_tag": self.player_tag.value, "discord_id": interaction.user.id}
            try:
                with open('event_registrations.json', 'r+') as file:
                    data = json.load(file)
                    data.append(data_entry)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
            except FileNotFoundError:
                with open('event_registrations.json', 'w') as file:
                    json.dump([data_entry], file, indent=4)

            await interaction.response.send_message(f"Registrierung erfolgreich: {player_name}")
        else:
            await interaction.response.send_message("Spieler-Tag nicht gefunden oder ungültig.", ephemeral=True)

class EventRegistrationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='register_event', description="Registriere dich für das Event.")
    async def register_event(self, interaction: nextcord.Interaction):
        modal = PlayerRegistrationModal()
        await interaction.response.send_modal(modal)

    @nextcord.slash_command(name='deregister_event', description="Melde dich vom Event ab.")
    async def deregister_event(self, interaction: nextcord.Interaction, player_tag: str):
        try:
            with open('event_registrations.json', 'r+') as file:
                registrations = json.load(file)
                registration_index = next((i for i, registration in enumerate(registrations) if registration["player_tag"] == player_tag and str(registration["discord_id"]) == str(interaction.user.id)), None)
                
                if registration_index is not None:
                    player_name = registrations[registration_index]["player_name"]
                    del registrations[registration_index]
                    file.seek(0)
                    file.truncate()
                    json.dump(registrations, file, indent=4)
                    await interaction.response.send_message(f"{player_name} ({player_tag}) wurde erfolgreich vom Event abgemeldet.")
                else:
                    await interaction.response.send_message("Keine Registrierung mit dem angegebenen Spieler-Tag gefunden.")
        except FileNotFoundError:
            await interaction.response.send_message("Es gibt noch keine Registrierungen.")

def setup(bot):
    bot.add_cog(EventRegistrationCog(bot))