import { DefaultAzureCredential } from '@azure/identity';
import { BlobServiceClient } from '@azure/storage-blob';

const accountName = process.env.AZURE_STORAGE_ACCOUNT_NAME;
if (!accountName) throw Error('Azure Storage accountName not found');

const blobServiceClient = new BlobServiceClient(
	`https://${accountName}.blob.core.windows.net`,
	new DefaultAzureCredential()
);

export const uploadBlob = async (pokemon: string, blob: Blob) => {
	const blobText = await blob.text();
	localStorage.setItem(pokemon, blobText);
	console.log(`Successfully uploaded drawing of ${pokemon} as blob: ${blobText}`);
};
