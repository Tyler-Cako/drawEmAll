import { ContainerClient } from '@azure/storage-blob';

export const uploadBlob = async (
	pokemon: string,
	blob: string,
	containerClient: ContainerClient
): Promise<Response> => {
	try {
		const blobName = pokemon + new Date().getUTCMilliseconds();
		const blobClient = containerClient.getBlockBlobClient(blobName);

		const res = await blobClient.upload(blob, 1);
		console.log(`Successfully uploaded drawing of ${pokemon} as blob. ${res}`);
	} catch (error) {
		console.log(error);
	}

	return new Response();
};
