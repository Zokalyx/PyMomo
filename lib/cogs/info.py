from discord.ext.commands import Cog, command
from typing import Union


class MomoInfo(Cog):
    """Comandos relacionados a información y ayuda"""

    def __init__(self, bot):
        self.bot = bot
        self.name = "info"
        self.aliases = ["info"]

    def cog_of(self, word) -> Union[Cog, None]:
        """Returns the cog that includes the command or None if the word
        is not part of any cog"""
        cogs = self.bot.cogs
        for cog in cogs:
            if word in cogs[cog].aliases:
                return cogs[cog]
        return None

    def specific_command_help(self, command) -> None:
        """Returns the formatted text corresponding to the information
        of a specific command"""
        return (
            f"`{command.name}`: {command.help}\n" +
            (f"Uso: `{command.name} {command.usage}`\n"
                if command.usage else "") +
            (f"Nombres alternativos: " +
                ", ".join([f"`{a}`" for a in command.aliases])
                if command.aliases else "")
        )

    def category_help(self, cog) -> None:
        """Returns the formatted text corresponding to the information
        of a category of commands, grouped by cog"""
        title = f"__{cog.description}__\n"
        content = ""
        for cmd in cog.get_commands():
            content += (
                f"`{cmd.name}" +
                (f" {cmd.usage}`" if cmd.usage else "`") +
                f": {cmd.help}\n"
            )
        return title + content

    def general_help(self, guild_id) -> None:
        """Returns the formatted text corresponding to general information
        and help about Momo"""
        cfg = self.bot.config
        title = "__Información y ayuda__\n"
        prefix = "El prefijo para comandos es" +\
            f" `{cfg['prefixes'].get(str(guild_id), cfg['default-prefix'])}`\n"
        content = ""
        cogs = self.bot.cogs
        for cog in cogs:
            content += f"`help {cogs[cog].name}`: {cogs[cog].description}\n"
        return title + prefix + content

#-------------------------------COMMANDS--------------------------------------

    @command(usage="(<categoría>) o (<comando>)", aliases=["h"])
    async def help(self, ctx, command_or_category=None) -> None:
        """muestra ayuda sobre el bot y sus comandos"""
        # The command was passed with an argument
        if command_or_category is not None:
            help_category = self.cog_of(command_or_category)
            # Argument is a category name
            if help_category is not None:
                await ctx.send(self.category_help(help_category))
            # Argument is not a category name
            else:
                command = self.bot.get_command(command_or_category)
                # Argument is a command
                if command is not None:
                    await ctx.send(self.specific_command_help(command))
                # Argument is not a command
                else:
                    await ctx.send(
                        f"No existe el comando `{command_or_category}`"
                    )
        # The command was passed by itself
        else:
            await ctx.send(self.general_help(ctx.guild.id))
