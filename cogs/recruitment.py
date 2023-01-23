from discord.ext import commands
from embeds import get_embed
from discord.utils import get
import discord

class Recruitment(commands.Cog, name="Recruitment"):

    def __init__(self,bot):
        self.bot = bot
        

    async def elegible(ctx):
        coach_role = get(ctx.guild.roles, name='Manager')
        return (ctx.author.top_role >= coach_role)

    @commands.command(name="interview", brief="Allows user access to Interview channels")
    
    @commands.has_any_role("Core", "Manager", "Coach")
    async def interview(self, ctx, *users: discord.Member):
        #logger.info(ctx)
        role = get(ctx.guild.roles, name='Applicant')
        interview_channel = get(ctx.guild.channels, name='interview-chat')
        for user in users:
            await user.add_roles(role)
            await user.send(f"Hello {user.mention}, you have been invited to join an AxieGlobal interview at this time. \nPlease join any of the available interview voice channels (Interview1, Interview2, Interview3)")
            await interview_channel.send(f"Hello {user.mention}, you have been invited to join an AxieGlobal interview at this time. \nPlease join any of the available interview voice channels (Interview1, Interview2, Interview3)")
            await ctx.send(f"Added Applicant role and sent a DM to {user.mention}")

    @commands.command(name='approve')
    
    @commands.has_any_role("Core", "Manager", "Master", "Coach")
    async def approve(self, ctx, *users: discord.Member):
        applicant_role = get(ctx.guild.roles, name='Applicant')
        Scholar_role = get(ctx.guild.roles, name='Scholar')
        waitlist_role = get(ctx.guild.roles, name='Waitlist')
        welcome_channel = get(ctx.guild.channels, name='welcome')
        waitlist_channel = get(ctx.guild.channels, name='waitlist')
        ex_role = get(ctx.guild.roles, name='ex')
        embed = get_embed("approve")
        for user in users:
            ex_role_user = get(user.roles, name="ex")
            if(ex_role == ex_role_user):
                await user.remove_roles(ex_role)
            await user.remove_roles(applicant_role)
            await user.add_roles(Scholar_role, waitlist_role)
            await user.send(f"Congratulations {user.mention}!", embed=embed)
            await welcome_channel.send(f"Congratulations and welcome to our newest member {user.mention} ! New members are now placed in the #waitlist channel")
            await ctx.send(f"Added Scholar, Probation and Waitlist roles and sent Accepted message DM to {user.mention}")

    @commands.command(name='reject')
    
    @commands.has_any_role("Core", "Manager", "Master", "Coach")
    async def reject(self, ctx, *users: discord.Member):
        applicant_role = get(ctx.guild.roles, name='Applicant')
        interviewed_role = get(ctx.guild.roles, name='Interviewed')
        for user in users:
            await user.remove_roles(applicant_role)
            await user.add_roles(interviewed_role)
            await user.send(f"Hello {user.mention}, thank you for your application and for interviewing with us. \nUnfortunately, after careful review, we are unable to progress your application for scholarship at this time. \nWe wish you the best in your Axie Infinity journey and hope to be able to take you for a scholarship in the future. Please follow via Discord or Twitter for future recruitment rounds.")
            await ctx.send(f"Removed Applicant role, Added Interviewed role and sent a rejection DM to {user.mention}")

    @commands.command(name='probation-pass')
    
    @commands.has_any_role("Core", "Manager", "Master", "Coach")
    async def probation(self, ctx, *users: discord.Member):
        probation_role = get(ctx.guild.roles, name='Probation')
        for user in users:
            await user.remove_roles(probation_role)
            embed = get_embed("probation_pass")
            await user.send(f"Hi {user.mention}",embed=embed)
            await ctx.send(f"Sent Probation Pass DM to all supplied {user.mention}")

    @commands.command(name="notice")
    
    @commands.has_any_role("Core", "Manager","Coach")
    async def notice(self, ctx, *users: discord.Member):
        for user in users:
            embed = get_embed("notice")
            await user.send(f"Hi {user.mention}", embed=embed)
            await ctx.send(f"Head's up sent to {user.mention}")
    
    @commands.command(name="alert")
    
    @commands.has_any_role("Core", "Manager","Coach")
    async def alert(self, ctx, *users: discord.Member):
        for user in users:
            embed = get_embed("alert")
            await user.send(f"Hi {user.mention}", embed=embed)
            await ctx.send(f"Alert sent to {user.mention}")
    
    @commands.command(name="warning")
    
    @commands.has_any_role("Core", "Manager","Coach")
    async def warning(self, ctx, *users: discord.Member):
        for user in users:
            embed = get_embed("warning")
            await user.send(f"Hi {user.mention}", embed=embed)
            await ctx.send(f"Warning sent to {user.mention}")

    @commands.command(name='onboard')
    
    @commands.has_any_role("Core", "Manager", "Master", "Coach")
    async def onboard(self, ctx, *users: discord.Member):
        for user in users:
            embed = get_embed("onboard")
            waitlist_role = get(ctx.guild.roles, name='Waitlist')
            probation_role = get(ctx.guild.roles, name='Probation')
            await user.remove_roles(waitlist_role)
            await user.add_roles(probation_role)
            await user.send(f"Hi {user.mention}",embed=embed)
            await ctx.send(f"Removed Waitlist role and sent onboarding message DM to {user.mention}")

    @commands.command(name='terminate')
    
    @commands.has_any_role("Core", "Manager", "Master", "Coach")
    async def terminate(self, ctx, *users: discord.Member):
        for user in users:
            embed = get_embed("terminate")
            Scholar_role = get(ctx.guild.roles, name='Scholar')
            Scholar_role_user = get(user.roles, name="Scholar")
            if Scholar_role == Scholar_role_user: await user.remove_roles(Scholar_role)
            waitlist_role = get(ctx.guild.roles, name='Waitlist')
            waitlist_role_user = get(user.roles, name="Waitlist")
            if waitlist_role == waitlist_role_user: await user.remove_roles(waitlist_role)
            probation_role = get(ctx.guild.roles, name='Probation')
            probation_role_user = get(user.roles, name="Probation")
            if probation_role == probation_role_user: await user.remove_roles(probation_role)
            ex_role = get(ctx.guild.roles, name='ex')
            await user.add_roles(ex_role)
            await user.send(f"Hi {user.mention}",embed=embed)
            await ctx.send(f"Removed Scholar role, added ex role and sent termination message DM to {user.mention}")

async def setup(bot):
	await bot.add_cog(Recruitment(bot))