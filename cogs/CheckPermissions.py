import disnake
from disnake.ext import commands

import config

staffRoles = [
    config.ADMIN_ROLE_ID,
    config.DEVELOPER_ROLE_ID,
    config.CURATOR_ROLE_ID,
    config.MODERATOR_ROLE_ID,
    config.HELPER_ROLE_ID,
    config.EVENTER_ROLE_ID
]

class CheckPermissions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def check_permissions_for_action():
        def predicate (interaction: disnake.Interaction): 
            for role in interaction.user.roles:
                if role.id in config.staffRoles:
                    return True
        return commands.check(predicate)
    
def setup(bot):
    bot.add_cog(CheckPermissions(bot))
