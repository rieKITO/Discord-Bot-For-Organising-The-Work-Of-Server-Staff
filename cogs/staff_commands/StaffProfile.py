import disnake
from disnake.ext import commands

import config
from cogs.DataBase import Data

class StaffProfile(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(description = "Посмотреть профиль модератора.")
    @commands.has_any_role(config.MODERATOR_ROLE_ID, *config.HIGHER_STAFF_ROLES)
    async def moderator_profile(self, interaction: disnake.CommandInteraction, user: disnake.User = None):
        _user = interaction.user
        if user:
            _user = user

        moderator = Data.staffUsers.find_one({"_id": _user.id, "moderator": True})

        if moderator:
                    
            embed = disnake.Embed(
                title = f"Профиль модератора - {_user.name}:",
                color = 0x292b2e,
            )
            embed.set_thumbnail(_user.avatar)
            embed.add_field(name = '> Стафф-баллы:', value = f"```{moderator['StaffPoints']}```", inline = True)
            embed.add_field(name = '> Баллы модератора:', value = f"```{moderator['WeekModeratorPoints']}```", inline = True)
            
        else:

            embed = disnake.Embed(
                description = f"Пользователь {_user.mention} ({_user.name}#{_user.discriminator}) не является модератором!",
                color = 0x292b2e,
            )
        
        await interaction.response.send_message(embed = embed)


    @commands.slash_command(description = "Посмотреть профиль хелпера.")
    @commands.has_any_role(config.HELPER_ROLE_ID, *config.HIGHER_STAFF_ROLES)
    async def helper_profile(self, interaction: disnake.CommandInteraction, user: disnake.User = None):
        _user = interaction.user
        if user:
            _user = user

        helper = Data.staffUsers.find_one({"_id": _user.id, "helper": True})

        if helper:
                    
            embed = disnake.Embed(
                title = f"Профиль хелпера - {_user.name}:",
                color = 0x292b2e,
            )
            embed.set_thumbnail(_user.avatar)
            embed.add_field(name = '> Стафф-баллы:', value = f"```{helper['StaffPoints']}```", inline = True)
            embed.add_field(name = '> Баллы хелпера:', value = f"```{helper['WeekHelperPoints']}```", inline = True)
            
        else:

            embed = disnake.Embed(
                description = f"Пользователь {_user.mention} ({_user.name}#{_user.discriminator}) не является хелпером!",
                color = 0x292b2e,
            )
        
        await interaction.response.send_message(embed = embed)


    @commands.slash_command(description = "Посмотреть профиль ивентера.")
    @commands.has_any_role(config.EVENTER_ROLE_ID, *config.HIGHER_STAFF_ROLES)
    async def eventer_profile(self, interaction: disnake.CommandInteraction, user: disnake.User = None):
        _user = interaction.user
        if user:
            _user = user

        eventer = Data.staffUsers.find_one({"_id": _user.id, "eventer": True})

        if eventer:
                    
            embed = disnake.Embed(
                title = f"Профиль ивентера - {_user.name}:",
                color = 0x292b2e,
            )
            embed.set_thumbnail(_user.avatar)
            embed.add_field(name = '> Стафф-баллы:', value = f"```{eventer['StaffPoints']}```", inline = True)
            embed.add_field(name = '> Баллы ивентера:', value = f"```{eventer['WeekEventerPoints']}```", inline = True)
            
        else:

            embed = disnake.Embed(
                description = f"Пользователь {_user.mention} ({_user.name}#{_user.discriminator}) не является ивентером!",
                color = 0x292b2e,
            )
        
        await interaction.response.send_message(embed = embed)


def setup(bot):
    bot.add_cog(StaffProfile(bot))