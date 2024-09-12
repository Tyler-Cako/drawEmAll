<script lang="ts">
	import Draw from '$lib/components/Draw.svelte';
	import { onMount } from 'svelte';
	import { uploadBlob } from '$lib/services/uploadBlob';
	import type { PokemonJSON } from '$lib/types/PokemonJSON';
	import { Button } from 'flowbite-svelte';

	const pokemonArr = ['bulbasaur', 'charmander', 'squirtle'];
	let currentPokemon = pokemonArr[0];
	let pokemonJSON: PokemonJSON | null;

	let counter = 0;

	const updateCounter = async () => {
		counter++;

		if (counter == 10) {
			currentPokemon = pokemonArr[1];
			updatePokemon();
		}
		if (counter == 20) {
			currentPokemon = pokemonArr[2];
			updatePokemon();
		}

		console.log(counter);
	};

	const updatePokemon = async () => {
		const pokemonReq = await fetch(`https://pokeapi.co/api/v2/pokemon/${currentPokemon}`);
		pokemonJSON = await pokemonReq.json();
	};

	const uploadCanvas = async (blob: Blob) => {
		const response = await fetch('/', {
			method: 'POST',
			body: blob,
			headers: {
				'Content-Type': 'application/json'
			}
		});
		if (response.ok) {
			updateCounter();
		} else {
			throw new Error(`Unable to upload! ${response.status}: ${response.statusText}`);
		}
	};

	onMount(async () => {
		updatePokemon();
	});
</script>

<div>
	<div class="w-full flex items-center flex-col">
		<h2>Training</h2>
	</div>
	{#if counter < 30}
		<Draw {pokemonJSON} on:canvasSubmit={(e) => uploadCanvas(e.detail.blob)} />
	{:else}
		<div>All done!</div>
		<Button data-sveltekit-reload href="/training">Train again</Button>
	{/if}
</div>
