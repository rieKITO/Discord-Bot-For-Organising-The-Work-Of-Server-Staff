from typing import Optional
import disnake
import asyncio

class TicketModal(disnake.ui.Modal):
    def __init__(self, event: asyncio.Event):
        self.event = event
        self.reply = None
        self.timeout = 300

        components = [
            disnake.ui.TextInput(label="Ответ", placeholder="Введите ответ на вопрос", custom_id="reply"),
        ]
        title = "ОТВЕТ НА ТИКЕТ"
        super().__init__(title=title, components=components, custom_id="TicketModal")

    async def callback(self, interaction: disnake.ModalInteraction):
        self.reply = interaction.text_values['reply']
        self.event.set()
        await interaction.response.send_message("Вы успешно отправили ответ на тикет.", ephemeral=True)

