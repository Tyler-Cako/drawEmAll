<script lang="ts">
	import { onMount } from 'svelte';
	import { Button } from 'flowbite-svelte';

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
		const dataURL = canvasElement.toDataURL();
	};

	onMount(() => {
		ctx = canvasElement.getContext('2d') as CanvasRenderingContext2D;
	});
</script>

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
<Button>Submit</Button>
<Button on:click={() => clearCanvas()}>Clear Canvas</Button>
