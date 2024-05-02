import datetime
import asyncio
import disnake
from disnake.ext import commands
from disnake.utils import get

import config

from cogs.models.models import User
from cogs.models.models import StaffUser
from cogs.DataBase import Data
from cogs.models.ActionView import ActionButtons
from cogs.models.ActionView import AddOrRemoveChoice
from cogs.models.ActionView import PaginationActionView
from cogs.models.ActionView import Choice

class Action(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    async def remove_specific_buttons_action(self, view: ActionButtons, interaction: disnake.CommandInteraction, _user):
        ObjectInteraction = StaffUser(interaction.user.id)

        if ObjectInteraction.curator == False and ObjectInteraction.developer == False and ObjectInteraction.admin == False:
            view.remove_item(view.staff_points_change)
            view.remove_item(view.push_reprimand)
            view.remove_item(view.moderator_points_change)
            view.remove_item(view.helper_points_change)
            view.remove_item(view.eventer_points_change)

            if ObjectInteraction.helper == False and ObjectInteraction.moderator == False:
                view.remove_item(view.role_change)
            
            if  ObjectInteraction.moderator == False:
                view.remove_item(view.mute)
                view.remove_item(view.warn)
                view.remove_item(view.ban)
                view.remove_item(view.unmute)
                view.remove_item(view.unwarn)
                view.remove_item(view.unban)
                view.remove_item(view.remove_all_roles)
                view.remove_item(view.ban_info)
                view.remove_item(view.history_of_punishments)

            if ObjectInteraction.helper == False:
                view.remove_item(view.gender_change)
                view.remove_all_roles(view.night_role_change)
            
            if ObjectInteraction.eventer == False:
                view.remove_item(view.add_event_ban)
                view.remove_item(view.remove_event_ban)

        else:
            inStaff = Data.staffUsers.find_one({"_id": _user.id})
            if inStaff:
                ObjectUser = StaffUser(_user.id)
                if ObjectUser.moderator == False:
                    view.remove_item(view.moderator_points_change)
                if ObjectUser.helper == False:
                    view.remove_item(view.helper_points_change)
                if ObjectUser.eventer == False:
                    view.remove_item(view.eventer_points_change)
            else:
                view.remove_item(view.history_of_reprimands)
                view.remove_item(view.staff_points_change)
                view.remove_item(view.push_reprimand)
                view.remove_item(view.moderator_points_change)
                view.remove_item(view.helper_points_change)
                view.remove_item(view.eventer_points_change)

    async def remove_specific_buttons_paginator(self, view: PaginationActionView, interaction: disnake.CommandInteraction, _user):
        ObjectInteraction = StaffUser(interaction.user.id)

        if view.type == "HistoryOfPunishments":
            view.remove_item(view.delete_reprimand)

        elif view.type == "HistoryOfReprimands":
            view.remove_item(view.delete_punishment)

        elif view.type == "HistoryOfNicknames":
            view.remove_item(view.delete_reprimand)
            view.remove_item(view.delete_punishment)
        
        if view.type == "HistoryOfPunishments" and ObjectInteraction.admin == False and ObjectInteraction.developer == False and ObjectInteraction.curator == False:
            view.remove_item(view.delete_punishment)

        elif view.type == "HistoryOfReprimands" and ObjectInteraction.admin == False and ObjectInteraction.developer == False and ObjectInteraction.curator == False:
            view.remove_item(view.delete_reprimand)

    @commands.slash_command(description = "Совершить действие над пользователем.")
    @commands.has_any_role(*config.STAFF_ROLES)
    async def action(self, interaction: disnake.CommandInteraction, user: disnake.User = None):
        guild = self.bot.get_guild(config.GUILD_ID)
        generalLogChannel = self.bot.get_channel(config.GENERAL_LOG_CHANNEL_ID)

        actionEmbed = disnake.Embed(
            title = "ДЕЙСТВИЕ",
            color = 0x292b2e,
            timestamp = datetime.datetime.now(),
        )

        _user = interaction.user
        if user:
            _user = user
            actionEmbed.description = f"{interaction.user.mention}, выберите действие над пользователем {_user.mention} ({_user.name}#{_user.discriminator})."
        else:
            actionEmbed.description = f"{interaction.user.mention}, выберите действие над самим собой."
        
        ObjectUser = User(_user.id)

        view = ActionButtons(interaction)
        await self.remove_specific_buttons_action(view, interaction, _user)
        await interaction.response.send_message(embed = actionEmbed, view = view)

        await view.wait()

        if view.value is None:
            await interaction.edit_original_message("Вы не успели ответить на взаимодействие!")

        else:

            def check_message(message):
                return message.channel == interaction.channel and message.author.id == interaction.user.id
            

            async def direct_message(user: disnake.User, type: str, reason: str = None, time: str = None):
                embed = disnake.Embed(
                    color = 0x292b2e,
                    timestamp = datetime.datetime.now(),
                )
                embed.set_image(url = "https://i.imgur.com/QzB7q9J.png")

                if reason:
                    embed.add_field(name = '> Причина:', value = f"```{reason}```", inline = True)
                if time:
                    embed.add_field(name = '> Время:', value = f"```{time}```", inline = True)

                if type == "mute":
                    embed.title = "МУТ"
                    embed.description = f"Вам был выдан мут на сервере KITO.\nМут был выдан модератором {interaction.user.mention} ({interaction.user.id})"

                elif type == "ban":
                    embed.title = "БАН"
                    embed.description = f"Вам был выдан бан на сервере KITO.\nБан был выдан модератором {interaction.user.mention} ({interaction.user.id})"

                elif type == "warn":
                    embed.title = "ВАРН"
                    embed.description = f"Вам был выдан варн на сервере KITO.\nВарн был выдан модератором {interaction.user.mention} ({interaction.user.id})"

                elif type == "EventBan":
                    embed.title = "ИВЕНТ-БАН"
                    embed.description = f"Вам был выдан ивент-бан на сервере KITO.\Ивент-бан был выдан ивентером {interaction.user.mention} ({interaction.user.id})"

                await _user.send(embed = embed)


            async def str_enter(interaction, argument: str):
                reasonAndTimeEmbed = disnake.Embed(
                    color = 0x292b2e,
                )

                if argument == "mute":
                    reasonAndTimeEmbed.description = "Введите причину и время:"

                elif argument == "points":
                    reasonAndTimeEmbed.description = "Введите количество баллов:"

                elif argument == "role":
                    reasonAndTimeEmbed.description = "Введите ID роли:"

                elif argument == "punishment":
                    reasonAndTimeEmbed.description = "Введите номер наказания:"

                else:
                    reasonAndTimeEmbed.description = "Введите причину:"

                await interaction.edit_original_message(embed = reasonAndTimeEmbed, view = None)

                try:
                    return await self.bot.wait_for('message', check = check_message, timeout = 30.0)
                except asyncio.TimeoutError:
                    return None


            async def timeout_embed(interaction):
                timeoutEmbed = disnake.Embed(
                    description = "Время истекло!",
                    color = 0x292b2e,
                )

                await interaction.edit_original_message(embed = timeoutEmbed)

                
            if view.value == "mute":

                if interaction.user.id == _user.id:
                    return await interaction.edit_original_message(embed = None, view = None, content = "Вы не можете выдать мут самому себе!")
                
                if _user.top_role.position >= interaction.user.top_role.position:
                    return await interaction.edit_original_message(embed = None, view = None, content = "Вы не можете выдать мут человеку с теми же правами/вышестоящему!")

                muteRole = get(guild.roles, id = config.MUTE_ROLE_ID)

                if muteRole not in user.roles:

                    ReasonAndTime = await str_enter(interaction, "mute")
                    ReasonAndTimeLine= str(ReasonAndTime.content)
                    
                    if ReasonAndTime:

                        await ReasonAndTime.delete()

                        list = ReasonAndTimeLine.split()
                        reason = ""
                        
                        for i in range(len(list) - 1):
                            reason += list[i] + " "
                        reason = reason[:len(reason) - 1]
                        
                        TimeString = list[len(list) - 1]
                        TimeType = TimeString[len(TimeString) - 1]

                        ObjectInteraction = StaffUser(interaction.user.id)
                        muteLogChannel = self.bot.get_channel(config.MUTE_LOG_CHANNEL_ID)

                        ResultEmbed = disnake.Embed(
                            title = "МУТ",
                            description = f"**Пользователь:** {user.mention}\n" +
                                        f"**Модератор:** {interaction.user.mention}",
                            color = 0x292b2e,
                            timestamp = datetime.datetime.now(),
                        )
                        ResultEmbed.set_thumbnail(url = "https://i.imgur.com/cE5MkYf.png")
                        ResultEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
                        ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                        ResultEmbed.add_field(name = '> Причина:', value = f"```{reason}```", inline = True)

                        if TimeType == 's':
                            time = int(TimeString[:-1])
                            EmbedTime = f"{TimeString[:-1]} секунд"
                            ResultEmbed.add_field(name = '> Время:', value = f"```{EmbedTime}```", inline = True)

                        elif TimeType == 'm':
                            time = int(TimeString[:-1]) * 60
                            EmbedTime = f"{TimeString[:-1]} минут"
                            ResultEmbed.add_field(name = '> Время:', value = f"```{EmbedTime}```", inline = True)

                        elif TimeType == 'h':
                            time = int(TimeString[:-1]) * 3600
                            EmbedTime = f"{TimeString[:-1]} часов"
                            ResultEmbed.add_field(name = '> Время:', value = f"```{EmbedTime}``", inline = True)

                        elif TimeType == 'd':
                            time = int(TimeString[:-1]) * 86400
                            EmbedTime = f"{TimeString[:-1]} дней"
                            ResultEmbed.add_field(name = '> Время:', value = f"```{EmbedTime}```", inline = True)

                        await user.add_roles(muteRole)
                        ObjectUser.set_mute_field(True)
                        ObjectUser.interaction_with_the_history_of_punishments("push", len(ObjectUser.HistoryOfPunishments) + 1, "Мут", interaction.user.id, reason, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                        await interaction.edit_original_message(embed = ResultEmbed, view = None)
                        await direct_message(_user, "mute", reason, EmbedTime)
                        await muteLogChannel.send(embed = ResultEmbed)
                        await generalLogChannel.send(embed = ResultEmbed)

                        ObjectInteraction.update_week_moderator_points(config.MUTE_POINTS)

                        await asyncio.sleep(time)

                        if muteRole in user.roles:

                            await user.remove_roles(muteRole)
                            ObjectUser.set_mute_field(False)

                            AutomaticRemoveMuteEmbed = disnake.Embed(
                                title = "Автоматическое снятие мута",
                                description = f"У пользователя {user.mention} ({user.name}#{user.discriminator}) был автоматически снят мут\n" +
                                              f"Мут был выдан модератором {interaction.user.mention} ({user.name}#{user.discriminator})",
                                color = 0x52ff5a,
                                timestamp = datetime.datetime.now(),
                            )
                            AutomaticRemoveMuteEmbed.set_thumbnail(url = "https://i.imgur.com/cE5MkYf.png")
                            AutomaticRemoveMuteEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
                            AutomaticRemoveMuteEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")

                            await muteLogChannel.send(embed = AutomaticRemoveMuteEmbed)
                            await generalLogChannel.send(embed = AutomaticRemoveMuteEmbed)

                    else:
                        await timeout_embed(interaction)

                else:

                    ResultEmbed = disnake.Embed(
                        description = f"У пользователя {user.mention} уже есть мут!",
                        color = 0x292b2e,
                    )

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)

                
            elif view.value == "warn":

                if interaction.user.id == _user.id:
                    return await interaction.edit_original_message(embed = None, view = None, content = "Вы не можете выдать варн самому себе!")
                
                if _user.top_role.position >= interaction.user.top_role.position:
                    return await interaction.edit_original_message(embed = None, view = None, content = "Вы не можете выдать мут человеку с теми же правами/вышестоящему!")

                reason = await str_enter(interaction, "warn")
                
                if reason:
                    
                    WarnLogChannel = self.bot.get_channel(config.WARN_LOG_CHANNEL_ID)
                    ObjectInteraction = StaffUser(interaction.user.id)

                    time = 14 * 86400

                    DateOfWarn = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    ObjectUser.push_warn(DateOfWarn)
                    ObjectUser.interaction_with_the_history_of_punishments("push", len(ObjectUser.HistoryOfPunishments) + 1, "Варн", interaction.user.id, str(reason.content), DateOfWarn)

                    ObjectUser = User(user.id)
                    CountOfWarns = 0
                    for value in ObjectUser.warns:
                        CountOfWarns += 1

                    if CountOfWarns >= 3:
                        banRole = get(guild.roles, id = config.BAN_ROLE_ID)
                        banLogChannel = self.bot.get_channel(config.BAN_LOG_CHANNEL_ID)
                        await user.add_roles(banRole)
                        ObjectUser.set_ban_field(True)
                        ObjectUser.interaction_with_the_history_of_punishments("push", len(ObjectUser.HistoryOfPunishments) + 1, "Бан", interaction.user.id, "3 варна", DateOfWarn)

                        ResultEmbed = disnake.Embed(
                            title = "БАН ЗА 3 ВАРНА",
                            description = f"**Пользователь:** {user.mention}\n" +
                                          f"**Модератор:** {interaction.user.mention}\n" +
                                          f"\nНе забудьте снять все роли с пользователя через команду **/action**",
                            color = 0x292b2e,
                            timestamp = datetime.datetime.now(),
                        )
                        ResultEmbed.set_thumbnail(url = "https://i.imgur.com/25ZMRDm.png")
                        ResultEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
                        ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                        ResultEmbed.add_field(name = '> Причина:', value = f"```3 варна```", inline = False)

                        await direct_message(_user, "ban", "3 варна")
                        await banLogChannel.send(embed = ResultEmbed)
                       

                    else:

                        ResultEmbed = disnake.Embed(
                            title = "ВАРН",
                            description = f"**Пользователь:** {user.mention}\n" +
                                        f"**Модератор:** {interaction.user.mention}",
                            color = 0x292b2e,
                            timestamp = datetime.datetime.now(),
                        )
                        ResultEmbed.set_thumbnail(url = "https://i.imgur.com/jDZUM38.png")
                        ResultEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
                        ResultEmbed.add_field(name = '> Причина:', value = f"```{reason.content}```", inline = True)
                        ResultEmbed.add_field(name = '> Время:', value = f"```14 дней```", inline = True)
                        ResultEmbed.add_field(name = '> Активных варнов:', value = f"```{CountOfWarns}```", inline = True)

                        await direct_message(_user, "warn", str(reason.content), "14 дней")
                        await WarnLogChannel.send(embed = ResultEmbed)


                    await reason.delete()

                    ObjectInteraction.update_week_moderator_points(config.WARN_POINTS)

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)
                    await generalLogChannel.send(embed = ResultEmbed)

                    await asyncio.sleep(time)

                    if ObjectUser.pull_warn(DateOfWarn):
                        AutomaticRemoveWarnEmbed = disnake.Embed(
                            title = "Автоматическое снятие варна",
                            description = f"У пользователя {user.mention} ({user.name}#{user.discriminator}) был автоматически снят варн\n" +
                                          f"Варн был выдан модератором {interaction.user.mention} ({user.name}#{user.discriminator})",
                            color = 0x52ff5a,
                            timestamp = datetime.datetime.now(),
                        )
                        AutomaticRemoveWarnEmbed.set_thumbnail(url = "https://i.imgur.com/jDZUM38.png")
                        AutomaticRemoveWarnEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
                        AutomaticRemoveWarnEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")

                        await WarnLogChannel.send(embed = AutomaticRemoveWarnEmbed)
                        await generalLogChannel.send(embed = AutomaticRemoveWarnEmbed)

                else:
                    await timeout_embed(interaction)


            elif view.value == "ban":

                if interaction.user.id == user.id:
                    return await interaction.edit_original_message(embed = None, view = None, content = "Вы не можете выдать бан самому себе!")
                
                ObjectInteraction = StaffUser(interaction.user.id)

                if ObjectInteraction.admin == False and ObjectInteraction.developer == False:
                    for role in user.roles:
                        if role.id in config.STAFF_ROLES:
                            return await interaction.edit_original_message(embed = None, view = None, content = "Вы не можете выдать бан человеку, находящемуся в стаффе!")

                banRole = get(guild.roles, id = config.BAN_ROLE_ID)

                if banRole not in user.roles:

                    reason = await str_enter(interaction, "ban")

                    if reason:
                        
                        banLogChannel = self.bot.get_channel(config.BAN_LOG_CHANNEL_ID)

                        ReasonForDB = str(reason.content)
                        await reason.delete()

                        choiceEmbed = disnake.Embed(
                            description = f"Вы уверены, что хотите выдать бан пользователю {user.mention} {user.name}#{user.discriminator}\n" +
                                           "Все роли забаненного пользователя будут удалены!",
                            color = 0x292b2e,
                        )

                        choiceView = Choice(interaction)
                        await interaction.edit_original_message(embed = choiceEmbed, view = choiceView)
                        await choiceView.wait()

                        if choiceView.value == True:

                            ResultEmbed = disnake.Embed(
                                title = "БАН",
                                description = f"**Пользователь:** {user.mention}\n" +
                                            f"**Модератор:** {interaction.user.mention}",
                                color = 0x292b2e,
                                timestamp = datetime.datetime.now(),
                            )
                            ResultEmbed.set_thumbnail(url = "https://i.imgur.com/25ZMRDm.png")
                            ResultEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
                            ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                            ResultEmbed.add_field(name = '> Причина:', value = f"```{ReasonForDB}```", inline = False)

                            await user.add_roles(banRole)
                            DateOfBan = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            ObjectUser.set_ban_field(True, interaction.user.id, ReasonForDB, DateOfBan)
                            ObjectUser.interaction_with_the_history_of_punishments("push", len(ObjectUser.HistoryOfPunishments) + 1, "Бан", interaction.user.id, ReasonForDB, DateOfBan)     

                            for role in user.roles:
                                if role.id not in config.STAFF_ROLES and role.id != config.BAN_ROLE_ID and role.id != config.MUTE_ROLE_ID and role.id != config.MALE_ROLE_ID and role.id != config.FEMALE_ROLE_ID:
                                    try:
                                        await user.remove_roles(role)
                                    except:
                                        ...

                            ObjectInteraction.update_week_moderator_points(config.BAN_POINTS)

                            await interaction.edit_original_message(embed = ResultEmbed, view = None)
                            await direct_message(_user, "ban", ReasonForDB)
                            await banLogChannel.send(embed = ResultEmbed)
                            await generalLogChannel.send(embed = ResultEmbed)

                        else:

                            refuseEmbed = disnake.Embed(
                                description = "Выход из команды action",
                                color = 0x292b2e,
                            )

                            await interaction.edit_original_message(embed = refuseEmbed, view = None)

                    else:
                        await timeout_embed(interaction)

                else:

                    ResultEmbed = disnake.Embed(
                        description = f"У пользователя {user.mention} уже есть бан!",
                        color = 0x292b2e,
                    )

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)


            elif view.value == "unmute":

                muteRole = get(guild.roles, id = config.MUTE_ROLE_ID)

                if muteRole in user.roles:

                    muteLogChannel = self.bot.get_channel(config.MUTE_LOG_CHANNEL_ID)

                    ResultEmbed = disnake.Embed(
                        title = "СНЯТИЕ МУТА",
                        description = f"**Пользователь:** {user.mention}\n" +
                                    f"**Модератор:** {interaction.user.mention}",
                        color = 0x292b2e,
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_thumbnail(url = "https://i.imgur.com/cE5MkYf.png")
                    ResultEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")

                    await user.remove_roles(muteRole)
                    ObjectUser.set_mute_field(False)

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)
                    await muteLogChannel.send(embed = ResultEmbed)
                    await generalLogChannel.send(embed = ResultEmbed)

                else:

                    ResultEmbed = disnake.Embed(
                        description = f"У пользователя {user.mention} ({user.name}#{user.discriminator}) нет мута!",
                        color = 0x292b2e,
                    )

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)


            elif view.value == "unwarn":

                DateOfWarn = ""
                CountOfWarns = 0
                for value in ObjectUser.warns:
                    DateOfWarn = value['date']
                    CountOfWarns += 1
                
                if DateOfWarn != "":

                    WarnLogChannel = self.bot.get_channel(config.WARN_LOG_CHANNEL_ID)

                    ResultEmbed = disnake.Embed(
                        title = "СНЯТИЕ ВАРНА",
                        description = f"**Пользователь:** {user.mention}\n" +
                                      f"**Модератор:** {interaction.user.mention}",
                        color = 0x292b2e,
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_thumbnail(url = "https://i.imgur.com/jDZUM38.png")
                    ResultEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                    ResultEmbed.add_field(name = '> Активных варнов:', value = f"```{CountOfWarns - 1}```", inline = True)
                  
                    ObjectUser.pull_warn(DateOfWarn)
                    
                    await interaction.edit_original_message(embed = ResultEmbed, view = None)
                    await WarnLogChannel.send(embed = ResultEmbed)
                    await generalLogChannel.send(embed = ResultEmbed)

                else:

                    ResultEmbed = disnake.Embed(
                        description = f"У пользователя {user.mention} ({user.name}#{user.discriminator}) нет варна!",
                        color = 0x292b2e,
                    )

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)

            elif view.value == "unban":

                banRole = get(guild.roles, id = config.BAN_ROLE_ID)

                if banRole in user.roles:

                    banLogChannel = self.bot.get_channel(config.BAN_LOG_CHANNEL_ID)

                    ResultEmbed = disnake.Embed(
                        title = "СНЯТИЕ БАНА",
                        description = f"**Пользователь:** {user.mention}\n" +
                                    f"**Модератор:** {interaction.user.mention}",
                        color = 0x292b2e,
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_thumbnail(url = "https://i.imgur.com/25ZMRDm.png")
                    ResultEmbed.set_footer(text = f"ID пользователя: {user.id}", icon_url = user.avatar)
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")

                    await user.remove_roles(banRole)
                    ObjectUser.set_ban_field(False)

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)
                    await banLogChannel.send(embed = ResultEmbed)
                    await generalLogChannel.send(embed = ResultEmbed)

                else:

                    ResultEmbed = disnake.Embed(
                        description = f"У пользователя {user.mention} ({user.name}#{user.discriminator}) нет бана!",
                        color = 0x292b2e,
                    )

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)

            
            elif view.value == "RemoveAllRoles":

                ObjectInteraction = StaffUser(interaction.user.id)

                if ObjectInteraction.admin == False and ObjectInteraction.developer == False:
                    for role in _user.roles:
                        if role.id in config.STAFF_ROLES:
                            return await interaction.edit_original_message(embed = None, view = None, content = "Вы не можете снять роли у человека, находящегося в стаффе!")

                for role in _user.roles:
                    if role.id not in config.STAFF_ROLES and role.id != config.BAN_ROLE_ID and role.id != config.MUTE_ROLE_ID and role.id != config.MALE_ROLE_ID and role.id != config.FEMALE_ROLE_ID:
                        try:
                            await _user.remove_roles(role)
                        except:
                            ...

                ResultEmbed = disnake.Embed(
                    title = "СНЯТИЕ ВСЕХ РОЛЕЙ",
                    description = f"**Пользователь:** {_user.mention}\n" +
                                f"**Модератор:** {interaction.user.mention}",
                    color = 0x292b2e,
                    timestamp = datetime.datetime.now(),
                )
                ResultEmbed.set_thumbnail(_user.avatar)
                ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)
                ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")

                await interaction.edit_original_message(embed = ResultEmbed, view = None)

            
            elif view.value == "HistoryOfPunishments":
                data = ObjectUser.HistoryOfPunishments

                if data:
                    view = PaginationActionView(interaction)
                    view.type = "HistoryOfPunishments"
                    view.user = _user
                    view.data = data

                    await self.remove_specific_buttons_paginator(view, interaction, _user)
                    await view.send(interaction)
                    await view.wait()

                    if view.value == "delete":
                        punishment = await str_enter(interaction, "punishment")

                        if punishment:

                            if str(punishment.content).isdigit():

                                if int(punishment.content) <= len(data):

                                    ObjectUser.interaction_with_the_history_of_punishments("pull", int(punishment.content))
                                    
                                    ResultEmbed = disnake.Embed(
                                        title = "УДАЛЕНИЕ НАКАЗАНИЯ", 
                                        description = f"{interaction.user.mention}, вы успешно очистили наказание **{punishment.content}** у пользователя {_user.mention} ({_user.name}#{_user.discriminator}).",
                                        color = 0x292b2e,
                                        timestamp = datetime.datetime.now(),
                                    )
                                    ResultEmbed.set_thumbnail(_user.avatar)
                                    ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)
                                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")

                                    await interaction.edit_original_message(embed = ResultEmbed, view = None)

                                else:
                                    await interaction.edit_original_message("Наказание указано неверно!", embed = None, view = None)

                            else:
                                await interaction.edit_original_message("Наказание указано неверно!", embed = None, view = None)

                            await punishment.delete()

                        else:
                            await timeout_embed(interaction)

                else:
                    ResultEmbed = disnake.Embed(
                        description = f"У пользователя {_user.mention} ({_user.name}#{_user.discriminator}) нет наказаний",
                        color = 0x292b2e,
                    )

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)


            elif view.value == "HistoryOfReprimands":
                ObjectStaffUser = StaffUser(_user.id)
                data = ObjectStaffUser.HistoryOfReprimands

                if data:
                    view = PaginationActionView(interaction)
                    view.type = "HistoryOfReprimands"
                    view.user = _user
                    view.data = data

                    await self.remove_specific_buttons_paginator(view, interaction, _user)
                    await view.send(interaction)
                    await view.wait()

                    if view.value == "delete":
                        reprimand = await str_enter(interaction, "reprimand")

                        if reprimand:

                            if str(reprimand.content).isdigit():

                                if int(reprimand.content) <= len(data):

                                    ObjectStaffUser.interaction_with_the_history_of_reprimands("pull", int(reprimand.content))
                                    
                                    ResultEmbed = disnake.Embed(
                                        title = "УДАЛЕНИЕ ВЫГОВОРА", 
                                        description = f"{interaction.user.mention}, вы успешно очистили выговор **{reprimand.content}** у пользователя {_user.mention} ({_user.name}#{_user.discriminator}).",
                                        color = 0x292b2e,
                                        timestamp = datetime.datetime.now(),
                                    )
                                    ResultEmbed.set_thumbnail(_user.avatar)
                                    ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)
                                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")

                                    await interaction.edit_original_message(embed = ResultEmbed, view = None)

                                else:
                                    await interaction.edit_original_message("Выговор указано неверно!", embed = None, view = None)

                            else:
                                await interaction.edit_original_message("Выговор указано неверно!", embed = None, view = None)

                            await reprimand.delete()

                        else:
                            await timeout_embed(interaction)

                else:
                    ResultEmbed = disnake.Embed(
                        description = f"У пользователя {_user.mention} ({_user.name}#{_user.discriminator}) нет выговоров",
                        color = 0x292b2e,
                    )

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)


            elif view.value == "HistoryOfNicknames":
                data = ObjectUser.HistoryOfNicknames

                if data:

                    view = PaginationActionView(interaction)
                    view.type = "HistoryOfNicknames"
                    view.user = _user
                    view.data = data

                    await self.remove_specific_buttons_paginator(view, interaction, _user)
                    await view.send(interaction)

                else:
                    ResultEmbed = disnake.Embed(
                        description = f"У пользователя {_user.mention} ({_user.name}#{_user.discriminator}) нет измененных ников!",
                        color = 0x292b2e,
                    )
                    await interaction.edit_original_message(embed = ResultEmbed, view = None)


            elif view.value == "BanInfo":

                if ObjectUser.ban != False:

                    ResultEmbed = disnake.Embed(
                        title = "ИНФОРМАЦИЯ О БАНЕ",
                        description = f"**Пользователь:** {_user.mention}\n" +
                                      f"**Модератор:** <@{ObjectUser.ban['moderator']}>",
                        color = 0x292b2e,
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_thumbnail(_user.avatar)
                    ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                    ResultEmbed.add_field(name = '> Причина:', value = f"```{ObjectUser.ban['reason']}```", inline = True)
                    ResultEmbed.add_field(name = '> Дата выдачи:', value = f"```{ObjectUser.ban['date']}```", inline = True)

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)

                else:

                    ResultEmbed = disnake.Embed(
                        description = f"У пользователя {_user.mention} ({_user.name}#{_user.discriminator}) нет бана!",
                        color = 0x292b2e,
                    )
                    await interaction.edit_original_message(embed = ResultEmbed, view = None)


            elif view.value == "GenderChange":

                ObjectInteraction = StaffUser(interaction.user.id)
                MaleRole = get(guild.roles, id = config.MALE_ROLE_ID)
                FemaleRole = get(guild.roles, id = config.FEMALE_ROLE_ID)

                ResultEmbed = disnake.Embed(
                    title = "ИЗМЕНЕНИЕ ГЕНДЕРНОЙ РОЛИ",
                    description = f"**Пользователь:** {_user.mention}\n" +
                                  f"**Хелпер:** {interaction.user.mention}",
                    timestamp = datetime.datetime.now(),
                )
                ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)
                

                if MaleRole in _user.roles:
                    await _user.remove_roles(MaleRole)
                    await _user.add_roles(FemaleRole)
                    
                    ResultEmbed.color = 0xff97b9
                    ResultEmbed.set_thumbnail(url = "https://i.imgur.com/kB2v6DY.png")

                elif FemaleRole in _user.roles:
                    await _user.remove_roles(FemaleRole)
                    await _user.add_roles(MaleRole)

                    ResultEmbed.color = 0x8db9fa
                    ResultEmbed.set_thumbnail(url = "https://i.imgur.com/PPryxQt.png")

                else:
                    await _user.add_roles(MaleRole)

                    ResultEmbed.color = 0x64e6ff
                    ResultEmbed.set_thumbnail(url = "https://i.imgur.com/rSigsn3.png")

                ObjectInteraction.update_week_helper_points(config.GENDER_CHANGE_POINTS)
                
                await interaction.edit_original_message(embed = ResultEmbed, view = None)


            elif view.value == "NightRoleChange":

                NightRole = get(guild.roles, id = config.NIGHT_ROLE_ID)

                ResultEmbed = disnake.Embed(
                    description = f"**Пользователь:** {_user.mention}\n" +
                                  f"**Хелпер:** {interaction.user.mention}",
                    color = 0x1b1b1b,
                    timestamp = datetime.datetime.now(),
                )
                ResultEmbed.set_thumbnail(url = "https://i.imgur.com/RvNyHg6.png")
                ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)

                if NightRole not in _user.roles:
                    await _user.add_roles(NightRole)

                    ObjectInteraction = StaffUser(interaction.user.id)
                    ObjectInteraction.update_week_helper_points(config.NIGHT_ROLE_CHANGE_POINTS)

                    ResultEmbed.title = "ВЫДАЧА НОЧНОЙ РОЛИ"
                    

                else:
                    await _user.remove_roles(NightRole)

                    ResultEmbed.title = "СНЯТИЕ НОЧНОЙ РОЛИ"
  
                await interaction.edit_original_message(embed = ResultEmbed, view = None)


            elif view.value == "StaffPointsChange":

                view = AddOrRemoveChoice(interaction)
                await interaction.edit_original_message(view = view)
                await view.wait()

                ObjectStaffUser = StaffUser(_user.id)
                points = await str_enter(interaction, "points")

                if points:

                    ResultEmbed = disnake.Embed(
                        color = 0x1b1b1b,
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                    ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)

                    if view.value == "add":
                        ObjectStaffUser.update_staff_points(float(points.content))

                        ResultEmbed.title = "ВЫДАЧА СТАФФ-БАЛЛОВ"

                        if interaction.user.id == _user.id:
                            ResultEmbed.description = f"{interaction.user.mention}, вы успешно выдали себе **{points.content}** стафф-баллов"
                        else:
                            ResultEmbed.description = f"{interaction.user.mention}, вы успешно выдали пользователю {_user.mention} ({_user.name}#{_user.discriminator}) **{points.content}** стафф-баллов"

                    else:
                        if float(ObjectStaffUser.StaffPoints) - float(points.content) >= 0: 
                            ObjectStaffUser.update_staff_points(float(points.content) * -1)

                            ResultEmbed.title = "СНЯТИЕ СТАФФ-БАЛЛОВ"

                            if interaction.user.id == _user.id:
                                ResultEmbed.description = f"{interaction.user.mention}, вы успешно сняли себе **{points.content}** стафф-баллов"
                            else:
                                ResultEmbed.description = f"{interaction.user.mention}, вы успешно сняли пользователю {_user.mention} ({_user.name}#{_user.discriminator}) **{points.content}** стафф-баллов"

                        else:
                            await points.delete()
                            return await interaction.edit_original_message(f"У пользователя нет такого количества баллов!", embed = None, view = None)

                    await points.delete()
                    await interaction.edit_original_message(embed = ResultEmbed, view = None)

                else:
                    await timeout_embed(interaction)

            
            elif view.value == "PushReprimand":

                if interaction.user.id == _user.id:
                    return await interaction.edit_original_message(embed = None, view = None, content = "Вы не можете выдать выговор самому себе!")
                
                if _user.top_role.position >= interaction.user.top_role.position:
                    return await interaction.edit_original_message(embed = None, view = None, content = "Вы не можете выдать выговор человеку с теми же правами/вышестоящему!")
                
                reason = await str_enter(interaction, "reprimand")

                if reason:
                    ResultEmbed = disnake.Embed(
                        title = "ВЫГОВОР",
                        description = f"**Пользователь:** {_user.mention}\n" +
                                      f"**Куратор:** {interaction.user.mention}",
                        color = 0xff0004,
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_thumbnail(_user.avatar)
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                    ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)
                    ResultEmbed.add_field(name = '> Причина:', value = f"```{reason.content}```", inline = True)

                    DateOfPunishment = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    ObjectStaffUser = StaffUser(_user.id)
                    ObjectStaffUser.interaction_with_the_history_of_reprimands("push", len(ObjectStaffUser.HistoryOfReprimands) + 1, interaction.user.id, str(reason.content), DateOfPunishment)

                    await reason.delete()
                    await interaction.edit_original_message(embed = ResultEmbed, view = None)

                else:
                    await timeout_embed(interaction)


            elif view.value == "ModeratorPointsChange":

                view = AddOrRemoveChoice(interaction)
                await interaction.edit_original_message(view = view)
                await view.wait()

                ObjectStaffUser = StaffUser(_user.id)
                points = await str_enter(interaction, "points")

                if points:

                    ResultEmbed = disnake.Embed(
                        color = 0x1b1b1b,
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                    ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)

                    if view.value == "add":
                        ObjectStaffUser.update_moderator_points(float(points.content))

                        ResultEmbed.title = "ВЫДАЧА БАЛЛОВ МОДЕРАТОРА"

                        if interaction.user.id == _user.id:
                            ResultEmbed.description = f"{interaction.user.mention}, вы успешно выдали себе **{points.content}** баллов модератора"
                        else:
                            ResultEmbed.description = f"{interaction.user.mention}, вы успешно выдали пользователю {_user.mention} ({_user.name}#{_user.discriminator}) **{points.content}** баллов модератора"

                    else:
                        if float(ObjectStaffUser.WeekModeratorPoints) - float(points.content) >= 0: 
                            ObjectStaffUser.update_moderator_points(float(points.content) * -1)

                            ResultEmbed.title = "СНЯТИЕ БАЛЛОВ МОДЕРАТОРА"

                            if interaction.user.id == _user.id:
                                ResultEmbed.description = f"{interaction.user.mention}, вы успешно сняли себе **{points.content}** баллов модератора"
                            else:
                                ResultEmbed.description = f"{interaction.user.mention}, вы успешно сняли пользователю {_user.mention} ({_user.name}#{_user.discriminator}) **{points.content}** баллов модератора"

                        else:
                            await points.delete()
                            return await interaction.edit_original_message(f"У пользователя нет такого количества баллов!", embed = None, view = None)

                    await points.delete()
                    await interaction.edit_original_message(embed = ResultEmbed, view = None)

                else:
                    await timeout_embed(interaction)

            
            elif view.value == "HelperPointsChange":

                view = AddOrRemoveChoice(interaction)
                await interaction.edit_original_message(view = view)
                await view.wait()

                ObjectStaffUser = StaffUser(_user.id)
                points = await str_enter(interaction, "points")

                if points:

                    ResultEmbed = disnake.Embed(
                        color = 0x1b1b1b,
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                    ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)

                    if view.value == "add":
                        ObjectStaffUser.update_helper_points(float(points.content))

                        ResultEmbed.title = "ВЫДАЧА БАЛЛОВ ХЕЛПЕРА"

                        if interaction.user.id == _user.id:
                            ResultEmbed.description = f"{interaction.user.mention}, вы успешно выдали себе **{points.content}** баллов хелпера"
                        else:
                            ResultEmbed.description = f"{interaction.user.mention}, вы успешно выдали пользователю {_user.mention} ({_user.name}#{_user.discriminator}) **{points.content}** баллов хелпера"

                    else:
                        if float(ObjectStaffUser.WeekHelperPoints) - float(points.content) >= 0: 
                            ObjectStaffUser.update_helper_points(float(points.content) * -1)

                            ResultEmbed.title = "СНЯТИЕ БАЛЛОВ ХЕЛПЕРА"

                            if interaction.user.id == _user.id:
                                ResultEmbed.description = f"{interaction.user.mention}, вы успешно сняли себе **{points.content}** баллов хелпера"
                            else:
                                ResultEmbed.description = f"{interaction.user.mention}, вы успешно сняли пользователю {_user.mention} ({_user.name}#{_user.discriminator}) **{points.content}** баллов хелпера"

                        else:
                            await points.delete()
                            return await interaction.edit_original_message(f"У пользователя нет такого количества баллов!", embed = None, view = None)

                    await points.delete()
                    await interaction.edit_original_message(embed = ResultEmbed, view = None)

                else:
                    await timeout_embed(interaction)


            elif view.value == "EventerPointsChange":

                view = AddOrRemoveChoice(interaction)
                await interaction.edit_original_message(view = view)
                await view.wait()

                ObjectStaffUser = StaffUser(_user.id)
                points = await str_enter(interaction, "points")

                if points:

                    ResultEmbed = disnake.Embed(
                        color = 0x1b1b1b,
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                    ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)

                    if view.value == "add":
                        ObjectStaffUser.update_eventer_points(float(points.content))

                        ResultEmbed.title = "ВЫДАЧА БАЛЛОВ ИВЕНТЕРА"

                        if interaction.user.id == _user.id:
                            ResultEmbed.description = f"{interaction.user.mention}, вы успешно выдали себе **{points.content}** баллов ивентера"
                        else:
                            ResultEmbed.description = f"{interaction.user.mention}, вы успешно выдали пользователю {_user.mention} ({_user.name}#{_user.discriminator}) **{points.content}** баллов ивентера"

                    else:
                        if float(ObjectStaffUser.WeekEventerPoints) - float(points.content) >= 0: 
                            ObjectStaffUser.update_eventer_points(float(points.content) * -1)

                            ResultEmbed.title = "СНЯТИЕ БАЛЛОВ ИВЕНТЕРА"

                            if interaction.user.id == _user.id:
                                ResultEmbed.description = f"{interaction.user.mention}, вы успешно сняли себе **{points.content}** баллов ивентера"
                            else:
                                ResultEmbed.description = f"{interaction.user.mention}, вы успешно сняли пользователю {_user.mention} ({_user.name}#{_user.discriminator}) **{points.content}** баллов ивентера"

                        else:
                            await points.delete()
                            return await interaction.edit_original_message(f"У пользователя нет такого количества баллов!", embed = None, view = None)

                    await points.delete()
                    await interaction.edit_original_message(embed = ResultEmbed, view = None)

                else:
                    await timeout_embed(interaction)


            elif view.value == "RoleChange":

                role_id = await str_enter(interaction, "role")

                if role_id:

                    role = get(guild.roles, id = int(role_id.content))
                    await role_id.delete()

                    ObjectInteraction = StaffUser(interaction.user.id)

                    ResultEmbed = disnake.Embed(
                        color = 0x292b2e,
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_thumbnail(interaction.user.avatar)
                    ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                
                    if role.id == config.ADMIN_ROLE_ID or role.id == config.DEVELOPER_ROLE_ID or (ObjectInteraction.admin == False and ObjectInteraction.developer == False and ObjectInteraction.curator == False and (role.id in config.STAFF_ROLES or role.id not in config.THEMATIC_ROLES)) or (ObjectInteraction.admin == False and ObjectInteraction.developer == False and role.id == config.CURATOR_ROLE_ID):
                            return await interaction.edit_original_message("Вы не можете выдать или снять данную роль!", embed = None, view = None)
                        
                    if role not in _user.roles:
                        await _user.add_roles(role)
                        ResultEmbed.title = "ВЫДАЧА РОЛИ"
                        ResultEmbed.description = f"{interaction.user.mention}, вы успешно выдали роль <@&{role.id}> пользователю {_user.mention} - {_user.name}#{_user.discriminator}"

                    else:
                        await _user.remove_roles(role)
                        ResultEmbed.title = "СНЯТИЕ РОЛИ"
                        ResultEmbed.description = f"{interaction.user.mention}, вы успешно сняли роль <@&{role.id}> пользователю {_user.mention} - {_user.name}#{_user.discriminator}"

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)     

                else:
                    await timeout_embed(interaction)


            elif view.value == "AddEventBan":

                EventBanRole = get(guild.roles, id = config.EVENT_BAN_ROLE_ID)

                if EventBanRole not in _user.roles:
                    await _user.add_roles(EventBanRole)
                    banLogChannel = self.bot.get_channel(config.BAN_LOG_CHANNEL_ID)

                    ResultEmbed = disnake.Embed(
                        title = "ИВЕНТ-БАН",
                        description = f"**Пользователь:** {_user.mention}\n" +
                                      f"**Ивентер:** {interaction.user.mention}",
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_thumbnail(_user.avatar)
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                    ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)
                    await direct_message(_user, "EventBan")
                    await banLogChannel.send(embed = ResultEmbed)
                    await generalLogChannel.send(embed = ResultEmbed)

                else:
                    ResultEmbed = disnake.Embed(
                        description = f"У пользователя {_user.mention} ({_user.name}#{_user.discriminator}) есть ивент-бан!",
                        color = 0x292b2e,
                    )

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)


            elif view.value == "RemoveEventBan":

                EventBanRole = get(guild.roles, id = config.EVENT_BAN_ROLE_ID)

                if EventBanRole in _user.roles:
                    await _user.remove_roles(EventBanRole)
                    banLogChannel = self.bot.get_channel(config.BAN_LOG_CHANNEL_ID)

                    ResultEmbed = disnake.Embed(
                        title = "СНЯТИЕ ИВЕНТ-БАНА",
                        description = f"**Пользователь:** {_user.mention}\n" +
                                      f"**Ивентер:** {interaction.user.mention}",
                        timestamp = datetime.datetime.now(),
                    )
                    ResultEmbed.set_thumbnail(_user.avatar)
                    ResultEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
                    ResultEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)
                    await banLogChannel.send(embed = ResultEmbed)
                    await generalLogChannel.send(embed = ResultEmbed)

                else:
                    ResultEmbed = disnake.Embed(
                        description = f"У пользователя {_user.mention} ({_user.name}#{_user.discriminator}) нет ивент-бана!",
                        color = 0x292b2e,
                    )

                    await interaction.edit_original_message(embed = ResultEmbed, view = None)


            elif view.value == "cancel":

                cancelEmbed = disnake.Embed(
                    description = "Выход из команды action!",
                    color = 0x292b2e,
                )

                await interaction.edit_original_message(embed = cancelEmbed, view = None)

    # перенести
    @commands.slash_command(description = "Посмотреть профиль.")
    async def profile(self, interaction: disnake.CommandInteraction, user: disnake.User = None):
        _user = interaction.user

        if user:
            _user = user
            
        ObjectUser = User(_user.id)
        CountOfWarns = 0
        for value in ObjectUser.warns:
            CountOfWarns += 1 
        
        profileEmbed = disnake.Embed(
            title = f"ПРОФИЛЬ - {_user.name}#{_user.discriminator}",
            description = f"**Баланс:** {ObjectUser.balance}\n" +
                          f"**Голосовой онлайн:** {ObjectUser.voice_time}\n" +
                          f"**Бан:** {ObjectUser.ban}\n" +  
                          f"**Варны:** {CountOfWarns}",
            color = 0x292b2e,
            timestamp = datetime.datetime.now(),
        )
        profileEmbed.set_thumbnail(_user.avatar)
        profileEmbed.set_footer(text = f"ID пользователя: {_user.id}", icon_url = _user.avatar)
        profileEmbed.set_image(url = "https://i.imgur.com/QzB7q9J.png")
        
        await interaction.response.send_message(embed = profileEmbed)


def setup(bot):
    bot.add_cog(Action(bot))