from typing import Optional
import disnake

from cogs.modals.TeamRecruitmentModal import TeamRecruitmentModal

class StaffSelect(disnake.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        self.value = Optional[int]
        options = [
            disnake.SelectOption(label = "Набор в команду модераторов", value = "moderator", emoji = "<:moderator:1140786430512210052>"),
            disnake.SelectOption(label = "Набор в команду хелперов", value = "helper", emoji = "<:helper:1140786390972518531>"),
            disnake.SelectOption(label = "Набор в команду ивентеров", value = "eventer", emoji = "<:eventer:1140786334752063518>")
        ]
        super().__init__(placeholder = "Подать заявку:", options = options, custom_id = "StaffRoles", min_values = 0, max_values = 1)

    async def callback(self, interaction: disnake.MessageInteraction):
        self.value = interaction.values[0]
        await interaction.response.send_modal(modal = TeamRecruitmentModal(self.value, self.bot))

