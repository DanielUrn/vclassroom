import os
import discord
from discord.ext.commands import Bot
from discord.utils import get
from embeds import get_embed
from config import read_config

token = read_config('bot_token')
server_name = read_config('discord_server')
bot_command_channel = read_config('bot_command_channel')

def isDocente(member, guilds):
    for guild in guilds:
        if(member.guild.id == guild.id):
            for role in member.guild.roles:
                if str(role) == "Docente":
                    return True
            return False
        return False

class AdminBot(Bot):
    def __init__(self, **kwargs):
        super(AdminBot, self).__init__(**kwargs)
        self.adminbot_status = True

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        guild = self.guilds[0]
        print(
            f'{self.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        for filename in os.listdir('./cogs'):
          if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

          else:
            print(f'Unable to load {filename[:-3]}')

    async def on_member_join(self, user: discord.User):
        embed = get_embed("welcome")
        await user.send(embed=embed)

    async def on_message(self,message):
        await bot.process_commands(message)

    async def on_command(self, ctx):
        context = {'author': ctx.author.name, 'channel': ctx.channel.name, 'command': ctx.command.name, 'status': 'invoked'}

    async def on_command_error(self, ctx, error):
        context = {'author': ctx.author.name, 'channel': ctx.channel.name, 'command': ctx.command.name, 'status': str(error)}
        await ctx.send(f"An error occured: {str(error)}")

    async def on_command_completion(self, ctx):
        context = {'author': ctx.author.name, 'channel': ctx.channel.name, 'command': ctx.command.name, 'status': 'success'}
    
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guilds = self.guilds
        channel = await self.fetch_channel(bot_command_channel)
        isDocente = isDocente(member,guilds)
        print(isDocente)
        



# Bot setup
intents = discord.Intents.all()
bot = AdminBot(command_prefix='!', intents=intents)


bot.run(token)