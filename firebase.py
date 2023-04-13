import json
import firebase_admin
import discord
from firebase_admin import credentials, firestore_async
 #Object that gives acceses to CRUD functions
from config import read_config

# Create the Secret Manager client.
# client = secretmanager.SecretManagerServiceClient()

# Build the resource name of the secret version.
name = read_config('firebase_key_path')

# Add Realtime Firebase datab link
url = read_config('firebase_url') # <- Add parameter into yaml config file

# Access the secret version.
# service_account = client.access_secret_version(request={"name": name})

# Create firebase_admin credentials from secret.
cred = credentials.Certificate(read_config('firebase_key'))

firebase_admin.initialize_app(cred,{
    'databaseURL':  url, #<- read_config('firebase_url') here
})

db = firestore_async.client()



async def saveStudent(cedula,guild):
    ref = db.collection('guilds').document(str(guild)).collection('cedulas').document(str(cedula))
    ver = await ref.get()
    if(not ver.exists):
        await ref.set({
            'nombre': ''
        })
        return True
    else: return False

async def deleteStudent(cedula, guild):
    delete = db.collection('guilds').document(str(guild)).collection('cedulas').document(str(cedula))
    ver = await delete.get()
    if(ver.exists):
        await delete.delete()
        return True
    else:
        return False
    
async def identifyStudent(cedula, nombre,discordId, guild):
    nombrec = nombre[1:len(nombre)]
    update = db.collection('guilds').document(str(guild)).collection('cedulas').document(str(cedula))
    ver = await update.get()
    if(ver.exists):
        await update.update({
            'nombre' : nombrec,
            'id': discordId
        })
        return True
    else:
        return False

async def findStudent(discordId, guild):
    student = db.collection('guilds').document(str(guild)).collection('cedulas').where('id','==',discordId)
    ver = await student.get()
    if(ver):
        return ver[0].id
    return False
    
async def nTemas(guild):
    ref = db.collection('guilds').document(str(guild)).collection('temas').document('estadistica')
    ver = await ref.get()
    if(ver.exists):
        return ver.to_dict()['n']
    else:
        await ref.set({
            'n': 0
        })
        ver = await ref.get().to_dict()
        return ver['n']

async def addTemas(guild):
    ref = db.collection('guilds').document(str(guild)).collection('temas').document('estadistica')
    ver = await ref.get()
    if(ver.exists):
        n = ver.to_dict()
        await ref.set({
            'n': (n['n']+1)
        })
        return (n['n']+1)
    
async def substractTemas(guild):
    ref = db.collection('guilds').document(str(guild)).collection('temas').document('estadistica')
    ver = await ref.get()
    if(ver.exists):
        n = ver.to_dict()
        await ref.set({
            'n': (n['n']-1)
        })
        return (n['n']-1)
    
async def listTemas(guild):
    ref = db.collection('guilds').document(str(guild)).collection('temas')
    ver = await ref.get()
    table = []
    
    if(ver):
        for i, tema in enumerate(ver):
            totalGroup = []
            groups = int(await nGrupo(guild,(i+1)))
            aux = 1
            while(aux<=groups):    
                groupsRef = db.collection('guilds').document(str(guild)).collection('temas').document(str(i+1)).collection('grupos').document(str(aux))
                verGroups = await groupsRef.get()
                if(verGroups.exists):
                    groupInfo = verGroups.to_dict()
                    print(groupInfo)
                    totalGroup.append({'#':aux,'integrantes':groupInfo["integrantes"]})
                aux+=1
            if("nombre" in tema.to_dict()):
                table.append({'tema':tema.to_dict()["nombre"],'grupos':totalGroup})
    
        return table

async def capacityTema(guild,tema):
    ref = db.collection('guilds').document(str(guild)).collection('temas').document('estadistica')
    ver = await ref.get()
    capacity = ver.to_dict()
    if(ver.exists and "capacidad" in capacity):
        return capacity["capacidad"]

async def saveTema(data, guild):
    temas = await nTemas(guild)
    last = len(data)
    ref = db.collection('guilds').document(str(guild)).collection('temas').document(str(temas+1))

    if(data[last].isnumeric()):
        ver = await ref.get()
        if(not ver.exists):
            await ref.set({
                'nombre': data[0:(last-1)],
                'capacidad': data[last]
            })
            await addTemas(guild)
            return True
        else:
            return False
    else:
        ver = await ref.get()
        if(not ver.exists):
            await ref.set({
                'nombre': data
            })
            await addTemas(guild)
            return True
        else:
            return False

async def deleteTema(tema, guild):
    delete = db.collection('guilds').document(str(guild)).collection('temas').document(str(tema))
    ver = await delete.get()
    if(ver.exists):
        await delete.delete()
        await substractTemas(guild)
        await rotateTema(tema,guild)
        return True
    else:
        return False
    

