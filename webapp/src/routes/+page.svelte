<script lang="ts">
	import Draw from '$lib/components/Draw.svelte';
	
	let pokemonPrediction = "";

	const uploadCanvas = async (blob: Blob) => {
		const response: Response = await fetch('/predict', {
			method: 'POST',
			body: blob,
			headers: {
				'Content-Type': 'image/png',
			}
		});
		if (response.ok) {
			const predictedPokemon = await response.text();
			pokemonPrediction = predictedPokemon ?? pokemonPrediction;
		} else {
			throw new Error(`Unable to upload! ${response.status}: ${response.statusText}`);
		}
	}

</script>

<Draw {pokemonPrediction} on:canvasSubmit={(e) => uploadCanvas(e.detail.blob)} />
