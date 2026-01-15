import { pokemonArr } from '$lib/consts';
import { node, image, argMax, type LayersModel } from '@tensorflow/tfjs-node';
import { loadModel } from '$lib/models/model';

const model: LayersModel = await loadModel();

export async function POST({ request }: { request: Request }) {

	const reqBlob = await request.blob();

	try {
		const arrayBuffer = await reqBlob.arrayBuffer();

		// Convert ArrayBuffer to Uint8Array
		const uint8Array = new Uint8Array(arrayBuffer);

		// Decode image into a tensor
		let imageTensor = node.decodeImage(uint8Array, 3);
		imageTensor = image.resizeBilinear(imageTensor, [128, 128]);
		imageTensor = imageTensor.div(255.0);
		imageTensor = imageTensor.expandDims(0);


		const prediction = model.predict(imageTensor);
		const best_pred = argMax(prediction, 1).dataSync()[0];

		console.log(pokemonArr[best_pred]);

		return new Response(pokemonArr[best_pred]);
	} catch (error) {
		console.log(error);
	}

	return new Response('Prediction failed');
}


