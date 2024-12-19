<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import Draw from '$lib/components/Draw.svelte';
	import { onMount } from 'svelte';
	import type { PokemonJSON } from '$lib/types/PokemonJSON';

	const pokemonArr = ['bulbasaur', 'charmander', 'squirtle'];
	let currentPokemon = pokemonArr[0];
	let pokemonIndex = 0;
	let pokemonJSON: PokemonJSON | null;

	const updatePokemon = async () => {
		const pokemonReq = await fetch(`https://pokeapi.co/api/v2/pokemon/${currentPokemon}`);
		pokemonJSON = await pokemonReq.json();
	};

	const uploadCanvas = async (blob: Blob) => {
		const response: Response = await fetch('/predict', {
			method: 'POST',
			body: blob,
			headers: {
				'Content-Type': 'image/png',
				pokemon: currentPokemon
			}
		});
		if (response.ok) {
			const predictedPokemon = await response.text();
			alert(predictedPokemon);
			iteratePokemon();
		} else {
			throw new Error(`Unable to upload! ${response.status}: ${response.statusText}`);
		}
	};

	const iteratePokemon = () => {
		pokemonIndex = (pokemonIndex + 1) % pokemonArr.length;
		currentPokemon = pokemonArr[pokemonIndex];
		updatePokemon();
	};

	onMount(async () => {
		updatePokemon();
	});
</script>

<h2>Help train the model here:</h2>

<Button href="/training">Train</Button>

<Button on:click={iteratePokemon}>Next pokemon</Button>
<Draw {pokemonJSON} on:canvasSubmit={(e) => uploadCanvas(e.detail.blob)} />
