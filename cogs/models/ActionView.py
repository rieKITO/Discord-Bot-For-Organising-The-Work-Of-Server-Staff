from typing import Optional
import disnake

class ActionButtons(disnake.ui.View):
    
    def __init__(self, interaction: disnake.CommandInteraction):
        super().__init__(timeout = 20.0)
        self.interaction = interaction
        self.value = Optional[str]


    async def on_timeout(self):
        timeoutEmbed = disnake.Embed(
            description = "Вы не успели ответить на взаимодействие!",
            color = 0x292b2e,
        )
        await self.interaction.edit_original_message(embed = timeoutEmbed, view = None)


    async def disable_all_items(self, interaction: disnake.CommandInteraction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view = self)


    @disnake.ui.button(label = "Выдать/снять стафф-баллы", style = disnake.ButtonStyle.blurple, emoji = "😒")
    async def staff_points_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "StaffPointsChange"
            self.stop()

    @disnake.ui.button(label = "Выдать выговор", style = disnake.ButtonStyle.red, emoji = "😒")
    async def push_reprimand(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "PushReprimand"
            self.stop()

    @disnake.ui.button(label = "Выдать/снять баллы модератора", style = disnake.ButtonStyle.blurple, emoji = "😒")
    async def moderator_points_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "ModeratorPointsChange"
            self.stop()

    @disnake.ui.button(label = "Выдать/снять баллы хелпера", style = disnake.ButtonStyle.blurple, emoji = "😒")
    async def helper_points_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "HelperPointsChange"
            self.stop()

    @disnake.ui.button(label = "Выдать/снять баллы ивентера", style = disnake.ButtonStyle.blurple, emoji = "😒")
    async def eventer_points_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "EventerPointsChange"
            self.stop()

    @disnake.ui.button(label = "Выдать/снять роль", style = disnake.ButtonStyle.blurple, emoji = "😒")
    async def role_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "RoleChange"
            self.stop()

    @disnake.ui.button(label = "Выдать мут", style = disnake.ButtonStyle.red, emoji = "😒")
    async def mute(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "mute"
            self.stop()

    @disnake.ui.button(label = "Выдать варн", style = disnake.ButtonStyle.red, emoji = "😜")
    async def warn(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "warn"
            self.stop()


    @disnake.ui.button(label = "Выдать бан", style = disnake.ButtonStyle.red, emoji = "😍")
    async def ban(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "ban"
            self.stop()


    @disnake.ui.button(label = "Снять мут", style = disnake.ButtonStyle.green, emoji = "👀")
    async def unmute(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "unmute"
            self.stop()


    @disnake.ui.button(label = "Снять варн", style = disnake.ButtonStyle.green, emoji = "😜")
    async def unwarn(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "unwarn"
            self.stop()


    @disnake.ui.button(label = "Снять бан", style = disnake.ButtonStyle.green, emoji = "👀")
    async def unban(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "unban"
            self.stop()

    @disnake.ui.button(label = "Снять все роли", style = disnake.ButtonStyle.red, emoji = "👀")
    async def remove_all_roles(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "RemoveAllRoles"
            self.stop()

    @disnake.ui.button(label = "История наказаний", style = disnake.ButtonStyle.gray, emoji = "👀")
    async def history_of_punishments(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "HistoryOfPunishments"
            self.stop()

    @disnake.ui.button(label = "История выговоров", style = disnake.ButtonStyle.gray, emoji = "👀")
    async def history_of_reprimands(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "HistoryOfReprimands"
            self.stop()

    @disnake.ui.button(label = "История ников", style = disnake.ButtonStyle.gray, emoji = "👀")
    async def history_of_nicknames(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "HistoryOfNicknames"
            self.stop()

    @disnake.ui.button(label = "Информация о бане", style = disnake.ButtonStyle.gray, emoji = "👀")
    async def ban_info(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "BanInfo"
            self.stop()

    @disnake.ui.button(label = "Изменить гендерную роль", style = disnake.ButtonStyle.green, emoji = "👀")
    async def gender_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "GenderChange"
            self.stop()

    @disnake.ui.button(label = "Выдать/снять ночную роль", style = disnake.ButtonStyle.green, emoji = "👀")
    async def night_role_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "NightRoleChange"
            self.stop()

    @disnake.ui.button(label = "Выдать ивент-бан", style = disnake.ButtonStyle.red, emoji = "👀")
    async def add_event_ban(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "AddEventBan"
            self.stop()

    @disnake.ui.button(label = "Снять ивент-бан", style = disnake.ButtonStyle.green, emoji = "👀")
    async def remove_event_ban(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "RemoveEventBan"
            self.stop()


    @disnake.ui.button(label = "Выход", style = disnake.ButtonStyle.red, emoji = "✖")
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "cancel"
            self.stop()


class AddOrRemoveChoice(disnake.ui.View):
    def __init__(self, interaction: disnake.CommandInteraction):
        super().__init__(timeout = 20.0)
        self.interaction = interaction
        self.value = Optional[str]

    async def on_timeout(self):
        timeoutEmbed = disnake.Embed(
            description = "Вы не успели ответить на взаимодействие!",
            color = 0x292b2e,
        )
        await self.interaction.edit_original_message(embed = timeoutEmbed, view = None)

    @disnake.ui.select(
        placeholder = "Выберите действие:",
        min_values = 1,
        max_values = 1,
        options = [
            disnake.SelectOption(label = "Выдать", value = "add"),
            disnake.SelectOption(label = "Снять", value = "remove")
        ]  
    )

    async def select_callback(self, select, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            self.value = select.values[0]
            self.disabled = True
            self.stop()


class PaginationActionView(disnake.ui.View):
    CurrentPage: int = 1
    sep: int = 6

    def __init__(self, interaction: disnake.CommandInteraction):
            super().__init__(timeout = 240)
            self.interaction = interaction

    async def on_timeout(self):
        timeoutEmbed = disnake.Embed(
            description = "Время вышло!",
            color = 0x292b2e,
        )
        await self.interaction.edit_original_message(embed = timeoutEmbed, view = None)

    async def disable_all_items(self, interaction: disnake.CommandInteraction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view = self)

    async def send(self, interaction):
        self.message = await self.interaction.edit_original_message(view=self)
        await self.update_message(self.data[:self.sep])

    def create_embed(self, data):
        if self.type == "HistoryOfPunishments":
            embed = disnake.Embed(
                title = f"ИСТОРИЯ НАКАЗАНИЙ - {self.user.name} | Всего наказаний: **{len(self.data)}**"
            )
            for item in data:
                embed.add_field(name = f"> ```Номер: {item['number']}```", value = f"> **Тип наказания:** {item['type']}\n> **Причина:** {item['reason']}\n> **Дата:** {item['date']}\n> **Модератор:** <@{item['moderator_id']}>", inline = True)

        elif self.type == "HistoryOfReprimands":
            embed = disnake.Embed(
                title = f"ИСТОРИЯ ВЫГОВОРОВ - {self.user.name} | Всего выговоров: **{len(self.data)}**"
            )
            for item in data:
                embed.add_field(name = f"> ```Номер: {item['number']}```", value = f"> **Причина:** {item['reason']}\n> **Дата:** {item['date']}\n> **Куратор:** <@{item['curator_id']}>", inline = True)

        elif self.type == "HistoryOfNicknames":
            embed = disnake.Embed(
                title = f"ИСТОРИЯ НИКОВ - {self.user.name} | Всего измененных ников: **{len(self.data)}**"
            )
            for item in data:
                embed.add_field(name = f"> ```Номер: {item['number']}```", value = f"> **Ник:** {item['nickname']}\n> **Дата:** {item['date']}\n", inline = False)

        return embed
    
    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed = self.create_embed(data), view = self)

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

    @disnake.ui.button(label = "|<", style = disnake.ButtonStyle.blurple)
    async def first_page_button(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await interaction.response.defer()
            self.CurrentPage = 1
            UntilItem = self.CurrentPage * self.sep
            FromItem = UntilItem - self.sep
            await self.update_message(self.data[:UntilItem])

    @disnake.ui.button(label = "<", style = disnake.ButtonStyle.blurple)
    async def prev_button(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await interaction.response.defer()
            self.CurrentPage -= 1
            UntilItem = self.CurrentPage * self.sep
            FromItem = UntilItem - self.sep
            await self.update_message(self.data[FromItem:UntilItem])

    @disnake.ui.button(label = "X", style = disnake.ButtonStyle.red)
    async def exit_button(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.interaction.delete_original_message()

    @disnake.ui.button(label = ">", style = disnake.ButtonStyle.blurple)
    async def next_button(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await interaction.response.defer()
            self.CurrentPage += 1
            UntilItem = self.CurrentPage * self.sep
            FromItem = UntilItem - self.sep
            await self.update_message(self.data[FromItem:UntilItem])

    @disnake.ui.button(label = ">|", style = disnake.ButtonStyle.blurple)
    async def last_page_button(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await interaction.response.defer()
            self.CurrentPage = int(len(self.data) / self.sep) + 1
            UntilItem = self.CurrentPage * self.sep
            FromItem = UntilItem - self.sep
            await self.update_message(self.data[FromItem:])

    @disnake.ui.button(label = "Удалить наказание", style = disnake.ButtonStyle.green)
    async def delete_punishment(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "delete"
            self.stop()

    @disnake.ui.button(label = "Удалить выговор", style = disnake.ButtonStyle.green)
    async def delete_reprimand(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "delete"
            self.stop()
        

class Choice(disnake.ui.View):

    def __init__(self, interaction: disnake.CommandInteraction):
        super().__init__(timeout=15.0)
        self.interaction = interaction
        self.value = Optional[bool]


    async def on_timeout(self):
        timeoutEmbed = disnake.Embed(
            description = "Вы не успели ответить на взаимодействие!",
            color = 0x292b2e,
        )
        await self.interaction.edit_original_message(embed = timeoutEmbed, view = None)


    async def disable_all_items(self, interaction: disnake.CommandInteraction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view = self)



    @disnake.ui.button(style = disnake.ButtonStyle.green, emoji = "✔")
    async def to_agree(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = True
            self.stop()


    @disnake.ui.button(style = disnake.ButtonStyle.red, emoji = "✖")
    async def refuse(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = False
            self.stop()


class ActionModal(disnake.ui.Modal):
    def __init__(self, argument):
        self.argument = argument
        self.reason = Optional[str]
        self.time = Optional[int]
        defaultComponents = [
            disnake.ui.TextInput(label = "REASON", placeholder = "Enter the reason", custom_id = "reason"),
            disnake.ui.TextInput(label = "TIME", placeholder = "Enter the time", custom_id = "time")
        ]
        warnComponents = [disnake.ui.TextInput(label = "REASON", placeholder = "Enter the reason", custom_id = "reason")]

        if self.argument == "mute":
            title = "MUTE"
            super().__init__(title = title, components = defaultComponents, custom_id = "ActionModal")
        elif self.argument == "ban": 
            title = "BAN"
            super().__init__(title = title, components = defaultComponents, custom_id = "ActionModal")
        else:
            title = "WARN"
            super().__init__(title = title, components = warnComponents, custom_id = "ActionModal")

    async def callback(self, interaction: disnake.ModalInteraction):
        self.reason = interaction.text_values["reason"]
        if self.argument != "warn":
            self.time = interaction.text_values["time"]
