import disnake
import asyncio

from cogs.modals.TicketModal import TicketModal

class TicketView(disnake.ui.View):
    def __init__(self, interaction=None):
        super().__init__(timeout=None)
        self.event = asyncio.Event()
        self.reply = None
        self.exit = False
        if interaction:
            self.interaction = interaction

    async def disable_all_items(self, interaction: disnake.CommandInteraction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

    @disnake.ui.button(label="Принять тикет", style=disnake.ButtonStyle.green, emoji="✔")
    async def take_ticket(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        button.disabled = True
        button.style = disnake.ButtonStyle.gray
        await interaction.response.edit_message(view=self)
        self.interaction = interaction
        self.stop()

    @disnake.ui.button(label="Ответить на тикет", style=disnake.ButtonStyle.blurple, emoji="💕")
    async def reply_ticket(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            modal = TicketModal(self.event)
            await interaction.response.send_modal(modal=modal)
            await self.event.wait()
            self.reply = modal.reply
            self.stop()

    @disnake.ui.button(label="Закрыть тикет", style=disnake.ButtonStyle.red, emoji="🔹")
    async def close_ticket(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
        if interaction.user.id == self.interaction.user.id:
            button.disabled = True
            button.style = disnake.ButtonStyle.gray
            self.exit = True
            self.stop()
