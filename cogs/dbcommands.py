from discord.ext import commands
from embeds import get_embed
from discord.utils import get
import discord
from firebase import saveStudent, deleteStudent, identifyStudent

class DBcommands(commands.Cog, name="Registrar estudiantes"):

    def __init__(self,bot):
        self.bot = bot


    @commands.command(name="registrar", rest_is_raw=True)
    @commands.has_any_role("Docente")
    async def registrar(self, ctx, *cedulas):
        guild = ctx.guild.id
        for cedula in cedulas:
            if len(cedula)<7:
                await ctx.send(f'{ctx.author.mention} La cedula # {cedula} es demasiado corta, verifique de nuevo')
            else:
                res = await saveStudent(cedula,guild)
                if(res):
                    embed = get_embed("anadido")
                    embed.add_field(name='cedula', value=f'`{cedula}`', inline=False)
                    await ctx.send(f'{ctx.author.mention}', embed=embed )
                else: 
                    embed = get_embed("duplicado")
                    embed.add_field(name='cedula', value=f'`{cedula}`', inline=False)
                    await ctx.send(f'{ctx.author.mention} La cedula # {cedula} esta duplicada', embed=embed )
    
    @commands.command(name="borrar", rest_is_raw=True)
    @commands.has_any_role("Docente")
    async def borrar(self, ctx, *cedula):
            guild = ctx.guild.id
            res = await deleteStudent(cedula[0],guild)
            print(res)
            if (res):
                await ctx.send(f'{ctx.author.mention} Su estudiante cedula '+cedula[0]+' ha sido eliminado') 
            else:
                await ctx.send(f'{ctx.author.mention} La cedula # {cedula[0]} no se encuentra en la base de datos')

    @commands.command(name="identificar", rest_is_raw=True)
    @commands.has_permissions(change_nickname=True)
    async def identificar(self, ctx: commands.Context, *datos):
            guild = ctx.guild.id
            id = ctx.author.id
            students = get(ctx.guild.roles,name="Estudiante")
            res = await identifyStudent(datos[0], datos,id, guild)
            if(res):
                await ctx.send(f'{ctx.author.mention} Usted cedula # {datos[0]} ha sido identificado como {datos[1:len(datos)]}')
                await ctx.author.edit(nick = str(' '.join(datos[1:len(datos)]))) 
                await ctx.author.add_roles(students)
            else:
                await ctx.send(f'{ctx.author.mention} La cedula # {datos[0]} no se encuentra en la base de datos')
            
        
async def setup(bot):
	await bot.add_cog(DBcommands(bot))