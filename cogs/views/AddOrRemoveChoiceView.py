from typing import Optional
import disnake

class AddOrRemoveChoiceView(disnake.ui.View):
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

