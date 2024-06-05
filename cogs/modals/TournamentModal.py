from typing import Optional
import disnake
import datetime

import config
from cogs.utils.NicknameAndIdSeparation import nickname_and_id_separation, link_plus_nickname_and_id, \
    nicknames_to_string


class TournamentModal(disnake.ui.Modal):
    def __init__(self, type: str, bot):
        self.timeout = 300
        self.bot = bot
        self.type = type
        self.reason = Optional[str]
        self.time = Optional[int]
        components = [
            disnake.ui.TextInput(label="Название команды", placeholder="Введите название команды",
                                 custom_id="team_name"),
            disnake.ui.TextInput(label="Капитан команды", placeholder="Ник, discord id", custom_id="captain"),
            disnake.ui.TextInput(label="Состав команды", placeholder="Ник, discord id, ник, discord id и т.д",
                                 custom_id="members"),
            disnake.ui.TextInput(label="id участников в игре", placeholder="Через запятую, в том же порядке",
                                 custom_id="game_id"),
            disnake.ui.TextInput(label="Ранги участников", placeholder="Через запятую, в том же порядке",
                                 custom_id="ranks"),
        ]

        title = "Заявка"
        super().__init__(title=title, components=components, custom_id="TournamentModal")

    async def callback(self, interaction: disnake.ModalInteraction):

        nicknames_and_identifiers = None
        captain_nickname_and_id = None
        members_game_id = None

        try:
            captain_nickname_and_id = link_plus_nickname_and_id(str(interaction.text_values['captain']))
        except:
            ...

        try:
            nicknames_and_identifiers = link_plus_nickname_and_id(str(interaction.text_values['members']))
        except:
            ...

        try:
            members_game_id = nicknames_to_string(str(interaction.text_values['game_id']))
        except:
            ...

        embed = disnake.Embed(
            title=f"Заявка на турнир. Команда: {interaction.text_values['team_name']}",
            color=0x292b2e,
            timestamp=datetime.datetime.now(),
        )
        embed.set_image(url="https://i.imgur.com/QzB7q9J.png")
        embed.add_field(name='> Название команды:', value=f"```{interaction.text_values['team_name']}```", inline=False)
        if captain_nickname_and_id:
            embed.add_field(name='> Капитан команды:', value=f"{captain_nickname_and_id}", inline=False)
        else:
            embed.add_field(name='> Капитан команды:', value=f"```{interaction.text_values['captain']}```",
                            inline=False)
        if nicknames_and_identifiers:
            embed.add_field(name='> Состав команды:', value=f"{nicknames_and_identifiers}", inline=False)
        else:
            embed.add_field(name='> Состав команды:', value=f"```{interaction.text_values['members']}```", inline=False)
        if members_game_id:
            embed.add_field(name='> id участников в игре:', value=f"```{members_game_id}```", inline=False)
        else:
            embed.add_field(name='> id участников в игре:', value=f"```{interaction.text_values['game_id']}```",
                            inline=False)
        embed.add_field(name='> Ранги участников:', value=f"```{interaction.text_values['ranks']}```", inline=False)

        channel = self.bot.get_channel(config.TOURNAMENT_APPLICATION_CHANNEL_ID)

        await interaction.response.send_message("Ваша заявка на участие была отправлена.", ephemeral=True)
        await channel.send(embed=embed)
