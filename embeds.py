from discord import Embed, Colour


def get_embed(type):
    embed = Embed(title='Virtual Classroom',
                  colour=Colour.from_rgb(3, 178, 248))
    embed.set_author(name='Virtual Classroom', url='https://www.urbe.edu/',
                     icon_url='https://www.urbe.edu/images/logos/logo-urbe1.jpg')
    if type == "help":
        embed.add_field(name="Ayuda Virtual Classroom",
                        value="Para más información acerca de un `Comando` escribe: **!help (comando)**\n Para más información sobre una `Categoria` escribe **!help (categoría)**", inline=False)
    else:
        embed.add_field(name='Mensaje automático - No responder',
                        value=get_content(type), inline=False)

    return embed


def get_content(type):
    content = ""
    if type == "bienvenida":
        content = """Bienvenido a Virtual Classroom
        Este es un proyecto de tésis diseñado como alternativa a un salón de clases virtual a través de Discord"""

    elif type == "identificar":
        content = """
            ***!identificar (cedula) (nombre y apellido)***
            Insertar datos sin parentesis, con un solo espacio entre datos
            
            Puede volver a ejecutar el comando si cometió un error para actualizar su nombre de nuevo
        """
    elif type == "anadido":
        content = """
            La cedula fue exitosamente añadida
        """
    elif type == "registrar":
        content = """
            ***!registrar (cedula)***
            Insertar datos sin parentesis, con un solo espacio entre datos
            Puede registrar varias cedulas al mismo tiempo
        """
    elif type == "borrar":
        content = """
           ***!borrar (cedula)***
           Insertar datos sin parentesis, con un solo espacio entre datos
           Puede borrar varias cedulas al mismo tiempo
           Los estudiantes que sean borrados de la base de datos también perderán su rol de Estudiante en el servidor
       """

    elif type == "duplicado":
        content = """
           La cedula que insertó ya se encontraba en la base de datos
       """
        
    elif type == "lista":
        content = """
            Todas los temas se muestran a continuación en orden:
            Nombre, número de grupos, capacidad máxima por grupo (si disponible)
        """

    elif type == "creartema":
        content = """
            Necesita proporcionar el nombre de un tema para permitir a los estudiantes formar grupos, opcionalmente puede incluir un numero al final del comando para limitar los grupos a N estudiantes.
            Si el último caracter es un número, será tomado como referencia para limitar el numero de integrantes por grupo
            Si necesita utilizar números para el nombre de su tema, opte por usar números romanos
            `!creartema (nombre del tema) (numero opcional)`
            Ejemplos:
            `!creartema Movimiento rectilineo uniforme taller 3` (para maximo de integrantes)
            `!creartema Taller I` (sin maximo especifico)
        """
    
    elif type == "borrartema":
        content = """
            Borrará un tema de la base de datos y sus grupos
            `!borrartema (numero del tema)`
            Ejemplos:
            `!grupos Movimiento rectilineo uniforme taller 3`
            `!grupos Taller I`
        """

    elif type == "creargrupo":
        content = """
            Crea un grupo para un respectivo tema
            `!creargrupo (numero del tema)`
            El numero del grupo será decidido automáticamente en secuencia
            Ejemplos:
            `!creargrupo 1`
            `!creargrupo 17`
        """

    elif type == "borrargrupo":
        content = """
            Borra un grupo de un respectivo tema
            Se debe especificar el número del grupo y del tema
            `!borrargrupo (numero de grupo) (numero de tema)`
            Ejemplos:
            `!borrargrupo 1 1`
            `!borrargrupo 4 2`
        """

    elif type == "entrargrupo":
        content = """
            Se añadirá al grupo elegido el usuario que ha llamado el comando
            `!entrargrupo (numero de grupo) (numero de tema)`
            Ejemplos:
            `!entrargrupo 1 1`
            `!entrargrupo 4 3`
        """

    elif type == "salirgrupo":
        content = """
            Se eliminará del grupo elegido el usuario que ha llamado el comando
            `!salirgrupo (numero de grupo) (numero de tema)`
            Ejemplos:
            `!salirgrupo 1 1`
            `!salirgrupo 4 3`
        """

    elif content == "":
        content = "No fue encontrado un contenido para este comando"

    return content
