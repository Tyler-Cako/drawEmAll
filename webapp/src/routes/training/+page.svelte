<script lang="ts">
	import Draw from '$lib/components/Draw.svelte';
	import { onMount } from 'svelte';
	import { uploadBlob } from '$lib/services/uploadBlob';
	import type { PokemonJSON } from '$lib/types/PokemonJSON';

	const pokemonArr = ['bulbasaur', 'charmander', 'squirtle'];
	let currentPokemon = pokemonArr[0];
	let pokemonJSON: PokemonJSON | null;

	const uploadCanvas = (blob: Blob) => {
		uploadBlob(currentPokemon, blob);
	};

	onMount(async () => {
		const pokemonReq = await fetch(`https://pokeapi.co/api/v2/pokemon/${currentPokemon}`);
		console.log(pokemonReq);
		pokemonJSON = await pokemonReq.json();
		console.log(pokemonJSON);
		console.log(typeof pokemonJSON);
	});
</script>

<div>
	<div class="w-full flex items-center flex-col">
		<h2>Training</h2>
	</div>
	<Draw {pokemonJSON} on:canvasSubmit={(e) => uploadCanvas(e.detail.blob)} />
</div>
