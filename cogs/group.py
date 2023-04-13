from discord.ext import commands
from embeds import get_embed
from discord.utils import get
import discord


class Group(commands.Cog, name="Dinamica de grupos"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="grupos", rest_is_raw=True)
    @commands.has_any_role("Docente")
    async def grupos(self, ctx, *data):
        students: discord.Role = get(ctx.guild.roles, name="Estudiante")
        studentsNumber = len(students.members)
        last = len(data)-1
        subject = {
            'name': ''
        }
        grupos = {
            'groupsNumber': 0,
            'groups': []
        }
        if (data):
            if (data[last].isnumeric()):
                div = int(data[last])
                if (div >= len(students.members)):
                    await ctx.send('Haz solicitado crear grupos de ' + div + ' personas pero en el servidor solo se encuentran ' + studentsNumber + 'usuarios con el rol de estudiantes, asegurese de que todos se hayan identificado apropiadamente')
                else:
                    subjectName = data[slice(0, last-1)]
                    subject['name'] = subjectName
                    print(data)
                    grupo = {
                        'n': 0,
                        'students': []
                    }
                    for student in students.members:
                        if (grupo['n'] < div):
                            grupo['n'] += 1
                            grupo['students'].append({
                                'id': student.id,
                                'name': student.display_name
                            })
                            if (grupo['n'] >= div):
                                print(grupo)
                                grupos['groups'].append(grupo)
                                grupo['n'] = 0
                                grupo['students'] = []
                                grupos['groupsNumber'] += 1
                    print(grupos)
            else:
                print('los estudiantes crearan sus grupos')
        else:
            await ctx.send('Necesita introducir argumentos a su comando. Para más información, escriba !help grupos')


async def setup(bot):
    await bot.add_cog(Group(bot))
