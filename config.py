import pathlib
import os
import logging
from logging.config import dictConfig
from    dotenv import load_dotenv

load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
CLUSTER = os.getenv("DISCORD_CLUSTER")
DATABASE = os.getenv("DISCORD_DATABASE_NAME")
COLLECTION = os.getenv("DISCORD_COLLECTION_NAME")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))

# STAFF ROLES ID
ADMIN_ROLE_ID = int(os.getenv("DISCORD_ADMINISTRATOR_ROLE_ID"))
DEVELOPER_ROLE_ID = int(os.getenv("DISCORD_DEVELOPER_ROLE_ID"))
CURATOR_ROLE_ID = int(os.getenv("DISCORD_CURATOR_ROLE_ID"))
MODERATOR_ROLE_ID = int(os.getenv("DISCORD_MODERATOR_ROLE_ID"))
HELPER_ROLE_ID = int(os.getenv("DISCORD_HELPER_ROLE_ID"))
EVENTER_ROLE_ID = int(os.getenv("DISCORD_EVENTER_ROLE_ID"))

# NECESSARY STATISTICS
MODERATOR_NECESSARY_STATISTICS = int(os.getenv("DISCORD_MODERATOR_NECESSARY_STATISTICS"))
HELPER_NECESSARY_STATISTICS = int(os.getenv("DISCORD_HELPER_NECESSARY_STATISTICS"))
EVENTER_NECESSARY_STATISTICS = int(os.getenv("DISCORD_EVENTER_NECESSARY_STATISTICS"))

# MODERATOR POINTS
MUTE_POINTS = float(os.getenv("DISCORD_MUTE_POINTS"))
WARN_POINTS = float(os.getenv("DISCORD_WARN_POINTS"))
BAN_POINTS = float(os.getenv("DISCORD_BAN_POINTS"))
REPORT_POINTS = float(os.getenv("DISCORD_REPORT_POINTS"))

# HELPER POINTS
GENDER_CHANGE_POINTS = float(os.getenv("DISCORD_GENDER_CHANGE_POINTS"))
NIGHT_ROLE_CHANGE_POINTS = float(os.getenv("DISCORD_NIGHT_ROLE_CHANGE_POINTS"))
TICKET_POINTS = float(os.getenv("DISCORD_TICKET_POINTS"))

# GENDER ROLES ID
MALE_ROLE_ID = int(os.getenv("DISCORD_MALE_ROLE_ID"))
FEMALE_ROLE_ID = int(os.getenv("DISCORD_FEMALE_ROLE_ID"))

# THEMATIC ROLES ID
NIGHT_ROLE_ID = int(os.getenv("DISCORD_NIGHT_ROLE_ID"))
ARTIST_ROLE_ID = int(os.getenv("DISCORD_ARTIST_ROLE_ID"))
#MUSICIANT_ROLE_ID = int(os.getenv("DISCORD_MUSICIANT_ROLE_ID"))

# PUNISHMENTS ROLES ID
MUTE_ROLE_ID = int(os.getenv("DISCORD_MUTE_ROLE_ID"))
BAN_ROLE_ID = int(os.getenv("DISCORD_BAN_ROLE_ID"))
EVENT_BAN_ROLE_ID = int(os.getenv("DISCORD_EVENT_BAN_ROLE_ID"))

# CHANNELS ID
GENERAL_LOG_CHANNEL_ID = int(os.getenv("DISCORD_GENERAL_LOG_CHANNEL_ID"))
MUTE_LOG_CHANNEL_ID = int(os.getenv("DISCORD_MUTE_LOG_CHANNEL_ID"))
WARN_LOG_CHANNEL_ID = int(os.getenv("DISCORD_WARN_LOG_CHANNEL_ID"))
BAN_LOG_CHANNEL_ID = int(os.getenv("DISCORD_BAN_LOG_CHANNEL_ID"))
REPORT_CHANNEL_ID = int(os.getenv("DISCORD_REPORT_CHANNEL_ID"))
TICKET_CHANNEL_ID = int(os.getenv("DISCORD_TICKET_CHANNEL_ID"))
RECRUITMENT_CHANNEL_ID = int(os.getenv("DISCORD_RECRUITMENT_CHANNEL_ID"))
TOURNAMENT_APPLICATION_CHANNEL_ID = int(os.getenv("DISCORD_TOURNAMENT_APPLICATION_CHANNEL_ID"))

# DIR
BASE_DIR = pathlib.Path(__file__).parent
COGS_DIR = BASE_DIR / "cogs"

# COG EXTENSIONS
EXTENSIONS = [
    'cogs.staff_commands.action',
    'cogs.staff_commands.HighStaffCommands',
    'cogs.staff_commands.StaffProfile',
    'cogs.staff_commands.StaffTop',
    'cogs.tournament.tournament_application_command',
    'cogs.CheckPermissions',
    'cogs.CogsControl',
    'cogs.DataBase',
    'cogs.ErrorHandling',
    'cogs.report',
    'cogs.TeamRecruitment',
    'cogs.ticket'
]

# STAFF ROLES LIST
STAFF_ROLES = [
    ADMIN_ROLE_ID,
    DEVELOPER_ROLE_ID,
    CURATOR_ROLE_ID,
    MODERATOR_ROLE_ID,
    HELPER_ROLE_ID,
    EVENTER_ROLE_ID
]

HIGHER_STAFF_ROLES = [
    ADMIN_ROLE_ID,
    DEVELOPER_ROLE_ID,
    CURATOR_ROLE_ID
]

# THEMATIC ROLES LIST
THEMATIC_ROLES = [
    NIGHT_ROLE_ID,
    ARTIST_ROLE_ID
#    MUSICIANT_ROLE_ID
]

LOGGING_CONFIG = {  
    "version": 1,   
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)