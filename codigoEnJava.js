const { ConfidentialClientApplication } = require('@azure/msal-node');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Configuración de MSAL
const msalConfig = {
    auth: {
        clientId: "",
        authority: "https://login.microsoftonline.com/cd03ea4c-3ca9-4f23-94f2-cdc5293c5dde",
        clientSecret: "" 
    }
};

const cca = new ConfidentialClientApplication(msalConfig);

// Función para obtener el token de acceso
async function getToken() {
    const tokenRequest = {
        scopes: ["https://graph.microsoft.com/.default"]
    };

    try {
        const tokenResponse = await cca.acquireTokenByClientCredential(tokenRequest);
        return tokenResponse.accessToken;
    } catch (error) {
        console.error('Error al obtener el token:', error);
    }
}

// Función para subir un archivo a OneDrive
async function uploadFileToOneDrive(folderId, filePath) {
    const accessToken = await getToken();
    const fileName = path.basename(filePath);
    const uploadUrl = `https://graph.microsoft.com/v1.0/me/drive/items/${folderId}:/${fileName}:/content`;
    const fileStream = fs.createReadStream(filePath);

    try {
        // Lee el archivo
        const fileStream = fs.createReadStream(filePath);

        // Realiza la solicitud PUT para subir el archivo
        const response = await axios.put(uploadUrl, fileStream, {
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "text/plain"
            }
        });

        // Imprime la respuesta de la API
        console.log('Archivo subido exitosamente:', response.data);
    } catch (error) {
        // Maneja los errores
        console.error('Error durante la subida del archivo:', error.response?.data || error.message);
    }
}
const folderId = ' ';
const filePath = 'C:/Users/isabe/Desktop/prueba de OneDrive Api/ArchivoPrueba.txt';
// Ejecuta la función
uploadFileToOneDrive(folderId, filePath);
