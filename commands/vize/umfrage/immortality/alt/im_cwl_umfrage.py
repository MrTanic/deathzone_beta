import nextcord
from nextcord.ext import commands
from bot.setup.discord.has_permissions import has_permission
from bot.setup.discord.channel_ids import IM_ANNOUNCEMENT_CHANNEL

class ImCWLCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='im_cwl_announcement', description='Sendet eine Ankündigung für die kommende CWL', guild_ids=[884325196104884248])
    async def cwl_announcement(self, interaction: nextcord.Interaction):
        if not has_permission(interaction.user, 'imvize') and not has_permission(interaction.user, 'owner'):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
            return

        await self.announce_cwl(interaction)

    async def announce_cwl(self, interaction):
        channel = self.bot.get_channel(IM_ANNOUNCEMENT_CHANNEL)
        if not channel:
            return

        message_content = "Hallo zusammen <@&893503798704742450> !"
        embed = nextcord.Embed(
            title="CWL Ankündigung",
            description=(
                "Dies ist die **Umfrage**, für die **kommende CWL**.\n\n"
                "Bitte alle eigenständig Abstimmen, somit können wir Vize vorausschauender und besser planen.\n\n"
                "<:ja:961978768765911110> <:arrow2:920341386757279824> wenn du **dabei** sein willst\n"
                "<:nein:961978783483699251> <:arrow2:920341386757279824> wenn du **nicht** dabei sein willst\n"
                "<:zap:1204471668198875156> <:arrow2:920341386757279824> wenn du **mehrere** Accounts anmelden willst\n\n"
                "Alle die sich anmelden, werden auf unsere Clanfamilie aufgeteilt. "
                "Gerne können Präferenzen mitgeteilt werden, wo ihr gerne spielen wollt.\n\n"
                "~ euer <@&893503791532503101> Team ⚜️"
            ),
            color=16532095
        )
        message = await channel.send(content=message_content, embed=embed)
        emojis = ["<:ja:961978768765911110>", "<:nein:961978783483699251>", "<:zap:1204471668198875156>"]
        for emoji in emojis:
            await message.add_reaction(emoji)

        await interaction.response.send_message("CWL Ankündigung wurde manuell im Kanal gesendet.", ephemeral=True)

def setup(bot):
    bot.add_cog(ImCWLCommand(bot))