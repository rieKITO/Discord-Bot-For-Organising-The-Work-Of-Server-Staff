from typing import Optional
import disnake

class TeamRecruitmentModal(disnake.ui.Modal):
    def __init__(self, type: str, bot):
        self.timeout = 300
        self.bot = bot
        self.type = type
        self.reason = Optional[str]
        self.time = Optional[int]
        components = [
            disnake.ui.TextInput(label="Имя и возраст", placeholder="Введите свое имя и возраст",
                                 custom_id="NameAndAge"),
            disnake.ui.TextInput(label="Расскажите о себе", placeholder="Расскажите о себе", custom_id="info"),
            disnake.ui.TextInput(label="Состояли ли вы в стаффе на других серверах?", placeholder="Опишите свой опыт",
                                 custom_id="experience"),
            disnake.ui.TextInput(label="Сколько времени вы готовы уделять серверу?",
                                 placeholder="Пример (с 10:00 до 15:00)", custom_id="time"),
            disnake.ui.TextInput(label="Какой у вас часовой пояс", placeholder="Укажите часовой пояс",
                                 custom_id="TimeZone")
        ]

        title = "Набор в стафф"
        super().__init__(title=title, components=components, custom_id="TeamRecruitmentModal")

    async def callback(self, interaction: disnake.ModalInteraction):
        embed = disnake.Embed(
            color=0x292b2e,
            timestamp=datetime.datetime.now(),
        )
        embed.set_footer(text=f"ID пользователя: {interaction.user.id}", icon_url=interaction.user.avatar)
        embed.set_image(url="https://i.imgur.com/QzB7q9J.png")
        embed.add_field(name='> Пользователь:',
                        value=f"{interaction.user.mention} - ({interaction.user.name}#{interaction.user.discriminator})",
                        inline=False)
        embed.add_field(name='> Имя и возраст:', value=f"```{interaction.text_values['NameAndAge']}```", inline=False)
        embed.add_field(name='> О себе:', value=f"```{interaction.text_values['info']}```", inline=False)
        embed.add_field(name='> Другие проекты и опыт:', value=f"```{interaction.text_values['experience']}```",
                        inline=False)
        embed.add_field(name='> Время:', value=f"```{interaction.text_values['time']}```", inline=False)
        embed.add_field(name='> Часовой пояс:', value=f"```{interaction.text_values['TimeZone']}```", inline=False)

        if self.type == "moderator":
            embed.title = "НАБОР В КОМАНДУ МОДЕРАТОРОВ"
            embed.set_thumbnail(url="https://i.imgur.com/fx7yKl3.png")
        elif self.type == "helper":
            embed.title = "НАБОР В КОМАНДУ ХЕЛПЕРОВ"
            embed.set_thumbnail(url="https://i.imgur.com/oWTSdDO.png")
        elif self.type == "eventer":
            embed.title = "НАБОР В КОМАНДУ ИВЕНТЕРОВ"
            embed.set_thumbnail(url="https://i.imgur.com/qrWJbtU.png")

        channel = self.bot.get_channel(config.RECRUITMENT_CHANNEL_ID)
        await interaction.response.send_message(
            "Ваша заявка была отправлена. Если она нам подойдет, то с вами в ближайшее время свяжутся.", ephemeral=True)
        await channel.send(embed=embed)

