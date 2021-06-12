"""Helper functions and objects for initializing momo"""

def custom_command_prefix(bot, message):
    config = bot.data["config"]
    try:
        return config["prefixes"][str(message.guild.id)]
    except KeyError:
        return config["default-prefixes"]

init_dict = {
    "command_prefix": custom_command_prefix
}
