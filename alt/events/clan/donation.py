import coc
from nextcord.ext import commands
import nextcord

class DonationEventsHandlers:
    def __init__(self, bot, clan_channel_mapping):
        self.bot = bot
        self.clan_channel_mapping = clan_channel_mapping

    def register_donation_events(self, client):
        client.add_events(
            self.on_clan_member_donation,
            self.on_clan_member_donation_receive
        )

    @coc.ClanEvents.member_donations()
    async def on_clan_member_donation(self, old_member, new_member):
        final_donated_troops = new_member.donations - old_member.donations
        channel_id = self.clan_channel_mapping.get(new_member.clan.tag)
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed = nextcord.Embed(
                    description=f"{new_member.name} has donated {final_donated_troops} troops.",
                    color=nextcord.Color.green()  # Grün für Spenden
                )
                await channel.send(embed=embed)
            else:
                print(f"Could not find channel for clan {new_member.clan.tag}")
        else:
            print(f"No channel mapping found for clan {new_member.clan.tag}")

    @coc.ClanEvents.member_received()
    async def on_clan_member_donation_receive(self, old_member, new_member):
        final_received_troops = new_member.received - old_member.received
        channel_id = self.clan_channel_mapping.get(new_member.clan.tag)
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed = nextcord.Embed(
                    description=f"{new_member.name} has received {final_received_troops} troops.",
                    color=nextcord.Color.red()  # Rot für Empfang
                )
                await channel.send(embed=embed)
            else:
                print(f"Could not find channel for clan {new_member.clan.tag}")
        else:
            print(f"No channel mapping found for clan {new_member.clan.tag}")

def setup(bot):
    bot.add_cog(DonationEventsHandlers(bot))