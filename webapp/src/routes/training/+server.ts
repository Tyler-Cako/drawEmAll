import { DefaultAzureCredential } from '@azure/identity';
import { BlobServiceClient } from '@azure/storage-blob';
import {
	AZURE_STORAGE_ACCOUNT_NAME,
	AZURE_BLOB_CONTAINER_NAME,
	AZURE_STORAGE_ACCOUNT_CONN_STRING
} from '$env/static/private';
import { uploadBlob } from '$lib/services/uploadBlob';
import fs from 'fs';

const accountName = AZURE_STORAGE_ACCOUNT_NAME;
const containerName = AZURE_BLOB_CONTAINER_NAME;
const connString = AZURE_STORAGE_ACCOUNT_CONN_STRING;

if (!accountName) throw Error('Azure Storage accountName not found');
if (!containerName) throw Error('Azure Container name not found');
if (!connString) throw Error('Azure Storage Account connection string not found');

export async function POST({ request }: { request: Request }) {
	//const reader = new FileReader();

	const dataURL = JSON.stringify(request);
	const pokemon = request.headers.get('pokemon');

	//reader.readAsDataUrl

	console.log(dataURL);

	//fs.writeFileSync('test3.txt', dataURL);

	const blobServiceClient = BlobServiceClient.fromConnectionString(connString);
	const containerClient = blobServiceClient.getContainerClient(`${containerName}/${pokemon}`);

	let response = new Response();

	if (pokemon) {
		//fs.writeFile('file.txt', blobText);
		//response = await uploadBlob(pokemon, blob, containerClient);
		//console.log(blob);
	} else {
		throw new Error('Pokemon not selected');
	}

	return response;
}
