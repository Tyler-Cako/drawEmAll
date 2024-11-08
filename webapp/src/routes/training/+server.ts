import { DefaultAzureCredential } from '@azure/identity';
import { BlobServiceClient } from '@azure/storage-blob';
import {
	AZURE_STORAGE_ACCOUNT_NAME,
	AZURE_BLOB_CONTAINER_NAME,
	AZURE_STORAGE_ACCOUNT_CONN_STRING
} from '$env/static/private';
import { uploadBlob } from '$lib/services/uploadBlob';

const accountName = AZURE_STORAGE_ACCOUNT_NAME;
const containerName = AZURE_BLOB_CONTAINER_NAME;
const connString = AZURE_STORAGE_ACCOUNT_CONN_STRING;

if (!accountName) throw Error('Azure Storage accountName not found');
if (!containerName) throw Error('Azure Container name not found');
if (!connString) throw Error('Azure Storage Account connection string not found');

export async function POST({ request }: { request: Request }) {
	let postRes = new Response;

	const reqBlob = await request.blob();
	const pokemon = request.headers.get('pokemon');

	try {

	const blobServiceClient = BlobServiceClient.fromConnectionString(connString);
	const containerClient = blobServiceClient.getContainerClient(`${containerName}/${pokemon}`);

	if (pokemon) {
		const blobName = pokemon + new Date().getUTCMilliseconds() + '.png';
		const blobClient = containerClient.getBlockBlobClient(blobName);

		const blobBuffer = await reqBlob.arrayBuffer();

		const res = await blobClient.upload(blobBuffer, blobBuffer.byteLength, {
			blobHTTPHeaders: {
				blobContentType: "image/png"
			},
		});

		// const blobDownload = await blobClient.downloadToFile(`./images/${blobName}`, 0, {
		// 	blobHTTPHeaders: {
		// 		blobContentType: "image/png"
		// 	}
		// });

		postRes = new Response(`Successfully uploaded drawing of ${pokemon} as blob with name of ${blobName}`);

		//console.log(`Successfully downloaded blob: ${blobDownload}`);
		console.log(`Successfully uploaded drawing of ${pokemon} as blob. ${JSON.stringify(res)}`);
	} else {
		throw new Error('Pokemon not selected');
	}
	} catch (error) {
		console.log(`${error}`);
	}

	return postRes;
}
