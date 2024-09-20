import { ContainerClient } from '@azure/storage-blob';
import { setLogLevel } from '@azure/logger';

setLogLevel('info');

export const uploadBlob = async (
	pokemon: string,
	imgBlob: Blob,
	containerClient: ContainerClient
): Promise<Response> => {
	try {
		const blobName = pokemon + new Date().getUTCMilliseconds() + '.png';
		const blobClient = containerClient.getBlockBlobClient(blobName);

		// const blobUpload = new Blob([imgBlob], {
		// 	type: 'image/png'
		// });

		console.log(await imgBlob.text());

		const res = await blobClient.upload(await imgBlob.text(), 1);
		//console.log(`Successfully uploaded drawing of ${pokemon} as blob. ${JSON.stringify(res)}`);
	} catch (error) {
		throw new Error(`ERROR THROWN: ${JSON.stringify(error)}`);
	}

	return new Response();
};
