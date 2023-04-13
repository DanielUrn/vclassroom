import json
from discord.ext import commands
from embeds import get_embed
from discord.utils import get
import discord
from firebase import saveTema, deleteTema, saveGrupo, deleteGrupo, appendEstudiante, popEstudiante, listTemas

class Group(commands.Cog, name="Dinamica de grupos"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="temas", rest_is_raw=True)
    @commands.has_any_role("Estudiante","Docente")
    async def temas(self, ctx:commands.Context):
        guild = ctx.guild.id
        temas = await listTemas(guild)
        if(temas):
            embed = get_embed('lista')
            for i, tema in enumerate(temas):
                content = tema
                embed.add_field(name='Tema ', value=(i+1), inline=True)
                embed.add_field(name='Nombre', value=content["tema"], inline=True)
                if("grupos" in content):
                    for grupo in content["grupos"]:
                        embed.add_field(name=f'Grupo '+str(grupo["#"]) , value=grupo, inline=False)
            await ctx.send(f'{ctx.author.mention}', embed=embed )
        else:
            await ctx.send('Ha ocurrido un error con la de los temas, para más información prueba !help temas')

    @commands.command(name="creartema", rest_is_raw=True)
    @commands.has_any_role("Docente")
    async def crearTema(self, ctx:commands.Context, *data):
        guild = ctx.guild.id
        if(data and data != ''):
            success = await saveTema(data,guild)
            if(success):
                await ctx.send(f'El tema '+ ' '.join(data) + ' ha sido exitosamente guardado en la base de datos')
            else:
                await ctx.send('Ha ocurrido un error con la creación del tema, probablemente debido a la base de datos')
        else:
            await ctx.send('Ha ocurrido un error con la creación del tema, por favor verifica que proporcionaste un nombre para tu tema luego del comando, para más información prueba !help creartema')
    
    @commands.command(name="borrartema", rest_is_raw=True)
    @commands.has_any_role("Docente")
    async def borrarTema(self, ctx:commands.Context, data):
        guild = ctx.guild.id
        if(data and data.isnumeric()):
            success = await deleteTema(data,guild)
            if(success):
                await ctx.send('El tema '+ ' '.join(data) + ' ha sido exitosamente borrado de la base de datos')
            else:
                await ctx.send('Ha ocurrido un error con la eliminacion del tema, probablemente debido a la base de datos')
        else:
            await ctx.send('Ha ocurrido un error con la eliminación del tema, por favor verifica que proporcionaste el numero de tema a borrar luego del comando, para más información prueba !help borrartema')

    @commands.command(name="creargrupo", rest_is_raw=True)
    @commands.has_any_role("Estudiante")
    async def crearGrupo(self, ctx: commands.Context, *data):
        guild = ctx.guild.id
        if(data):
            success = await saveGrupo(ctx.author.id,*data[0],guild)
            if(success):
                await ctx.send('El grupo '+ ' '.join(data) + ' ha sido exitosamente creado en la base de datos')
            else:
                await ctx.send('Ha ocurrido un error con la creación del grupo, probablemente debido a la base de datos')
        else:
            await ctx.send('Ha ocurrido un error con la creación del grupo, para más información prueba !help creargrupo')

    @commands.command(name="borrargrupo", rest_is_raw=True)
    @commands.has_any_role("Estudiante", "Docente")
    async def borrarGrupo(self, ctx: commands.Context, *data):
        guild = ctx.guild.id
        if(len(data)==2):
            success = await deleteGrupo(data[0],data[1],guild)
            if(success):
                await ctx.send('El grupo '+ ' '.join(data) + ' ha sido exitosamente borrado de la base de datos')
            else:
                await ctx.send('Ha ocurrido un error con la eliminación del grupo, probablemente debido a la base de datos')
        else:
            await ctx.send('Ha ocurrido un error con la eliminación del grupo, quizá te faltan o te sobran argumentos, recuerda que son un par de números separados por un espacio, para más información prueba !help borrargrupo')
    
    @commands.command(name="entrargrupo", rest_is_raw=True)
    @commands.has_any_role("Estudiante")
    async def entrarGrupo(self, ctx: commands.Context, *data):
        guild = ctx.guild.id
        if(len(data)==2):
            success = await appendEstudiante(ctx.author.id,data[0],data[1],guild)
            if(success):
                await ctx.send('Haz sido añadido existosamente al grupo '+ ' '.join(data[0]) + ' ha sido exitosamente creado en la base de datos')
            else:
                await ctx.send('Ha ocurrido un error con la integración al grupo, probablemente debido a la base de datos')
        else:
            await ctx.send('Ha ocurrido un error con la integración del grupo, para más información prueba !help entrargrupo')

    @commands.command(name="salirgrupo", rest_is_raw=True)
    @commands.has_any_role("Estudiante")
    async def salirGrupo(self, ctx: commands.Context, *data):
        guild = ctx.guild.id
        if(len(data)==2):
            success = await popEstudiante(ctx.author.id,data[0],data[1],guild)
            if(success):
                await ctx.send('Haz sido eliminado existosamente al grupo '+ ' '.join(data[0]))
            else:
                await ctx.send('Ha ocurrido un error con la salida del grupo, probablemente debido a la base de datos')
        else:
            await ctx.send('Ha ocurrido un error con la salida del grupo, para más información prueba !help salirgrupo')


async def setup(bot):
    await bot.add_cog(Group(bot))
