from discord.ext import commands
from embeds import get_embed
from discord.utils import get
import discord

class Group(commands.Cog, name="Dinamica de grupos"):

    def __init__(self,bot):
        self.bot = bot


    @commands.command(name="agrupar", rest_is_raw=True)
    @commands.has_any_role("Docente")
    async def grupos(self, ctx, *multiplo):
        students = get(ctx.guild.roles,name="Estudiante")
        print('hoola')

async def setup(bot):
    await bot.add_cog(Group(bot))