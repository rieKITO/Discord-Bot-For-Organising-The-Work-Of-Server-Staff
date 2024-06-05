import disnake

class ActionPaginatorView(disnake.ui.View):
    CurrentPage: int = 1
    sep: int = 6

    def __init__(self, interaction: disnake.CommandInteraction):
        super().__init__(timeout=240)
        self.interaction = interaction

    async def on_timeout(self):
        timeoutEmbed = disnake.Embed(
            description="Время вышло!",
            color=0x292b2e,
        )
        await self.interaction.edit_original_message(embed=timeoutEmbed, view=None)

    async def disable_all_items(self, interaction: disnake.CommandInteraction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

    async def send(self, interaction):
        self.message = await self.interaction.edit_original_message(view=self)
        await self.update_message(self.data[:self.sep])

    def create_embed(self, data):
        if self.type == "HistoryOfPunishments":
            embed = disnake.Embed(
                title=f"ИСТОРИЯ НАКАЗАНИЙ - {self.user.name} | Всего наказаний: **{len(self.data)}**"
            )
            for item in data:
                embed.add_field(name=f"> ```Номер: {item['number']}```",
                                value=f"> **Тип наказания:** {item['type']}\n> **Причина:** {item['reason']}\n> **Дата:** {item['date']}\n> **Модератор:** <@{item['moderator_id']}>",
                                inline=True)

        elif self.type == "HistoryOfReprimands":
            embed = disnake.Embed(
                title=f"ИСТОРИЯ ВЫГОВОРОВ - {self.user.name} | Всего выговоров: **{len(self.data)}**"
            )
            for item in data:
                embed.add_field(name=f"> ```Номер: {item['number']}```",
                                value=f"> **Причина:** {item['reason']}\n> **Дата:** {item['date']}\n> **Куратор:** <@{item['curator_id']}>",
                                inline=True)

        elif self.type == "HistoryOfNicknames":
            embed = disnake.Embed(
                title=f"ИСТОРИЯ НИКОВ - {self.user.name} | Всего измененных ников: **{len(self.data)}**"
            )
            for item in data:
                embed.add_field(name=f"> ```Номер: {item['number']}```",
                                value=f"> **Ник:** {item['nickname']}\n> **Дата:** {item['date']}\n", inline=False)

        return embed

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        if self.CurrentPage == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = disnake.ButtonStyle.gray
            self.prev_button.style = disnake.ButtonStyle.gray

        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = disnake.ButtonStyle.green
            self.prev_button.style = disnake.ButtonStyle.primary

        if self.CurrentPage == int(len(self.data) / self.sep) + 1:
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = disnake.ButtonStyle.gray
            self.next_button.style = disnake.ButtonStyle.gray

        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = disnake.ButtonStyle.green
            self.next_button.style = disnake.ButtonStyle.primary

    @disnake.ui.button(label="|<", style=disnake.ButtonStyle.blurple)
    async def first_page_button(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await interaction.response.defer()
            self.CurrentPage = 1
            UntilItem = self.CurrentPage * self.sep
            FromItem = UntilItem - self.sep
            await self.update_message(self.data[:UntilItem])

    @disnake.ui.button(label="<", style=disnake.ButtonStyle.blurple)
    async def prev_button(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await interaction.response.defer()
            self.CurrentPage -= 1
            UntilItem = self.CurrentPage * self.sep
            FromItem = UntilItem - self.sep
            await self.update_message(self.data[FromItem:UntilItem])

    @disnake.ui.button(label="X", style=disnake.ButtonStyle.red)
    async def exit_button(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.interaction.delete_original_message()

    @disnake.ui.button(label=">", style=disnake.ButtonStyle.blurple)
    async def next_button(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await interaction.response.defer()
            self.CurrentPage += 1
            UntilItem = self.CurrentPage * self.sep
            FromItem = UntilItem - self.sep
            await self.update_message(self.data[FromItem:UntilItem])

    @disnake.ui.button(label=">|", style=disnake.ButtonStyle.blurple)
    async def last_page_button(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await interaction.response.defer()
            self.CurrentPage = int(len(self.data) / self.sep) + 1
            UntilItem = self.CurrentPage * self.sep
            FromItem = UntilItem - self.sep
            await self.update_message(self.data[FromItem:])

    @disnake.ui.button(label="Удалить наказание", style=disnake.ButtonStyle.green)
    async def delete_punishment(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "delete"
            self.stop()

    @disnake.ui.button(label="Удалить выговор", style=disnake.ButtonStyle.green)
    async def delete_reprimand(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "delete"
            self.stop()