"""Helper functions and objects for initializing momo"""
import discord as ds

def custom_command_prefix(bot, message):
    config = bot.db.data["config"]
    try:
        return config["prefixes"][str(message.guild.id)]
    except KeyError:
        return config["default-prefix"]


init_dict = {
    "owner_id": 284696251566391296,
    "command_prefix": custom_command_prefix,
    "help_command": None,
    "activity": ds.Activity(
            name="sugerencias",
            type=ds.ActivityType.listening
        ),
    "case_insensitive": True,
}
