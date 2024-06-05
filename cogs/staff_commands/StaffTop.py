import disnake
from disnake.ext import commands

import config
from cogs.models.DataBase import Data

class StaffTop(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description = "Посмотреть недельную статистику модераторов.")
    @commands.has_any_role(config.MODERATOR_ROLE_ID, *config.HIGHER_STAFF_ROLES)
    async def moderator_top(self, interaction: disnake.CommandInteraction):
        i = 1
        moderators = Data.staffUsers.find({"moderator": True}).sort("WeekModeratorPoints", -1)
                    
        embed = disnake.Embed(
            title = "Топ модераторов:",
            description = "\n",
            color = 0x292b2e,
        )

        for value in moderators:
            embed.description += f"\n{i}) <@{value['_id']}> - ***{value['WeekModeratorPoints']}*** недельных баллов"
            i += 1
        
        await interaction.response.send_message(embed = embed)

    @commands.slash_command(description = "Посмотреть недельную статистику хелперов.")
    @commands.has_any_role(config.HELPER_ROLE_ID, *config.HIGHER_STAFF_ROLES)
    async def helper_top(self, interaction: disnake.CommandInteraction):
        i = 1
        helpers = Data.staffUsers.find({"helper": True}).sort("WeekHelperPoints", -1)
                    
        embed = disnake.Embed(
            title = "Топ хелперов:",
            description = "\n",
            color = 0x292b2e,
        )

        for value in helpers:
            embed.description += f"\n{i}) <@{value['_id']}> - ***{value['WeekHelperPoints']}*** недельных баллов"
            i += 1
        
        await interaction.response.send_message(embed = embed)

    @commands.slash_command(description = "Посмотреть недельную статистику ивентеров.")
    @commands.has_any_role(config.EVENTER_ROLE_ID, *config.HIGHER_STAFF_ROLES)
    async def eventer_top(self, interaction: disnake.CommandInteraction):
        i = 1
        eventers = Data.staffUsers.find({"eventer": True}).sort("WeekEventerPoints", -1)
                    
        embed = disnake.Embed(
            title = "Топ ивентеров:",
            description = "\n",
            color = 0x292b2e,
        )

        for value in eventers:
            embed.description += f"\n{i}) <@{value['_id']}> - ***{value['WeekEventerPoints']}*** недельных баллов"
            i += 1
        
        await interaction.response.send_message(embed = embed)

def setup(bot):
    bot.add_cog(StaffTop(bot))