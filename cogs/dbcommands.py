from discord.ext import commands
from embeds import get_embed
from discord.utils import get
import discord
from firebase import saveStudent, deleteStudent, identifyStudent

class DBcommands(commands.Cog, name="Wallets register"):

    def __init__(self,bot):
        self.bot = bot


    @commands.command(name="registrar", rest_is_raw=True)
    @commands.has_any_role("Docente")
    async def registrar(self, ctx, *cedula):
        # firebase only allows lists, can't store the list with Role's object
        # Json.dumps(ctx.author.roles) won't solve it

        name = ctx.author.name
        id= ctx.author.id
        guild = ctx.guild.id
         # simple request to an endpoint to validate cedula ONLY ETH MAINNET
        for i in cedula:
            if len(i)<7:
                await ctx.send(f'{ctx.author.mention} La cedula # {i} es demasiado corta, verifique de nuevo')
            else:
                res = await saveStudent(i,guild)
                if(res):
                    embed = get_embed("added")
                    embed.add_field(name='cedula', value=f'`{i}`', inline=False)
                    await ctx.send(f'{ctx.author.mention}', embed=embed )
                else: 
                    embed = get_embed("duplicated")
                    embed.add_field(name='cedula', value=f'`{i}`', inline=False)
                    await ctx.send(f'{ctx.author.mention} La cedula # {i} esta duplicada', embed=embed )
    
    @commands.command(name="borrar", rest_is_raw=True)
    @commands.has_any_role("Docente")
    async def borrar(self, ctx, *cedula):
            guild = ctx.guild.id
            res = await deleteStudent(cedula[0],guild)
            await ctx.send(f'{ctx.author.mention} Su estudiante cedula '+cedula[0]+' ha sido eliminado') if res else await ctx.send(f'{ctx.author.mention} La cedula # {cedula[0]} no se encuentra en la base de datos')

    @commands.command(name="identificar", rest_is_raw=True)
    async def borrar(self, ctx, *datos):
            guild = ctx.guild.id
            res = await identifyStudent(datos[0], datos, guild)
            await ctx.send(f'{ctx.author.mention} Usted cedula # {datos[0]} ha sido identificado como {datos[1:len(datos)]}') if res else await ctx.send(f'{ctx.author.mention} La cedula # {datos[0]} no se encuentra en la base de datos')
            
async def setup(bot):
	await bot.add_cog(DBcommands(bot))