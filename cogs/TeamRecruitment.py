from typing import Optional
import disnake
from disnake.ext import commands
import datetime

import config


class TeamRecruitmentModal(disnake.ui.Modal):
    def __init__(self, type: str, bot):
        self.timeout = 300
        self.bot = bot
        self.type = type
        self.reason = Optional[str]
        self.time = Optional[int]
        components = [
            disnake.ui.TextInput(label = "Имя и возраст", placeholder = "Введите свое имя и возраст", custom_id = "NameAndAge"),
            disnake.ui.TextInput(label = "Расскажите о себе", placeholder = "Расскажите о себе", custom_id = "info"),
            disnake.ui.TextInput(label = "Состояли ли вы в стаффе на других серверах?", placeholder = "Опишите свой опыт", custom_id = "experience"),
            disnake.ui.TextInput(label = "Сколько времени вы готовы уделять серверу?", placeholder = "Пример (с 10:00 до 15:00)", custom_id = "time"),
            disnake.ui.TextInput(label = "Какой у вас часовой пояс", placeholder = "Укажите часовой пояс", custom_id = "TimeZone")
        ]
        
        title = "Набор в стафф"
        super().__init__(title = title, components = components, custom_id = "TeamRecruitmentModal")
        

    async def callback(self, interaction: disnake.ModalInteraction):
        embed = disnake.Embed(
            color = 0x292b2e,
            timestamp = datetime.datetime.now(),
        )
        embed.set_footer(text = f"ID пользователя: {interaction.user.id}", icon_url = interaction.user.avatar)
        embed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
        embed.add_field(name = '> Пользователь:', value = f"{interaction.user.mention} - ({interaction.user.name}#{interaction.user.discriminator})", inline = False)
        embed.add_field(name = '> Имя и возраст:', value = f"```{interaction.text_values['NameAndAge']}```", inline = False)
        embed.add_field(name = '> О себе:', value = f"```{interaction.text_values['info']}```", inline = False)
        embed.add_field(name = '> Другие проекты и опыт:', value = f"```{interaction.text_values['experience']}```", inline = False)
        embed.add_field(name = '> Время:', value = f"```{interaction.text_values['time']}```", inline = False)
        embed.add_field(name = '> Часовой пояс:', value = f"```{interaction.text_values['TimeZone']}```", inline = False)

        if self.type == "moderator":
            embed.title = "НАБОР В КОМАНДУ МОДЕРАТОРОВ"
            embed.set_thumbnail(url = "https://i.imgur.com/fx7yKl3.png")
        elif self.type == "helper":
            embed.title = "НАБОР В КОМАНДУ ХЕЛПЕРОВ"
            embed.set_thumbnail(url = "https://i.imgur.com/oWTSdDO.png")
        elif self.type == "eventer":
            embed.title = "НАБОР В КОМАНДУ ИВЕНТЕРОВ"
            embed.set_thumbnail(url = "https://i.imgur.com/qrWJbtU.png")
        
        channel = self.bot.get_channel(config.RECRUITMENT_CHANNEL_ID)
        await interaction.response.send_message("Ваша заявка была отправлена. Если она нам подойдет, то с вами в ближайшее время свяжутся.", ephemeral = True)
        await channel.send(embed = embed)


class StaffSelect(disnake.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        self.value = Optional[int]
        options = [
            disnake.SelectOption(label = "Набор в команду модераторов", value = "moderator", emoji = "<:moderator:1140786430512210052>"),
            disnake.SelectOption(label = "Набор в команду хелперов", value = "helper", emoji = "<:helper:1140786390972518531>"),
            disnake.SelectOption(label = "Набор в команду ивентеров", value = "eventer", emoji = "<:eventer:1140786334752063518>")
        ]
        super().__init__(placeholder = "Подать заявку:", options = options, custom_id = "StaffRoles", min_values = 0, max_values = 1)

    async def callback(self, interaction: disnake.MessageInteraction):
        self.value = interaction.values[0]
        await interaction.response.send_modal(modal = TeamRecruitmentModal(self.value, self.bot))


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