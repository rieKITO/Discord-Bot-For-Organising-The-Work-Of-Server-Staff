import disnake
from disnake.ext import commands
import datetime

from cogs.models.Models import StaffUser

from cogs.views.TicketView import TicketView

import config

class Ticket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description = "Задать вопрос по серверу")
    async def help(self, interaction: disnake.CommandInteraction, question: str):
        view = TicketView()
        view.remove_item(view.close_ticket)
        view.remove_item(view.reply_ticket)
        TicketChannel = self.bot.get_channel(config.TICKET_CHANNEL_ID)
        
        TicketEmbed = disnake.Embed(
            title = "ТИКЕТ",
            color = 0xffa5c7,
            timestamp = datetime.datetime.now(),
        )
        TicketEmbed.set_thumbnail(url = "https://i.imgur.com/atQdLTA.png")
        TicketEmbed.set_footer(text = f"ID пользователя: {interaction.user.id}", icon_url = interaction.user.avatar)
        TicketEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
        TicketEmbed.add_field(name = 'Пользователь:', value = f"{interaction.user.mention} - ({interaction.user.id})", inline = False)
        TicketEmbed.add_field(name = 'Вопрос:', value = f"{question}", inline = False)

        await interaction.response.send_message("Ваш вопрос был отправлен, в ближайшее время вам ответит хелпер.", ephemeral = True)
        message = await TicketChannel.send(f"<@&{config.HELPER_ROLE_ID}>", embed = TicketEmbed, view = view)
        await view.wait()


        PlaintiffEmbed = disnake.Embed(
            title = "ОТВЕТ НА ВОПРОС",
            description = f"Ответ от хелпера {view.interaction.user.mention} - ({view.interaction.user.name}#{view.interaction.user.discriminator})",
            color = 0x292b2e,
        )
        PlaintiffEmbed.add_field(name = 'Ваш вопрос:', value = f"{question}", inline = False)

        ReplyRow = ""
        RowLength = 0
        while view.exit == False:

            AceptedTicketEmbed = disnake.Embed(
                title = "ТИКЕТ НА РАССМОТРЕНИИ",
                description = f"Данный тикет находится на рассмотрении у хелпера {view.interaction.user.mention}",
                color = 0xffdf64,
                timestamp = datetime.datetime.now(),
            )
            AceptedTicketEmbed.set_thumbnail(url = "https://i.imgur.com/atQdLTA.png")
            AceptedTicketEmbed.set_footer(text = f"ID пользователя: {interaction.user.id}", icon_url = interaction.user.avatar)
            AceptedTicketEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
            AceptedTicketEmbed.add_field(name = 'Пользователь:', value = f"{interaction.user.mention} - ({interaction.user.id})", inline = False)
            AceptedTicketEmbed.add_field(name = 'Вопрос:', value = f"{question}", inline = False)
        
            view = TicketView(view.interaction)
            view.remove_item(view.take_ticket)
   
            await message.edit(embed = AceptedTicketEmbed, view = view)
            await view.wait()

            if view.reply is not None:
                ReplyRow += " " + view.reply
                RowLength += 1
                PlaintiffEmbed.add_field(name = f"Ответ #{RowLength}:", value = f"{view.reply}", inline = False)
                await interaction.user.send(embed = PlaintiffEmbed)

        ClosedTicketEmbed = disnake.Embed(
            title = "ТИКЕТ РАССМОТРЕН",
            description = f"Данный тикет был рассмотрен хелпером {view.interaction.user.mention}",
            color = 0x53ff19,
            timestamp = datetime.datetime.now(),
        )
        ClosedTicketEmbed.set_thumbnail(url = "https://i.imgur.com/atQdLTA.png")
        ClosedTicketEmbed.set_footer(text = f"ID пользователя: {interaction.user.id}", icon_url = interaction.user.avatar)
        ClosedTicketEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
        ClosedTicketEmbed.add_field(name = 'Пользователь:', value = f"{interaction.user.mention} - ({interaction.user.id})", inline = False)
        ClosedTicketEmbed.add_field(name = 'Вопрос:', value = f"{question}", inline = False)
        ClosedTicketEmbed.add_field(name = 'Ответ:', value = f"{ReplyRow}", inline = False)

        await message.edit(embed = ClosedTicketEmbed, view = None)

        ObjectHelper = StaffUser(view.interaction.user.id)
        ObjectHelper.update_helper_points(config.TICKET_POINTS)

        
def setup(bot):
    bot.add_cog(Ticket(bot))