from cogs.DataBase import Data

class User(Data):
    def __init__(self, id):
        self.row = Data.users.find_one({"_id": id})
        self.id = self.row["_id"]
        self.balance = self.row["balance"]
        self.voice_time = self.row["voice_time"]
        self.warns = self.row["warns"]
        self.ban = self.row["ban"]
        self.mute = self.row["mute"]
        self.HistoryOfPunishments = self.row["history_of_punishments"]
        self.HistoryOfNicknames = self.row["history_of_nicknames"]

    def update_balance(self, amount):
        Data.users.update_one({"_id": self.id}, {"$inc": {"balance": amount}})
        return self.__init__(self.id)
    
    def set_mute_field(self, choice: bool):
        Data.users.update_one({"_id": self.id}, {"$set": {"mute": choice}})
        return self.__init__(self.id)
    
    def push_warn(self, date: str):
        Data.users.update_one({"_id": self.id}, {"$push": {"warns": {"date": date}}})
        return self.__init__(self.id)

    def pull_warn(self, date: str):
        usr = User.users.find_one({"_id": self.id})
        for value in usr["warns"]:
            if value['date'] == date: 
                Data.users.update_one({"_id": self.id}, {"$pull": {"warns": {"date": date}}})
                return True
        return False
    
    def set_ban_field(self, choice: bool, moderatorID: int = None, reason: str = None, date: str = None):
        if choice == True:
            Data.users.update_one(
                {
                    "_id": self.id
                },
                {
                    "$set":
                    {
                        "ban":
                        {
                            "moderator": moderatorID,
                            "reason": reason,
                            "date": date
                        }
                    }
                }
            )
        else:
            Data.users.update_one({"_id": self.id}, {"$set": {"ban": choice}})
        return self.__init__(self.id)
    
    def interaction_with_the_history_of_punishments(self, choice: str, number: int, type: str = None, moderatorID: int = None, reason: str = None, date: str = None):
        if choice == "push":
            Data.users.update_one(
                {
                    "_id": self.id
                },
                {
                    "$push":
                    {
                        "history_of_punishments":
                        {
                            "number": number,
                            "type": type,
                            "moderator_id": moderatorID,
                            "reason": reason,
                            "date": date
                        }
                    }
                }
            )

        elif choice == "pull":
            Data.users.update_one(
                {
                    "_id": self.id
                },
                {
                    "$pull":
                    {
                        "history_of_punishments":
                        {
                            "number": number
                        }
                    }
                }
            )

            _user = Data.users.find_one({"_id": self.id})
            array = _user['history_of_punishments']
            i = 0
            for punishment in array:
                array[i]['number'] = i + 1
                i += 1

            Data.users.update_one({"_id": self.id}, {"$set": {"history_of_punishments": array}})
                
        return self.__init__(self.id)
    
class StaffUser(Data):
    def __init__(self, id):
        self.row = Data.staffUsers.find_one({"_id": id})
        self.id = self.row["_id"]
        self.admin = self.row["admin"]
        self.developer = self.row["developer"]
        self.curator = self.row["curator"]
        self.moderator = self.row["moderator"]
        self.helper = self.row["helper"]
        self.eventer = self.row["eventer"]
        self.StaffPoints = self.row["StaffPoints"]
        self.WeekModeratorPoints = self.row["WeekModeratorPoints"]
        self.WeekHelperPoints = self.row["WeekHelperPoints"]
        self.WeekEventerPoints = self.row["WeekEventerPoints"]
        self.HistoryOfReprimands = self.row["history_of_reprimands"]

    def update_staff_points(self, points: float):
        Data.staffUsers.update_one({"_id": self.id}, {"$inc": {"StaffPoints": points}})
        return self.__init__(self.id)
    
    def update_moderator_points(self, points: float):
        Data.staffUsers.update_one({"_id": self.id}, {"$inc": {"WeekModeratorPoints": points}})
        return self.__init__(self.id)
    
    def update_helper_points(self, points: float):
        Data.staffUsers.update_one({"_id": self.id}, {"$inc": {"WeekHelperPoints": points}})
        return self.__init__(self.id)
    
    def update_eventer_points(self, points: float):
        Data.staffUsers.update_one({"_id": self.id}, {"$inc": {"WeekEventerPoints": points}})
        return self.__init__(self.id)

    def update_week_moderator_points(self, points: float):
        Data.staffUsers.update_one({"_id": self.id}, {"$inc": {"WeekModeratorPoints": points}})
        return self.__init__(self.id)

    def update_week_helper_points(self, points: float):
        Data.staffUsers.update_one({"_id": self.id}, {"$inc": {"WeekHelperPoints": points}})
        return self.__init__(self.id)
    
    def update_week_eventer_points(self, points: float):
        Data.staffUsers.update_one({"_id": self.id}, {"$inc": {"WeekEventerPoints": points}})
        return self.__init__(self.id)
    
    def interaction_with_the_history_of_reprimands(self, choice: str, number: int, curatorID: int = None, reason: str = None, date: str = None):
        if choice == "push":
            Data.staffUsers.update_one(
                {
                    "_id": self.id
                },
                {
                    "$push":
                    {
                        "history_of_reprimands":
                        {
                            "number": number,
                            "curator_id": curatorID,
                            "reason": reason,
                            "date": date
                        }
                    }
                }
            )

        elif choice == "pull":
            Data.staffUsers.update_one(
                {
                    "_id": self.id
                },
                {
                    "$pull":
                    {
                        "history_of_reprimands":
                        {
                            "number": number
                        }
                    }
                }
            )

            _user = Data.staffUsers.find_one({"_id": self.id})
            array = _user['history_of_reprimands']
            i = 0
            for reprimand in array:
                array[i]['number'] = i + 1
                i += 1

            Data.staffUsers.update_one({"_id": self.id}, {"$set": {"history_of_reprimands": array}})
                
        return self.__init__(self.id)

