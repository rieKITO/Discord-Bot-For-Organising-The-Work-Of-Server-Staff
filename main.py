import disnake
from disnake.ext import commands

import config

logger = config.logging.getLogger("bot")

class MaikiBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: disnake.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)
    
    async def on_ready(self):
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        for cogFile in config.EXTENSIONS:
            self.load_extension(cogFile)


if __name__ == "__main__":
    intents = disnake.Intents.default()
    intents.message_content = True
    intents.members = True
    command_sync_flags = commands.CommandSyncFlags.default()
    command_sync_flags.sync_commands_debug = True

    bot = MaikiBot( 
        command_prefix = "!",
        help_command = None,
        intents = intents,
        test_guilds = [config.GUILD_ID],
        command_sync_flags = command_sync_flags
    )

    bot.run(config.DISCORD_API_SECRET)