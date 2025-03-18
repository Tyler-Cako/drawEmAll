<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { Button } from 'flowbite-svelte';
	import {
		type PokemonJSON,
		type PixelData,
		type CanvasPt,
		DrawTypes
	} from '$lib/types/PokemonJSON';
	import ColorPicker, { type RgbaColor } from 'svelte-awesome-color-picker';
	import { Range } from 'flowbite-svelte';

	const dispatch = createEventDispatcher();

	export let pokemonJSON: PokemonJSON | null;
	export let pokemonPrediction = "";

	let imgSize = 512;

	let canvasElement: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D;
	let prevCtx: ImageData;
	let mouseDown = false,
		touchDown = false;

	let prevX: number, prevY: number;
	let curX: number, curY: number;
	let offsetX: number, offsetY: number;

	let drawType: DrawTypes = DrawTypes.draw;
	let drawWidth: number = 3;

	let currColor: string;
	let currColorRgb: RgbaColor = { r: 0, g: 0, b: 0, a: 1 };

	let innerWidth: number = 0;

	$: {
		if (drawType == DrawTypes.erase) {
			currColor = '#ffffff';
			currColorRgb = { r: 255, g: 255, b: 255, a: 1 };
		}

		if (drawType == DrawTypes.draw) {
			currColor = '#000000';
			currColorRgb = { r: 0, g: 0, b: 0, a: 1 };
		}
	}

	const beginDraw = (e: MouseEvent) => {
		e.preventDefault();

		ctx.lineWidth = drawWidth;
		prevCtx = ctx.getImageData(0, 0, imgSize, imgSize);

		if (drawType == DrawTypes.fill) {
			drawFill(e);
		} else {
			prevX = e.offsetX;
			prevY = e.offsetY;

			mouseDown = true;
		}
	};

	const beginTouchDraw = (e: TouchEvent) => {
		e.preventDefault();

		ctx.lineWidth = drawWidth;
		prevCtx = ctx.getImageData(0, 0, imgSize, imgSize);

		offsetX = canvasElement.offsetLeft;
		offsetY = canvasElement.offsetTop;

		const touch = e.touches[0];

		if (drawType == DrawTypes.fill) {
			drawTouchFill(touch);
		} else {
			prevX = touch.pageX - offsetX;
			prevY = touch.pageY - offsetY;

			touchDown = true;
		}
	};

	const stopDraw = (e: MouseEvent) => {
		e.preventDefault();

		mouseDown = false;

		predictPokemon();
	};

	const stopTouchDraw = (e: TouchEvent) => {
		e.preventDefault();

		touchDown = false;

		predictPokemon();
	};

	const draw = (e: MouseEvent) => {
		e.preventDefault();

		if (mouseDown) {
			curX = e.offsetX;
			curY = e.offsetY;

			ctx.strokeStyle = currColor;

			ctx.beginPath();
			ctx.moveTo(prevX, prevY);
			ctx.lineTo(curX, curY);
			ctx.stroke();
			ctx.closePath();

			prevX = curX;
			prevY = curY;
		}
	};

	const touchDraw = (e: TouchEvent) => {
		e.preventDefault();

		const touch = e.touches[0];

		if (touchDown) {
			curX = touch.pageX - offsetX;
			curY = touch.pageY - offsetY;

			ctx.strokeStyle = currColor;

			ctx.beginPath();
			ctx.moveTo(prevX, prevY);
			ctx.lineTo(curX, curY);
			ctx.stroke();
			ctx.closePath();

			prevX = curX;
			prevY = curY;
		}
	};

	const drawFill = async (e: MouseEvent) => {
		e.preventDefault();

		const startX = e.offsetX;
		const startY = e.offsetY;
		
		// Start Queue for BFS
		const pixelsToCheck: Array<[number, number]> = [[startX, startY]];
		const visited = new Set<string>();

		// imageData object for updating canvas
		const imageData = ctx.getImageData(0, 0, imgSize, imgSize);

		// Selected color when filling
		const fillColor = currColorRgb;

		// Color of background when filling
		const targetColor = getPixel(imageData, startX, startY);

		ctx.fillStyle = currColor;

		// If selected color == current background: don't fill
		if (colorsMatchFill(targetColor, fillColor)) return;

		const range = 128 ** 2;

		while (pixelsToCheck.length > 0) {
			const [x, y] = pixelsToCheck.pop() || [-1, -1];
			const currentColor = getPixel(imageData, x, y);

			// Check if point is within canvas bounds
			if (x < 0 || y < 0 || x >= imgSize || y >= imgSize) continue;
			// Check if we have already filled
			if (visited.has(`${x},${y}`)) continue;

			// Check if we reached a boundary
			if (!colorsMatch(currentColor, targetColor, range)) {
				continue;
			}

			setPixel(imageData, fillColor, x, y);
			visited.add(`${x},${y}`);
			// If I reach the border pixel, I don't add the surrounding pixels to the queue so it misses a few white pixels.diagonal ones?
			pixelsToCheck.push([x + 1, y], [x - 1, y], [x, y - 1], [x, y + 1]);
		}

		// Final imageData update
		ctx.putImageData(imageData, 0, 0);
	};

	const drawTouchFill = async (touch: Touch) => {
		const rect = canvasElement.getBoundingClientRect();
		const startX = Math.floor(touch.clientX - rect.left);
		const startY = Math.floor(touch.clientY - rect.top);


		// Start Queue for BFS
		const pixelsToCheck: Array<[number, number]> = [[startX, startY]];
		const visited = new Set<string>();

		// imageData object for updating canvas
		const imageData = ctx.getImageData(0, 0, imgSize, imgSize);

		// Selected color when filling
		const fillColor = currColorRgb;

		// Color of background when filling
		const targetColor = getPixel(imageData, startX, startY);

		ctx.fillStyle = currColor;

		// If selected color == current background: don't fill
		if (colorsMatchFill(targetColor, fillColor)) return;

		const range = 128 ** 2;

		while (pixelsToCheck.length > 0) {
			const [x, y] = pixelsToCheck.pop() || [-1, -1];
			const currentColor = getPixel(imageData, x, y);

			// Check if point is within canvas bounds
			if (x < 0 || y < 0 || x >= imgSize || y >= imgSize) continue;
			// Check if we have already filled
			if (visited.has(`${x},${y}`)) continue;

			// Check if we reached a boundary
			if (!colorsMatch(currentColor, targetColor, range)) {
				continue;
			}

			setPixel(imageData, fillColor, x, y);
			visited.add(`${x},${y}`);
			// If I reach the border pixel, I don't add the surrounding pixels to the queue so it misses a few white pixels.diagonal ones?
			pixelsToCheck.push([x + 1, y], [x - 1, y], [x, y - 1], [x, y + 1]);
		}

		// Final imageData update
		ctx.putImageData(imageData, 0, 0);
	};

	const getPixel = (imageData: ImageData, x: number, y: number) => {
		const offset = (y * imageData.width + x) * 4;
		return imageData.data.slice(offset, offset + 4);
	};

	const setPixel = (imageData: ImageData, fillColor: RgbaColor, x: number, y: number) => {
		const offset = (y * imageData.width + x) * 4;
		imageData.data[offset] = fillColor.r;
		imageData.data[offset + 1] = fillColor.g;
		imageData.data[offset + 2] = fillColor.b;
		imageData.data[offset + 3] = 255;
	};

	const colorsMatchFill = (targetColor: Uint8ClampedArray, fillColor: RgbaColor) => {
		return (
			targetColor[0] == fillColor.r &&
			targetColor[1] == fillColor.g &&
			targetColor[2] == fillColor.b
		);
	};

	const colorsMatch = (a: Uint8ClampedArray, b: Uint8ClampedArray, rangeSq: number) => {
		const dr = a[0] - b[0];
		const dg = a[1] - b[1];
		const db = a[2] - b[2];
		const da = a[3] - b[3];
		return dr * dr + dg * dg + db * db + da * da < rangeSq;
	};

	const clearCanvas = () => {
		ctx.reset();
	};

	const handleMouseEnter = (e: MouseEvent) => {
		e.preventDefault();

		prevX = e.offsetX;
		prevY = e.offsetY;
	};

	const undo = () => {
		ctx.reset();

		ctx.putImageData(prevCtx, 0, 0);
	};

	const predictPokemon = () => {
		const canvasBlobRet = canvasElement.toBlob((blob: Blob | null) => {
				if (blob) {
					//saveAs(blob, "./test.png");
					dispatch('canvasSubmit', {
						blob: blob
					});
				} else {
					throw new Error('Blob creation failed!');
				}
			});
	}

	const submitCanvas = () => {
		try {
			predictPokemon();

			const pokemonCry = new Audio(pokemonJSON?.cries.latest);

			pokemonCry.volume = 0.3;
			pokemonCry.play();
			clearCanvas();
		} catch (error) {
			console.log(error);
		}
	};

	onMount(() => {
		if (innerWidth < imgSize && innerWidth <= 512) {
			imgSize = innerWidth;
		}

		if (innerWidth > 512) {
			imgSize = 512;
		}

		ctx = canvasElement.getContext('2d', { willReadFrequently: true }) as CanvasRenderingContext2D;
		ctx.fillStyle = '#ffffff';
		ctx.fillRect(0, 0, imgSize, imgSize);
	});
