import msal
import requests
import os

client_id = ''
tenant_id = '' 
client_secret = ''
authority = f"https://login.microsoftonline.com/{tenant_id}"
redirect_uri = 'http://localhost' 
scope = ["https://graph.microsoft.com/.default"]


# Crear una instancia de la aplicación 
app = msal.ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret,
)

# Adquirir un token de acceso
result = app.acquire_token_for_client(scopes=scope)

if "access_token" in result:
    # Realizar una solicitud a Microsoft Graph
    headers = {
        'Authorization': 'Bearer ' + result['access_token'],
        'Content-Type': 'text/plain'
    }
else:
    print("Error al obtener el token de acceso.")
    print(result.get("error"))

user_id = 'cd03ea4c-3ca9-4f23-94f2-cdc5293c5dde'
file_path =  r'C:\Users\isabe\Desktop\prueba de OneDrive Api\ArchivoPrueba.txt'
file_name = os.path.basename(file_path) # Extraer el nombre del archivo desde la ruta
GRAPH_API_ENDPOINT = f'https://graph.microsoft.com/v1.0/{user_id}/drive/items/root:/{file_name}:/content' # Endpoint de microsft graph para onedrive
print(file_name)

#abrir el archivo y leerlo en modo binario 
with open(file_path, 'rb') as upload:
    file_content = upload.read()

# Se hace una solicitud PUT a la API de Microsoft Graph para subir el archivo a OneDrive
response = requests.put(
    # /me/drive/items/root:/ se refiere a la raíz del directorio de OneDrive del usuario
    # :/content especifica que estamos subiendo el contenido del archivo
    GRAPH_API_ENDPOINT, 
    headers = headers,
    data=file_content
)
print(response.json())
    