from typing import Optional
import disnake

class ReportView(disnake.ui.View):
    def __init__(self, interaction = None):
        super().__init__(timeout = None)
        self.value = Optional[str]
        if interaction:
            self.interaction = interaction

    async def disable_all_items(self, interaction: disnake.CommandInteraction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view = self)

    @disnake.ui.button(label = "Принять репорт", style = disnake.ButtonStyle.green, emoji = "✔")
    async def take_report(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        button.disabled = True
        button.style = disnake.ButtonStyle.gray
        await interaction.response.edit_message(view = self)
        self.interaction = interaction
        self.stop()

    @disnake.ui.button(label = "Закрыть репорт", style = disnake.ButtonStyle.blurple, emoji = "❌")
    async def close_report(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            button.disabled = True
            button.style = disnake.ButtonStyle.gray
            self.stop()
