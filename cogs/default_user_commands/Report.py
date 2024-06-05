from typing import Optional
import disnake
from disnake.ext import commands
import datetime

from cogs.models.Models import StaffUser

from cogs.views.ReportView import ReportView

import config

class Report(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description = "Пожаловаться на пользователя")
    async def report(self, interaction: disnake.CommandInteraction, user: disnake.User, reason):
        view = ReportView()
        view.remove_item(view.close_report)
        ReportChannel = self.bot.get_channel(config.REPORT_CHANNEL_ID)
        
        ReportEmbed = disnake.Embed(
            title = "РЕПОРТ",
            color = 0xff0005,
            timestamp = datetime.datetime.now(),
        )
        ReportEmbed.set_thumbnail(url = "https://i.imgur.com/4cySEK6.png")
        ReportEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
        ReportEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
        ReportEmbed.add_field(name = 'Истец:', value = f"{interaction.user.mention} - ({interaction.user.id})", inline = False)
        ReportEmbed.add_field(name = 'Нарушитель:', value = f"{user.mention} - ({user.id})", inline = False)
        ReportEmbed.add_field(name = 'Причина:', value = f"{reason}", inline = False)
        if user.voice:
            ReportEmbed.add_field(name = 'Голосовой канал:', value = f"{user.voice.channel.mention}", inline = False)

        await interaction.response.send_message("Репорт был отправлен, в ближайшее время с вами свяжется модератор.", ephemeral = True)
        message = await ReportChannel.send(f"<@&{config.MODERATOR_ROLE_ID}>", embed = ReportEmbed, view = view)
        await view.wait()

        PlaintiffEmbed = disnake.Embed(
            title = "РЕПОРТ НА РАССМОТРЕНИИ",
            description = f"Ваш репорт находится на рассмотрении у модератора {view.interaction.user.mention} - ({view.interaction.user.name}#{view.interaction.user.discriminator}). Вскоре модератор свяжется с Вами!",
            color = 0x292b2e,
        )
        await interaction.user.send(embed = PlaintiffEmbed)

        AceptedReportEmbed = disnake.Embed(
            title = "РЕПОРТ НА РАССМОТРЕНИИ",
            description = f"Данный репорт находится на рассмотрении у модератора {view.interaction.user.mention}",
            color = 0xffdf64,
            timestamp = datetime.datetime.now(),
        )
        AceptedReportEmbed.set_thumbnail(url = "https://i.imgur.com/4cySEK6.png")
        AceptedReportEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
        AceptedReportEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
        AceptedReportEmbed.add_field(name = 'Истец:', value = f"{interaction.user.mention} - ({interaction.user.id})", inline = False)
        AceptedReportEmbed.add_field(name = 'Нарушитель:', value = f"{user.mention} - ({user.id})", inline = False)
        AceptedReportEmbed.add_field(name = 'Причина:', value = f"{reason}", inline = False)
        if user.voice:
            AceptedReportEmbed.add_field(name = 'Голосовой канал:', value = f"{user.voice.channel.mention}", inline = False)
        
        view = ReportView(view.interaction)
        view.remove_item(view.take_report)
   
        await message.edit(embed = AceptedReportEmbed, view = view)
        await view.wait()

        ClosedReportEmbed = disnake.Embed(
            title = "РЕПОРТ РАССМОТРЕН",
            description = f"Данный репорт был рассмотрен модератором {view.interaction.user.mention}",
            color = 0x53ff19,
            timestamp = datetime.datetime.now(),
        )
        ClosedReportEmbed.set_thumbnail(url = "https://i.imgur.com/4cySEK6.png")
        ClosedReportEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
        ClosedReportEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
        ClosedReportEmbed.add_field(name = 'Истец:', value = f"{interaction.user.mention} - ({interaction.user.id})", inline = False)
        ClosedReportEmbed.add_field(name = 'Нарушитель:', value = f"{user.mention} - ({user.id})", inline = False)
        ClosedReportEmbed.add_field(name = 'Причина:', value = f"{reason}", inline = False)
        if user.voice:
            ClosedReportEmbed.add_field(name = 'Голосовой канал:', value = f"{user.voice.channel.mention}", inline = False)

        await message.edit(embed = ClosedReportEmbed, view = None)

        ObjectModerator = StaffUser(view.interaction.user.id)
        ObjectModerator.update_moderator_points(config.REPORT_POINTS)

        
def setup(bot):
    bot.add_cog(Report(bot))