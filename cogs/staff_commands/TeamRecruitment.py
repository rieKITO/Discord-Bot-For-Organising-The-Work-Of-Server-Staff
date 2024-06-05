import disnake
from disnake.ext import commands

import config

from cogs.selects.StaffSelect import StaffSelect

class TeamRecruitment(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(*config.HIGHER_STAFF_ROLES)
    async def team_recruitment(self, ctx):
        view = disnake.ui.View(timeout = None)
        view.add_item(StaffSelect(self.bot))
        
        embed = disnake.Embed(
            title = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀НАБОР В СТАФФ",
            description = "Понравился наш сервер и хочешь стать его частью?\n" +
                          "Мы как раз проводим набор в **команду**!\n" +
                          "\n**От тебя потребуется:**\n" +
                          "<a:arrow:1140371321683984424> **16** полных лет\n" +
                          "<a:arrow:1140371321683984424> Месяц без нарушений\n" +
                          "<a:arrow:1140371321683984424> Адекватность и стрессоустойчивость\n" +
                          "<a:arrow:1140371321683984424> Активность на сервере\n" +
                          "\n**Что тебя ждет:**\n" +
                          "<a:arrow:1140371321683984424> Дружный коллектив\n" +
                          "<a:arrow:1140371321683984424> Получение бесценного опыта\n" +
                          "<a:arrow:1140371321683984424> Возможность карьерного продвижения\n"
                          "\nЗаинтересовало? Рассмотри предложенные должности и скорее присоединяйся к нам!",
        )
        embed.set_footer(text = "Мы ждем именно тебя!")
        embed.set_image(url= "https://i.imgur.com/KljEzBX.gif")
        await ctx.send(embed = embed, view = view)

        
def setup(bot):
    bot.add_cog(TeamRecruitment(bot))