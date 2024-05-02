from disnake.ext import commands

import config

class CogsControl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(config.DEVELOPER_ROLE_ID)
    async def load(self, ctx, cog: str):
        await self.bot.load_extension(f"cogs.{cog.lower()}")

    @commands.command()
    @commands.has_role(config.DEVELOPER_ROLE_ID)
    async def unload(self, ctx, cog: str):
        await self.bot.unload_extension(f"cogs.{cog.lower()}")

    @commands.command()
    @commands.has_role(config.DEVELOPER_ROLE_ID)
    async def reload(self, ctx, cog: str):
        await self.bot.reload_extension(f"cogs.{cog.lower()}")

def setup(bot):
    bot.add_cog(CogsControl(bot))