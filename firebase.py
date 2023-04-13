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
    ref = db.collection(str(guild)).document(str(cedula))
    ver = await ref.get()
    if(not ver.exists):
        await ref.set({
            'nombre': ''
        })
        return True
    else: return False

async def deleteStudent(cedula, guild):
    delete = db.collection(str(guild)).document(str(cedula))
    ver = await delete.get()
    if(ver.exists):
        await delete.delete()
        return True
    else:
        return False
    
async def identifyStudent(cedula, nombre,discordId, guild):
    nombrec = nombre[1:len(nombre)]
    update = db.collection(str(guild)).document(str(cedula))
    ver = await update.get()
    if(ver.exists):
        await update.update({
            'nombre' : nombrec,
            'id': discordId
        })
        return True
    else:
        return False

