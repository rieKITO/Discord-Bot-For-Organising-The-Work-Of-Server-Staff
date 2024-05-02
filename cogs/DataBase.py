from pymongo import MongoClient
import disnake
from disnake.ext import commands
import datetime
from disnake.utils import get

import config

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = self.bot.get_guild(config.GUILD_ID)

    post = {
        "_id": None,
        "balance": 0,
        "voice_time": 0,
        "message_count": 0,
        "warns": [],
        "ban": False,
        "mute": False,
        "history_of_punishments": [],
        "history_of_nicknames": [],
        "transactions_history": []
    }

    StaffPost = {
        "_id": None,
        "admin": False,
        "developer": False,
        "curator": False,
        "moderator": False,
        "helper": False,
        "eventer": False,
        "StaffPoints": 0,
        "WeekModeratorPoints": 0,
        "WeekHelperPoints": 0,
        "WeekEventerPoints": 0,
        "history_of_reprimands": [],
    }

    cluster = MongoClient(config.CLUSTER)
    db = cluster[config.DATABASE]
    collection = db[config.COLLECTION]

    users = cluster.shp.nf_users
    staffUsers = cluster.shp.nf_StaffUsers

    @commands.command()
    @commands.has_role(config.DEVELOPER_ROLE_ID)
    async def update_data_base2(self, ctx):
        Data.users.delete_many({})
        Data.staffUsers.delete_many({})

    @commands.command()
    @commands.has_role(config.DEVELOPER_ROLE_ID)
    async def update_data_base(self, ctx):
        for member in self.guild.members:
            if Data.users.count_documents({"_id": member.id}) == 0:
                self.post["_id"] = member.id
                Data.users.insert_one(self.post)

            inStaff = False
            for role in member.roles:
                if role.id in config.STAFF_ROLES:
                    inStaff = True
                    break
            
            if inStaff:
                if Data.staffUsers.count_documents({"_id": member.id}) == 0:
                    self.StaffPost["_id"] = member.id
                    Data.staffUsers.insert_one(self.StaffPost)
                
                Data.staffUsers.update_one(
                        {
                            "_id": member.id
                        },
                        {
                            "$set": {
                                "admin": False,
                                "developer": False,
                                "curator": False,
                                "moderator": False,
                                "helper": False,
                                "eventer": False,
                            }
                        }
                    )
                    
                for role in member.roles:
                    if role.id == config.ADMIN_ROLE_ID:
                        Data.staffUsers.update_one({"_id": member.id},{"$set": {"admin": True}})
                    elif role.id == config.DEVELOPER_ROLE_ID:
                        Data.staffUsers.update_one({"_id": member.id},{"$set": {"developer": True}})
                    elif role.id == config.CURATOR_ROLE_ID:
                        Data.staffUsers.update_one({"_id": member.id},{"$set": {"curator": True}})
                    elif role.id == config.MODERATOR_ROLE_ID:
                        Data.staffUsers.update_one({"_id": member.id},{"$set": {"moderator": True}})
                    elif role.id == config.HELPER_ROLE_ID:
                        Data.staffUsers.update_one({"_id": member.id},{"$set": {"helper": True}})
                    elif role.id == config.EVENTER_ROLE_ID:
                        Data.staffUsers.update_one({"_id": member.id},{"$set": {"eventer": True}})

        ResultEmbed = disnake.Embed(
            description = "databases have been updated!",
            color = 0x292b2e,
            timestamp = datetime.datetime.now(),
        )

        await ctx.send(embed = ResultEmbed)	

    @commands.Cog.listener()
    async def on_connect(self):
        #for member in self.guild.members:
         #   if Data.users.count_documents({"_id": member.id}) == 0:
          #      self.post["_id"] = member.id
           #     Data.users.insert_one(self.post)

        #self.guild = self.bot.get_guild(config.GUILD_ID)
        #t1 = threading.Thread(target = self.check_users)
        #t1.start()
        ...
        
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if Data.users.count_documents({"_id": member.id}) == 0:
            self.post["_id"] = member.id
            Data.users.insert_one(self.post)

        else:

            user = Data.users.find_one(
                {
                    "_id": member.id,
                }
            )

            if user["ban"]:
                banRole = get(self.guild.roles, id = config.BAN_ROLE_ID)
                await member.add_roles(banRole)

            if user["mute"]:
                muteRole = get(self.guild.roles, id = config.MUTE_ROLE_ID)
                await member.add_roles(muteRole)

    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if len(before.roles) != len(after.roles):

            if len(before.roles) < len(after.roles):
                _role = next(role for role in after.roles if role not in before.roles)

                if _role.id in config.STAFF_ROLES:

                    if Data.staffUsers.count_documents({"_id": after.id}) == 0:
                        self.StaffPost["_id"] = after.id
                        Data.staffUsers.insert_one(self.StaffPost)

                    if _role.id == config.ADMIN_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"admin": True}})
                    elif _role.id == config.DEVELOPER_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"developer": True}})
                    elif _role.id == config.CURATOR_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"curator": True}})
                    elif _role.id == config.MODERATOR_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"moderator": True}})
                    elif _role.id == config.HELPER_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"helper": True}})
                    elif _role.id == config.EVENTER_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"eventer": True}})

            else:

                for role in before.roles:
                    if role not in after.roles:
                        _role = role
                        break

                if _role.id in config.STAFF_ROLES:
                    if _role.id == config.ADMIN_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"admin": False}})
                    elif _role.id == config.DEVELOPER_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"developer": False}})
                    elif _role.id == config.CURATOR_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"curator": False}})
                    elif _role.id == config.MODERATOR_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"moderator": False}})
                    elif _role.id == config.HELPER_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"helper": False}})
                    elif _role.id == config.EVENTER_ROLE_ID:
                        Data.staffUsers.update_one({"_id": after.id},{"$set": {"eventer": False}})

        elif before.nick != after.nick:
            _user = Data.users.find_one({"_id": before.id})
            Data.users.update_one(
                {
                    "_id": before.id
                },
                {
                    "$push":
                    {
                        "history_of_nicknames":
                        {
                            "number": len(_user["history_of_nicknames"]) + 1,
                            "nickname": str(before.nick),
                            "date": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        }
                    }
                }
            )



                    # Удаление пользователя из БД, если у него не осталось стафф ролей (работает)

#                    usr = Data.staffUsers.find_one(
#                        {
#                            "_id": after.id
#                        },
#                        {
#                            "admin": False,
#                            "developer": False,
#                            "curator": False,
#                            "moderator": False,
#                            "helper": False,
#                            "eventer": False,
#                        }
#                    )

#                    if usr:
#                        Data.staffUsers.delete_one({"_id": after.id})



      

def setup(bot):
    bot.add_cog(Data(bot))