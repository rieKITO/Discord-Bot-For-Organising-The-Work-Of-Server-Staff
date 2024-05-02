from disnake.ext import commands

from cogs.tournament.button_view import TournamentApplicationButton

import config

class TournamentApplication(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(*config.HIGHER_STAFF_ROLES)
    async def tournament_application(self, ctx):
        view = TournamentApplicationButton(self.bot)
        await ctx.send(view = view)


def setup(bot):
    bot.add_cog(TournamentApplication(bot))