</script>

<svelte:window bind:innerWidth />

<div class="w-full flex items-center flex-col">
	<!-- <img src={pokemonJSON?.sprites.front_default} alt={pokemonJSON?.forms.name} /> -->
	{pokemonPrediction} &nbsp;
</div> 

<div class="flex w-full max-w-full flex-col items-center mt-5">
	<div>
		<div class="mb-3 flex bg-sky-500 shadow-slate-200 rounded-md p-5 w-full">
			<div class="flex flex-col w-1/3 space-y-1">
				<h6>Choose Color</h6>
				<ColorPicker bind:rgb={currColorRgb} bind:hex={currColor} />
				<h6>Paint size</h6>
				<div class="flex">
					<p class="w-1/6">{drawWidth}</p>
					<Range min="0" max="32" bind:value={drawWidth} />
				</div>
			</div>
			<div class="grid grid-cols-2 w-1/3 space-x-1 space-y-2 ml-12">
				<Button class="bg-pink-500" on:touchstart={() => (drawType = DrawTypes.draw)} on:click={() => (drawType = DrawTypes.draw)}>Draw</Button>
				<Button class="bg-green-500" on:touchstart={() => (drawType = DrawTypes.fill)} on:click={() => (drawType = DrawTypes.fill)}>Fill</Button>
				<Button class="bg-purple-500" on:touchstart={() => (drawType = DrawTypes.erase)} on:click={() => (drawType = DrawTypes.erase)}>Erase</Button>
				<Button class="bg-pink-500" on:touchstart={() => clearCanvas()} on:click={() => clearCanvas()}>Clear</Button>
			</div>
			<div class="flex h-1/2">
				<Button on:click={() => undo()}>Undo</Button>
			</div>
		</div>
		<canvas
			class="items-center flex-initial shadow-lg shadow-slate-600 bg-poke_white-500 rounded-md w-full"
			id="canvasElement"
			width={imgSize}
			height={imgSize}
			bind:this={canvasElement}
			on:mousedown={(e) => beginDraw(e)}
			on:touchstart={(e) => beginTouchDraw(e)}
			on:mouseup={(e) => stopDraw(e)}
			on:touchend={(e) => stopTouchDraw(e)}
			on:mousemove={(e) => draw(e)}
			on:touchmove={(e) => touchDraw(e)}
			on:mouseenter={(e) => handleMouseEnter(e)}
		/>
	</div>
	<div class="mt-3">
		<!-- <Button on:touchstart={() => submitCanvas()} on:click={() => submitCanvas()} class="bg-poke_red-500">Submit</Button> -->
	</div>
</div>
