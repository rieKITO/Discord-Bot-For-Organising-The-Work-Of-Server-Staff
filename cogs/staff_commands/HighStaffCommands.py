import disnake
from disnake.ext import commands
import datetime
from disnake.utils import get

from cogs.models.Models import StaffUser
from cogs.views.StaffSelectView import StaffSelectView


import config

from cogs.models.DataBase import Data

class HighStaffCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild = self.bot.get_guild(config.GUILD_ID)

    @commands.slash_command(description = "Выдать/снять стафф роль пользователю.")
    @commands.has_any_role(*config.HIGHER_STAFF_ROLES)
    async def staff_control(self, interaction: disnake.CommandInteraction, user: disnake.User = None):
        ObjectUser = interaction.user
        
        if user:
            ObjectUser = user

        MainEmbed = disnake.Embed(
            title = "ВЫДАЧА/СНЯТИЕ СТАФФ РОЛИ",
            description = f"{interaction.user.mention}, выберите одну из доступных ролей, " +
                          f"которую хотите выдать/снять пользователю {ObjectUser.mention} - {ObjectUser.name}#{ObjectUser.discriminator}",
            color = 0x292b2e,
            timestamp = datetime.datetime.now(),
        )
        MainEmbed.set_thumbnail(interaction.user.avatar)
        MainEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")

        view = StaffSelectView(interaction)
        await interaction.response.send_message(embed = MainEmbed, view = view)
        await view.wait()

        if int(view.value) in config.STAFF_ROLES:
            role = get(self.guild.roles, id = int(view.value))

            ResultEmbed = disnake.Embed(
                title = "ВЫДАЧА/СНЯТИЕ СТАФФ РОЛИ",
                color = 0x292b2e,
                timestamp = datetime.datetime.now(),
            )
            ResultEmbed.set_thumbnail(interaction.user.avatar)
            ResultEmbed.set_footer(text = f"ID пользователя: {ObjectUser.id}", icon_url = ObjectUser.avatar)
            ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                       
            if role not in ObjectUser.roles:
                await ObjectUser.add_roles(role)
                ResultEmbed.description = f"{interaction.user.mention}, вы успешно выдали роль <@&{role.id}> пользователю {ObjectUser.mention} - {ObjectUser.name}#{ObjectUser.discriminator}"

            else:
                await ObjectUser.remove_roles(role)
                ResultEmbed.description = f"{interaction.user.mention}, вы успешно сняли роль <@&{role.id}> у пользователя {ObjectUser.mention} - {ObjectUser.name}#{ObjectUser.discriminator}"
            
            await interaction.edit_original_message(embed = ResultEmbed, view = None)        

    @commands.slash_command(description = "Очистить недельную статистику модераторов.")
    @commands.has_any_role(*config.HIGHER_STAFF_ROLES)
    async def moderator_reset(self, interaction: disnake.CommandInteraction):
        embed = disnake.Embed(
            title = "ОЧИСТКА СТАТИСТИКИ (МОДЕРАТОРЫ)",
            description = f"{interaction.user.mention}, вы успешно очистили недельную статистику модераторов!",
            color = 0x292b2e,
            timestamp = datetime.datetime.now(),
        )
        embed.set_thumbnail(interaction.user.avatar)

        moderators = Data.staffUsers.find({"moderator": True})

        for moderator in moderators:

            if moderator["WeekModeratorPoints"] > float(config.MODERATOR_NECESSARY_STATISTICS):
            
                points = (int(moderator["WeekModeratorPoints"]) - config.MODERATOR_NECESSARY_STATISTICS) / 2
                await interaction.channel.send(points)
                ObjectModerator = StaffUser(moderator["_id"])
                ObjectModerator.update_staff_points(float(points))

        Data.staffUsers.update_many({},
            {
                "$set":{
                    "WeekModeratorPoints": 0
                }
            }
        )
        
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(description = "Очистить недельную статистику хелперов.")
    @commands.has_any_role(*config.HIGHER_STAFF_ROLES)
    async def helper_reset(self, interaction: disnake.CommandInteraction):
        embed = disnake.Embed(
            title = "ОЧИСТКА СТАТИСТИКИ (ХЕЛПЕРЫ)",
            description = f"{interaction.user.mention}, вы успешно очистили недельную статистику хелперов!",
            color = 0x292b2e,
            timestamp = datetime.datetime.now(),
        )
        embed.set_thumbnail(interaction.user.avatar)

        helpers = Data.staffUsers.find({"helper": True})

        for helper in helpers:

            if helper["WeekHelperPoints"] > float(config.HELPER_NECESSARY_STATISTICS):
            
                points = (int(helper["WeekHelperPoints"]) - config.HELPER_NECESSARY_STATISTICS) / 2
                ObjectHelper = StaffUser(helper["_id"])
                ObjectHelper.update_staff_points(float(points))

        Data.staffUsers.update_many({},
            {
                "$set":{
                    "WeekHelperPoints": 0
                }
            }
        )
        
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(description = "Очистить недельную статистику ивентеров.")
    @commands.has_any_role(*config.HIGHER_STAFF_ROLES)
    async def eventer_reset(self, interaction: disnake.CommandInteraction):
        embed = disnake.Embed(
            title = "ОЧИСТКА СТАТИСТИКИ (ИВЕНТЕРЫ)",
            description = f"{interaction.user.mention}, вы успешно очистили недельную статистику ивентеров!",
            color = 0x292b2e,
            timestamp = datetime.datetime.now(),
        )
        embed.set_thumbnail(interaction.user.avatar)

        eventers = Data.staffUsers.find({"eventer": True})

        for eventer in eventers:

            if eventer["WeekEventerPoints"] > float(config.EVENTER_NECESSARY_STATISTICS):
            
                points = (int(eventer["WeekEventerPoints"]) - config.EVENTER_NECESSARY_STATISTICS) / 2
                ObjectEventer = StaffUser(eventer["_id"])
                ObjectEventer.update_staff_points(float(points))

        Data.staffUsers.update_many({},
            {
                "$set":{
                    "WeekEventerPoints": 0
                }
            }
        )
        
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(HighStaffCommands(bot))