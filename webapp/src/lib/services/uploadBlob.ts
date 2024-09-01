export const uploadBlob = async (pokemon: string, blob: Blob) => {
	const blobText = await blob.text();
	localStorage.setItem(pokemon, blobText);
	console.log(`Successfully uploaded drawing of ${pokemon} as blob: ${blobText}`);
};
