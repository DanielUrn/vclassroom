from discord.ext import commands
from embeds import get_embed
from discord.utils import get
import discord

class Coaches(commands.Cog, name="Coaches squads"):

    def __init__(self,bot):
        self.bot = bot

    async def elegible(ctx):
        coach_role = get(ctx.guild.roles, name='Manager')
        return (ctx.author.top_role >= coach_role)
    

    @commands.command(name='approve-coach')
    @commands.check(elegible)
    @commands.has_any_role("Core", "Manager", "Master")
    async def approve(self, ctx, interviewee: discord.Member):
        coach_role = get(ctx.guild.roles, name='Coach')
        welcome_channel = get(ctx.guild.channels, name='coaches-chat')
        #await interviewee.add_roles(coach_role)
        await interviewee.send(f"Congratulations {interviewee.mention}! You have been accepted as a Coach in AxieGlobal! Please see the #coaches-chat channel and the Coach Terms and Conditions here: https://drive.google.com/file/d/1iYT0au4aSQWT4vtzwQwO0i7XPWue7mJh/view?usp=sharing")
        await ctx.send(f"Added Coach role and sent a DM to {interviewee.mention}")

    @commands.command(name='assign-squad')
    @commands.check(elegible)
    @commands.has_any_role("Core", "Manager", "Master")
    async def assign(self, ctx, user: discord.Member, role: discord.Role):
        embed = get_embed("assign-squad")
        await user.add_roles(role)
        await user.send(f"Hi {user.mention}",embed=embed)
        await ctx.send(f"Added {role.mention} and sent a DM to {user.mention}")

async def setup(bot):
	await bot.add_cog(Coaches(bot)) 