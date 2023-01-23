from unicodedata import name
from discord.ext import commands
from embeds import get_embed, get_content
from discord.utils import get
import discord

class CustomHelp(commands.HelpCommand):
    # signature
    # if there were subcommands, get em' all
    # also works for a single command
    def get_command_signature(self, command):
        param=''
        for params in command.clean_params.items():
            param+=params[0]
    
        if param != '':
            return '`{0.context.clean_prefix}{1.qualified_name} ({2})`\n'.format(self, command,param)
        else:
            return '`{0.context.clean_prefix}{1.qualified_name}`\n'.format(self, command)

    def get_command_help(self, command):
        return '`{0.context.clean_prefix}{1.qualified_name} {1.signature}`'.format(self, command)

    # !help
    async def send_bot_help(self, mapping):
        ctx = self.context
        embed = get_embed("help")
        for cog, command in mapping.items():
            filtered = await self.filter_commands(command)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                if cog_name!="No Category":
                    embed.add_field(name=cog_name, value="".join(command_signatures))
        
        await ctx.send(embed=embed)

    # !help <command>
    async def send_command_help(self, command):
        ctx = self.context
        content = command.qualified_name
        help = get_embed("help")
        filter = await self.filter_commands([command], sort=True)
        if filter:
            name = command.qualified_name
            command_embed = self.get_command_signature(filter[0])
            help.add_field(name=name, value="".join(command_embed), inline=True)
            help.add_field(name='How to use: ', value=get_content(content), inline=False)
            await ctx.send(embed=help)
        else:
            raise commands.BadArgument("You probably don't have the Role to execute this command nor to get help of it")

            #help.add_field(name="Error", value="You do not have access to this command")
            #await ctx.send(embed=help)
        
        
    # !help <group>
    async def send_group_help(self, group):
        await self.context.send("Theres no subcommands for the moment")
    
    # !help <cog>
    async def send_cog_help(self, cog):
        await self.context.send("This is help cog")


class Help(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        help_command = CustomHelp()
        help_command.cog = self
        help_command.verify_checks=True
        bot.help_command = help_command


async def setup(bot):
	await bot.add_cog(Help(bot))