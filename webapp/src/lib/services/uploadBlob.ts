import { ContainerClient } from '@azure/storage-blob';
import { setLogLevel } from '@azure/logger';
import { BlobServiceClient } from '@azure/storage-blob';
import {
	AZURE_STORAGE_ACCOUNT_NAME,
	AZURE_BLOB_CONTAINER_NAME,
	AZURE_STORAGE_ACCOUNT_CONN_STRING
} from '$env/static/private';

const accountName = AZURE_STORAGE_ACCOUNT_NAME;
const containerName = AZURE_BLOB_CONTAINER_NAME;
const connString = AZURE_STORAGE_ACCOUNT_CONN_STRING;

if (!accountName) throw Error('Azure Storage accountName not found');
if (!containerName) throw Error('Azure Container name not found');
if (!connString) throw Error('Azure Storage Account connection string not found');

setLogLevel('info');

export const uploadBlob = async (
	pokemon: string,
	imgBlob: Blob,
	containerClient: ContainerClient
): Promise<Response> => {
	try {
		const blobName = pokemon + new Date().getUTCMilliseconds() + '.png';
		const blobClient = containerClient.getBlockBlobClient(blobName);

		const blobStr = await imgBlob.text();

		const res = await blobClient.upload(blobStr, blobStr.length, {
			blobHTTPHeaders: {
				blobContentType: "image/png"
			},
		});
		console.log(`Successfully uploaded drawing of ${pokemon} as blob. ${JSON.stringify(res)}`);
	} catch (error) {
		throw new Error(`ERROR THROWN: ${JSON.stringify(error)}`);
	}

	return new Response();
};