async def rotateTema(tema,guild):
    n = int(await nTemas(guild))
    temas = n - int(tema)
    pointer = int(tema)
    while(temas<n):
        rotate = db.collection('guilds').document(str(guild)).collection('temas').document(str(pointer + 1))
        replace = db.collection('guilds').document(str(guild)).collection('temas').document(str(pointer))
        ver = await rotate.get()
        if(ver.exists):
            await replace.set(ver.to_dict())
        temas += 1
        pointer += 1
    deleteLast = db.collection('guilds').document(str(guild)).collection('temas').document(str(n+1))
    await deleteLast.delete()

async def nGrupo(guild, tema):
    ref = db.collection('guilds').document(str(guild)).collection('temas').document(str(tema)).collection('grupos').document('estadistica')
    ver = await ref.get()
    if(ver.exists):
        return ver.to_dict()['n']
    else:
        await ref.set({
            'n': 0
        })
        ver = await ref.get()
        ver = ver.to_dict()
        return ver['n']

async def addGrupo(guild,tema):
    ref = db.collection('guilds').document(str(guild)).collection('temas').document(tema).collection('grupos').document('estadistica')
    ver = await ref.get()
    if(ver.exists):
        n = ver.to_dict()
        await ref.set({
            'n': (n['n']+1)
        })
        return (n['n']+1)

async def substractGrupo(guild,tema):
    ref = db.collection('guilds').document(str(guild)).collection('temas').document(tema).collection('grupos').document('estadistica')
    ver = await ref.get()
    if(ver.exists):
        n = ver.to_dict()
        await ref.set({
            'n': (n['n']-1)
        })
        return (n['n']-1)

async def saveGrupo(discordId,tema,guild):
    grupos = await nGrupo(guild,tema)
    cedula = await findStudent(discordId,guild)
    ref = db.collection('guilds').document(str(guild)).collection('temas').document(str(tema)).collection('grupos').document(str(grupos+1))
    ver = await ref.get()
    if(not ver.exists):
        await ref.set({
            'integrantes':[cedula]
        })
        await addGrupo(guild,tema)
        return True
    else:
        return False
    

async def deleteGrupo(grupo, tema, guild):
    delete = db.collection('guilds').document(str(guild)).collection('temas').document(str(tema)).collection('grupos').document(str(grupo))
    ver = await delete.get()
    if(ver.exists):
        await delete.delete()
        await substractGrupo(guild,tema)
        await rotateGrupo(grupo,tema,guild)
        return True
    else:
        return False

async def rotateGrupo(grupo, tema, guild):
    n = int(await nGrupo(guild,tema))
    grupos = n - int(grupo)
    pointer = int(grupo)
    while(grupos<n):
        rotate = db.collection('guilds').document(str(guild)).collection('temas').document(str(tema)).collection('grupos').document(str(pointer + 1))
        replace = db.collection('guilds').document(str(guild)).collection('temas').document(str(tema)).collection('grupos').document(str(pointer))
        ver = await rotate.get()
        if(ver.exists):
            await replace.set(ver.to_dict())
        grupos += 1
        pointer += 1
    deleteLast = db.collection('guilds').document(str(guild)).collection('temas').document(str(tema)).collection('grupos').document(str(n+1))

    await deleteLast.delete()

async def appendEstudiante(discordId, grupo, tema, guild):
    cedula = await findStudent(discordId,guild)
    tema = db.collection('guilds').document(str(guild)).collection('temas').document(str(tema)).collection('grupos').document(str(grupo))

    estudiante = db.collection('guilds').document(str(guild)).collection('cedulas').document(str(cedula))
    capacidad = await capacityTema(guild, tema)

    ver = await estudiante.get()
    verTema = await tema.get()
    
    if(ver.exists and verTema.exists):
        cedulas = verTema.to_dict()['integrantes']
        cedulas.append(cedula)
        if (capacidad):
            if(capacidad <= len(cedulas)):
                return False
        
        await tema.set({
            'integrantes':cedulas
        })
        return True
    else:
        return False
    
async def popEstudiante(discordId, grupo, tema, guild):
    cedula = await findStudent(discordId,guild)
    tema = db.collection('guilds').document(str(guild)).collection('temas').document(str(tema)).collection('grupos').document(str(grupo))
    estudiante = db.collection('guilds').document(str(guild)).collection('cedulas').document(str(cedula))

    ver = await estudiante.get()
    verTema = await tema.get()

    if(ver.exists and verTema.exists):
        cedulas = verTema.to_dict()['integrantes']
        if cedula in cedulas:
            cedulas.remove(cedula)
        else:
            return False
        await tema.set({
            'integrantes':cedulas
        })
        if(not cedulas):
            await tema.delete()
        return True
    else:
        return False