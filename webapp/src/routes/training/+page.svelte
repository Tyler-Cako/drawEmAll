<script lang="ts">
	import Draw from '$lib/components/Draw.svelte';
	import { onMount } from 'svelte';
	import type { PokemonJSON } from '$lib/types/PokemonJSON';
	import { Button } from 'flowbite-svelte';

	const pokemonArr = ['bulbasaur', 'charmander', 'squirtle'];
	let currentPokemon = pokemonArr[0];
	let pokemonJSON: PokemonJSON | null;

	let counter = 0;
	let counterDisplay = 1;

	const updateCounter = async () => {
		counter++;
		counterDisplay++;

		if (counter == 10) {
			counterDisplay = 1;
			currentPokemon = pokemonArr[1];
			updatePokemon();
		}
		if (counter == 20) {
			counterDisplay = 1;
			currentPokemon = pokemonArr[2];
			updatePokemon();
		}
	};

	const updatePokemon = async () => {
		const pokemonReq = await fetch(`https://pokeapi.co/api/v2/pokemon/${currentPokemon}`);
		pokemonJSON = await pokemonReq.json();
	};

	const uploadCanvas = async (blob: Blob) => {
		const response = await fetch('/training', {
			method: 'POST',
			body: JSON.stringify(await blob.text()),
			headers: {
				'Content-Type': 'application/json',
				pokemon: currentPokemon
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
		<div class="text-poke_red-500 flex justify-center align-center">
			<p>{counterDisplay}/10</p>
		</div>

		<Draw {pokemonJSON} on:canvasSubmit={(e) => uploadCanvas(e.detail.blob)} />
	{:else}
		<div>All done!</div>
		<Button data-sveltekit-reload href="/training">Train again</Button>
	{/if}
</div>
