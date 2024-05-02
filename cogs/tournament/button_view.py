from typing import Optional
import disnake

from cogs.tournament.tournament_modal import TournamentModal


class TournamentApplicationButton(disnake.ui.View):
    
    def __init__(self, bot):
        super().__init__(timeout = None)
        self.value = Optional[str]
        self.bot = bot


    @disnake.ui.button(label = "Подать заявку", style = disnake.ButtonStyle.blurple)
    async def tournament_application_button(self, button: disnake.ui.Button, interaction: disnake.CommandInteraction):
            await interaction.response.send_modal(modal = TournamentModal(self.value, self.bot))