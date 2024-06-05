from typing import Optional
import disnake

import config

class StaffSelectView(disnake.ui.View):
    def __init__(self, interaction: disnake.CommandInteraction):
        super().__init__(timeout=20.0)
        self.interaction = interaction
        self.value = Optional[int]

    async def on_timeout(self):
        timeoutEmbed = disnake.Embed(
            description="Вы не успели ответить на взаимодействие!",
            color=0x292b2e,
        )
        await self.interaction.edit_original_message(embed=timeoutEmbed, view=None)

    @disnake.ui.select(
        placeholder="Выберите роль:",
        custom_id="StaffRoles",
        min_values=1,
        max_values=1,
        options=[
            disnake.SelectOption(label="Модератор", value=f"{config.MODERATOR_ROLE_ID}",
                                 emoji="<:moderator:1140786430512210052>"),
            disnake.SelectOption(label="Хелпер", value=f"{config.HELPER_ROLE_ID}",
                                 emoji="<:helper:1140786390972518531>"),
            disnake.SelectOption(label="Ивентер", value=f"{config.EVENTER_ROLE_ID}",
                                 emoji="<:eventer:1140786334752063518>")
        ]
    )
    async def select_callback(self, select, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            self.value = select.values[0]
            self.disabled = True
            self.stop()
