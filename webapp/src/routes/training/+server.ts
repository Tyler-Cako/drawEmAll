import { DefaultAzureCredential } from '@azure/identity';
import { BlobServiceClient } from '@azure/storage-blob';
import { AZURE_STORAGE_ACCOUNT_NAME, AZURE_BLOB_CONTAINER_NAME } from '$env/static/private';
import uploadBlob from '$lib/services/uploadBlob';

const accountName = AZURE_STORAGE_ACCOUNT_NAME;
const containerName = AZURE_BLOB_CONTAINER_NAME;

if (!accountName) throw Error('Azure Storage accountName not found');
if (!containerName) throw Error('Azure Container name not found');

const blobServiceClient = new BlobServiceClient(
	`https://${accountName}.blob.core.windows.net`,
	new DefaultAzureCredential()
);

const containerClient = blobServiceClient.getContainerClient(containerName);

export const actions = {
	formUploadBlob: async ({ request }) => {
		const data = await request.formData();
	}
};
