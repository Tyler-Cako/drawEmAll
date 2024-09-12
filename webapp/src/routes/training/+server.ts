import { DefaultAzureCredential } from '@azure/identity';
import { BlobServiceClient } from '@azure/storage-blob';
import { AZURE_STORAGE_ACCOUNT_NAME, AZURE_BLOB_CONTAINER_NAME } from '$env/static/private';
import { uploadBlob } from '$lib/services/uploadBlob';

const accountName = AZURE_STORAGE_ACCOUNT_NAME;
const containerName = AZURE_BLOB_CONTAINER_NAME;

if (!accountName) throw Error('Azure Storage accountName not found');
if (!containerName) throw Error('Azure Container name not found');

const blobServiceClient = new BlobServiceClient(
	`https://${accountName}.blob.core.windows.net`,
	new DefaultAzureCredential()
);

const containerClient = blobServiceClient.getContainerClient(containerName);

export async function POST({ request }: { request: Request }) {
	const blobText = await request.json();
	const pokemon = request.headers.get('pokemon');

	let response = new Response();

	if (pokemon) {
		response = await uploadBlob(pokemon, blobText, containerClient);
	} else {
		throw new Error('Pokemon not selected');
	}

	return response;
}
