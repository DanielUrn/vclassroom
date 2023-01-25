from discord import Embed, Colour

def get_embed(type):
    embed = Embed(title='Virtual Classroom', colour=Colour.from_rgb(3,178,248))
    embed.set_author(name='Virtual Classroom', url='https://www.urbe.edu/', icon_url='https://www.urbe.edu/images/logos/logo-urbe1.jpg')
    if type == "help":
        embed.add_field(name="Ayuda Virtual Classroom", value="Para más información acerca de un `Comando` escribe: **!help (comando)**\n Para más información sobre una `Categoria` escribe **!help (categoría)**", inline=False)
    else:
        embed.add_field(name='Mensaje automático - No responder', value=get_content(type))

    return embed

def get_content(type):
    content = ""
    if type == "bienvenida":
        content="""Bienvenido a Virtual Classroom
        Este es un proyecto de tésis diseñado como alternativa a un salón de clases virtual a través de Discord"""
    
    elif type == "identificar":
        content= """
            ***!identificar (cedula) (nombre y apellido)***
            Insertar datos sin parentesis, con un solo espacio entre datos
            
            Puede volver a ejecutar el comando si cometió un error para actualizar su nombre de nuevo
        """
    elif type == "registrar":
        content= """
            ***!registrar (cedula)***
            Insertar datos sin parentesis, con un solo espacio entre datos
            Puede registrar varias cedulas al mismo tiempo
        """
    elif type == "borrar":
       content= """
           ***!borrar (cedula)***
           Insertar datos sin parentesis, con un solo espacio entre datos
           Puede borrar varias cedulas al mismo tiempo
           Los estudiantes que sean borrados de la base de datos también perderán su rol de Estudiante en el servidor
       """

    elif content == "":
        content = "No embed content found"
        
    return content
