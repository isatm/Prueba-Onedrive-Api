import os
import requests # Se debe instalar msal "pip install requests"
import webbrowser
from msal import ConfidentialClientApplication  # Se debe instalar msal "pip install msal"

# Todo esto se saca de azure
client_secret = ' '
app_id = ' '
SCOPES = ['Files.ReadWrite']
REDIRECT_URI = 'http://localhost'  # Se debe modificar la uri (en azure)

# CODIGO PARA EL TOKEN

# Usamos ConfidentialClientApplication para clientes confidenciales y el endpoint correcto para consumidores
client = ConfidentialClientApplication(
    client_id=app_id,
    client_credential=client_secret,
    authority='https://login.microsoftonline.com/consumers' # Endpoint código de autenticación de Microsoft (solo de cuentas personales)
) 
# https://login.microsoftonline.com/common  endpoint personales y organizacionales

# Se solicita al cliente que inicie sesión para obtener la URL de autorización
authorization_url = client.get_authorization_request_url(
    SCOPES, 
    redirect_uri=REDIRECT_URI
)
webbrowser.open(authorization_url)

authorization_code = input("Introduce el código de autorización: ")

# Se usa el código de autorización para solicitar un token de acceso
access_token_response = client.acquire_token_by_authorization_code(
    code = authorization_code, 
    scopes = SCOPES,
    redirect_uri=REDIRECT_URI 
)

# Extraemos el token de acceso de la respuesta
access_token = access_token_response['access_token']

print(access_token)
# SUBIR EL ARCHIVO

# Configuración de los encabezados para la solicitud
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'text/plain'
}

GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0' # Endpoint de microsft graph para onedrive
file_path =  r'C:\Users\isabe\Desktop\prueba de OneDrive Api\ArchivoPrueba.txt'
file_name = os.path.basename(file_path) # Extraer el nombre del archivo desde la ruta
print(file_name)

#abrir el archivo y leerlo en modo binario 
with open(file_path, 'rb') as upload:
    file_content = upload.read()

# Se hace una solicitud PUT a la API de Microsoft Graph para subir el archivo a OneDrive
response = requests.put(
    # /me/drive/items/root:/ se refiere a la raíz del directorio de OneDrive del usuario
    # :/content especifica que estamos subiendo el contenido del archivo
    GRAPH_API_ENDPOINT + f'/me/drive/items/root:/{file_name}:/content', 
    headers = headers,
    data=file_content
)
print(response.json())
    
