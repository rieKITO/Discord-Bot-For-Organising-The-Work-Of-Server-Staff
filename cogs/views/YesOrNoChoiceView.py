from typing import Optional
import disnake

class YesOrNoChoiceView(disnake.ui.View):

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
