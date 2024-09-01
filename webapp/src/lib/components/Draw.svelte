<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { Button } from 'flowbite-svelte';
	import type { PokemonJSON } from '$lib/types/PokemonJSON';

	const dispatch = createEventDispatcher();

	export let pokemonJSON: PokemonJSON | null;

	let canvasElement: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D;
	let mouseDown = false;

	let prevX: number;
	let prevY: number;
	let curX: number;
	let curY: number;

	const beginDraw = (e: MouseEvent) => {
		e.preventDefault();

		prevX = e.offsetX;
		prevY = e.offsetY;

		mouseDown = true;
	};

	const stopDraw = (e: MouseEvent) => {
		e.preventDefault();

		mouseDown = false;
	};

	const draw = (e: MouseEvent) => {
		e.preventDefault();

		if (mouseDown) {
			curX = e.offsetX;
			curY = e.offsetY;

			ctx.beginPath();
			ctx.moveTo(prevX, prevY);
			ctx.lineTo(curX, curY);
			ctx.lineWidth = 3;
			ctx.stroke();
			ctx.closePath();

			prevX = curX;
			prevY = curY;
		}
	};

	const clearCanvas = () => {
		ctx.reset();
	};

	const handleMouseEnter = (e: MouseEvent) => {
		e.preventDefault();

		prevX = e.offsetX;
		prevY = e.offsetY;
	};

	const submitCanvas = () => {
		try {
			canvasElement.toBlob((blob: Blob | null) => {
				if (blob) {
					dispatch('canvasSubmit', {
						blob: blob
					});
				}
			}, 'image/jpeg');

			const pokemonCry = new Audio(pokemonJSON?.cries.latest);

			pokemonCry.play();
			clearCanvas();
		} catch (error) {
			console.log(error);
		}
	};

	onMount(() => {
		console.log(pokemonJSON);
		ctx = canvasElement.getContext('2d') as CanvasRenderingContext2D;
	});
</script>

<div class="w-full flex items-center flex-col">
	<img src={pokemonJSON?.sprites.front_default} alt={pokemonJSON?.forms.name} />
</div>

<div class="flex justify-center">
	<canvas
		class="items-center shadow-lg shadow-slate-600 bg-poke_white-500 rounded-md"
		width="300"
		height="300"
		bind:this={canvasElement}
		on:mousedown={(e) => beginDraw(e)}
		on:mouseup={(e) => stopDraw(e)}
		on:mousemove={(e) => draw(e)}
		on:mouseenter={(e) => handleMouseEnter(e)}
	/>
</div>
<Button on:click={() => submitCanvas()}>Submit</Button>
<Button on:click={() => clearCanvas()}>Clear Canvas</Button>
