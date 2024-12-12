// import { spawn } from 'child_process';

export async function POST({ request }: { request: Request }) {
	let postRes = new Response();

	const reqBlob = await request.blob();

	try {
		const response = await fetch('http://localhost:7071/api/predict_pokemon', {
			method: 'POST',
			body: reqBlob
		});

		if (response.ok) {
			return response;
		} else {
			throw new Error(response.toString());
		}
	} catch (error) {
		console.log(`${error}`);
	}

	return postRes;
}
