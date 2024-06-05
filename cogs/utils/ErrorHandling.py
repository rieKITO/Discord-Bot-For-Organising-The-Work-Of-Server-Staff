import disnake
from disnake.ext import commands

class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Missing required argument!")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don't have permissions!")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.reply("Command not found!")

    @commands.Cog.listener()
    async def on_slash_command_error(self, interaction: disnake.CommandInteraction, error):
        if isinstance(error, commands.MissingAnyRole):
            await interaction.response.send_message("Missing permission roles!", ephemeral = True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await interaction.response.send_message("Missing required argument!", ephemeral = True)
        elif isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions!", ephemeral = True)
        elif isinstance(error, commands.CommandNotFound):
            await interaction.response.send_message("Command not found!", ephemeral = True)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))

    