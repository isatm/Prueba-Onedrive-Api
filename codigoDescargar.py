import os
import requests # Se debe instalar msal "pip install requests"
import webbrowser
from msal import ConfidentialClientApplication  # Se debe instalar msal "pip install msal"
import msal


client_secret = ''  
app_id =  '' 
SCOPES = ['Files.ReadWrite']
REDIRECT_URI = 'http://localhost'  # Se debe modificar la uri (en azure)

# CODIGO PARA EL TOKEN

# Usamos ConfidentialClientApplication para clientes confidenciales y el endpoint correcto para consumidores
client = ConfidentialClientApplication(
    client_id=app_id,
    client_credential=client_secret,
    authority='https://login.microsoftonline.com/consumers' # Endpoint código de autenticación de Microsoft (solo de cuentas personales)
) 


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
access_token = access_token_response.get('access_token')

if not access_token:
    print("Error al obtener el token de acceso")
    exit()

# Id del archivo que esta en onedrive
file_id = '6D5E9E581F00A524!s1b3bd3e78d6342eebbc72a1a114ed1ba'

url = f'https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content'

# Hacer la solicitud GET con el token de acceso
headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(url, headers=headers)

# Verificar si la solicitud fue exitosa con el codigo de estado de respuesta http
# 200 = salio bien 
if response.status_code == 200:
    # Guardar el archivo en tu sistema local
    with open('downloaded_file', 'wb') as file:
        file.write(response.content)
    print('Archivo descargado con éxito.')
else:
    print(f'Error al descargar el archivo: {response.status_code}')
    print(response.json())