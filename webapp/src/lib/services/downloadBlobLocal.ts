import { BlobServiceClient } from '@azure/storage-blob';
import {
	AZURE_STORAGE_ACCOUNT_NAME,
	AZURE_BLOB_CONTAINER_NAME,
	AZURE_STORAGE_ACCOUNT_CONN_STRING
} from '$env/static/private';

const accountName = AZURE_STORAGE_ACCOUNT_NAME;
const containerName = AZURE_BLOB_CONTAINER_NAME;
const connString = AZURE_STORAGE_ACCOUNT_CONN_STRING;

const downloadBlobLocal = async () => {
    const blobServiceClient = BlobServiceClient.fromConnectionString(connString);
	const containerClient = blobServiceClient.getContainerClient(`${containerName}/${pokemon}`);

    const blobClient = containerClient.getBlockBlobClient(blobName);

    const blobDownload = await blobClient.downloadToFile(`./images/${blobName}`, 0, {
        blobHTTPHeaders: {
            blobContentType: "image/png"
        }
    });

    console.log(`Successfully downloaded blob: ${blobDownload}`);
}