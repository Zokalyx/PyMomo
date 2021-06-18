import discord as ds


def custom_command_prefix(bot, message):
    """Dinamically determines which prefix to use for commands
    based on the guild"""
    config = bot.db.data["config"]
    # Try using the guild prefix
    try:
        return config["prefixes"][str(message.guild.id)]
    # Otherwise just use the default prefix
    except KeyError:
        return config["default-prefix"]


"""Helper functions and objects for initializing momo"""
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
