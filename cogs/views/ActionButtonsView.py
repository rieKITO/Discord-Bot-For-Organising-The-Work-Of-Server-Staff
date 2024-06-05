from typing import Optional
import disnake

class ActionButtonsView(disnake.ui.View):
    
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


    @disnake.ui.button(label = "Выдать/снять стафф-баллы", style = disnake.ButtonStyle.blurple)
    async def staff_points_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "StaffPointsChange"
            self.stop()

    @disnake.ui.button(label = "Выдать выговор", style = disnake.ButtonStyle.red)
    async def push_reprimand(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "PushReprimand"
            self.stop()

    @disnake.ui.button(label = "Выдать/снять баллы модератора", style = disnake.ButtonStyle.blurple)
    async def moderator_points_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "ModeratorPointsChange"
            self.stop()

    @disnake.ui.button(label = "Выдать/снять баллы хелпера", style = disnake.ButtonStyle.blurple)
    async def helper_points_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "HelperPointsChange"
            self.stop()

    @disnake.ui.button(label = "Выдать/снять баллы ивентера", style = disnake.ButtonStyle.blurple)
    async def eventer_points_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "EventerPointsChange"
            self.stop()

    @disnake.ui.button(label = "Выдать/снять роль", style = disnake.ButtonStyle.blurple)
    async def role_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "RoleChange"
            self.stop()

    @disnake.ui.button(label = "Выдать мут", style = disnake.ButtonStyle.red)
    async def mute(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "mute"
            self.stop()

    @disnake.ui.button(label = "Выдать варн", style = disnake.ButtonStyle.red)
    async def warn(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "warn"
            self.stop()


    @disnake.ui.button(label = "Выдать бан", style = disnake.ButtonStyle.red)
    async def ban(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "ban"
            self.stop()


    @disnake.ui.button(label = "Снять мут", style = disnake.ButtonStyle.green)
    async def unmute(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "unmute"
            self.stop()


    @disnake.ui.button(label = "Снять варн", style = disnake.ButtonStyle.green)
    async def unwarn(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "unwarn"
            self.stop()


    @disnake.ui.button(label = "Снять бан", style = disnake.ButtonStyle.green)
    async def unban(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "unban"
            self.stop()

    @disnake.ui.button(label = "Снять все роли", style = disnake.ButtonStyle.red)
    async def remove_all_roles(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "RemoveAllRoles"
            self.stop()

    @disnake.ui.button(label = "История наказаний", style = disnake.ButtonStyle.gray)
    async def history_of_punishments(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "HistoryOfPunishments"
            self.stop()

    @disnake.ui.button(label = "История выговоров", style = disnake.ButtonStyle.gray)
    async def history_of_reprimands(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "HistoryOfReprimands"
            self.stop()

    @disnake.ui.button(label = "История ников", style = disnake.ButtonStyle.gray)
    async def history_of_nicknames(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "HistoryOfNicknames"
            self.stop()

    @disnake.ui.button(label = "Информация о бане", style = disnake.ButtonStyle.gray)
    async def ban_info(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "BanInfo"
            self.stop()

    @disnake.ui.button(label = "Изменить гендерную роль", style = disnake.ButtonStyle.green)
    async def gender_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "GenderChange"
            self.stop()

    @disnake.ui.button(label = "Выдать/снять ночную роль", style = disnake.ButtonStyle.green)
    async def night_role_change(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "NightRoleChange"
            self.stop()

    @disnake.ui.button(label = "Выдать ивент-бан", style = disnake.ButtonStyle.red)
    async def add_event_ban(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "AddEventBan"
            self.stop()

    @disnake.ui.button(label = "Снять ивент-бан", style = disnake.ButtonStyle.green)
    async def remove_event_ban(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "RemoveEventBan"
            self.stop()


    @disnake.ui.button(label = "Выход", style = disnake.ButtonStyle.red)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = "cancel"
            self.stop()

    @disnake.ui.button(style = disnake.ButtonStyle.red)
    async def refuse(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            await self.disable_all_items(interaction)
            self.value = False
            self.stop()
