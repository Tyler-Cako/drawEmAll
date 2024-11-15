<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { Button } from 'flowbite-svelte';
	import { type PokemonJSON, type PixelData, type CanvasPt, DrawTypes } from '$lib/types/PokemonJSON';
	import ColorPicker, { type RgbaColor } from 'svelte-awesome-color-picker';
	import { error } from '@sveltejs/kit';

	const dispatch = createEventDispatcher();

	export let pokemonJSON: PokemonJSON | null;

	const imgSize = 512;

	let canvasElement: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D;
	let mouseDown = false;

	let prevX: number;
	let prevY: number;
	let curX: number;
	let curY: number;

	let drawType: DrawTypes = DrawTypes.draw;

	let currColor: string;
	let currColorRgb: RgbaColor = {r: 0, g: 0, b: 0, a: 1};

	const beginDraw = (e: MouseEvent) => {
		e.preventDefault();

		if (drawType == DrawTypes.fill) {
			drawFill(e);
		} else {
			prevX = e.offsetX;
			prevY = e.offsetY;

			mouseDown = true;
		}
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

			ctx.strokeStyle = currColor;

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

	const drawFill = async (e: MouseEvent) => {
		e.preventDefault();

		const startX = e.offsetX;
		const startY = e.offsetY;

		// Start Queue for BFS
		const pixelsToCheck:Array<[number, number]> = [[startX, startY]];
		const visited = new Set<[number, number]>();

		// Init ticks for performance
		let tickCount = 0;
		const ticksPerUpdate = 50;

		// imageData object for updating canvas
		const imageData = ctx.getImageData(0, 0, imgSize, imgSize);

		// Selected color when filling
		const fillColor = currColorRgb;

		// Color of background when filling
   		const targetColor = getPixel(imageData, startX, startY);

		ctx.fillStyle = currColor;

		// If selected color == current background: don't fill
		if (colorsMatchFill(targetColor, fillColor)) return;

		const range = 128**2

		while (pixelsToCheck.length > 0 && tickCount < imgSize) {
			const [x, y] = pixelsToCheck.pop() || [-1, -1]
			const currentColor = getPixel(imageData, x, y);

			// Check if point is within canvas bounds
			//console.log(`(x, y): ${[x, y]}, currentColor: ${currentColor}`);
			if (x < 0 || y < 0 || x >= imgSize || y >= imgSize) {
				//console.log(`${[x, y]} out of bounds, continue`);
				continue;
			}
			// Check if we have hit a boundary

			// Check if point has already been visited. If not, add the point
			//console.log("3")
			if (visited.has([x, y])) {
				//console.log(`${[x, y]} has been visited!`)
				continue;
			} 


			//CHECK THIS CONDITION
			if (!colorsMatch(currentColor, targetColor, range)) {
				//console.log(`Colors don't match at (${[x, y]})`)
				continue;
			};

			//if (!colorsMatch(targetColor, fillColor)) continue;


			// Update pixel, add border pixels to the queue
			setPixel(imageData, fillColor, x, y);
			visited.add([x, y]); 
			pixelsToCheck.push([x + 1, y], [x - 1, y], [x, y - 1], [x, y + 1]);


			//Update imageData after x amount of ticks
			// tickCount++;
			// if (tickCount % ticksPerUpdate === 0) {
			// 	ctx.putImageData(imageData, 0, 0);
			// }
		}    

		// Final imageData update
		ctx.putImageData(imageData, 0, 0);
	}

	const getPixel = (imageData: ImageData, x: number, y: number) => {
		const offset = (y * imageData.width + x) * 4;
    	return imageData.data.slice(offset, offset + 4);
	}

	const setPixel = (imageData: ImageData, fillColor: RgbaColor, x: number, y: number) => {
		const offset = (y * imageData.width + x) * 4;
		imageData.data[offset] = fillColor.r;
		imageData.data[offset + 1] = fillColor.g;
		imageData.data[offset + 2] = fillColor.b;
		imageData.data[offset + 3] = 255;
	}

	const colorsMatchFill = (targetColor: Uint8ClampedArray, fillColor: RgbaColor) => {
		return (
			targetColor[0] == fillColor.r && 
			targetColor[1] == fillColor.g && 
			targetColor[2] == fillColor.b
		);
	}

	const colorsMatch = (a: Uint8ClampedArray, b: Uint8ClampedArray, rangeSq : number) => {
		const dr = a[0] - b[0];
		const dg = a[1] - b[1];
		const db = a[2] - b[2];
		const da = a[3] - b[3];
		return dr * dr + dg * dg + db * db + da * da < rangeSq;
	}

	const wait = (delay : number | undefined) => {
		if (!delay) delay = 0;
		return new Promise((resolve) => {
			setTimeout(resolve, delay);
		});
	}

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
			const canvasBlobRet = canvasElement.toBlob((blob : Blob | null) => {
				if (blob) {
					//saveAs(blob, "./test.png");
					dispatch('canvasSubmit', {
						blob: blob
					});
				} else {
					throw new Error("Blob creation failed!")
				}
			});

			const pokemonCry = new Audio(pokemonJSON?.cries.latest);

			pokemonCry.volume = 0.3;
			pokemonCry.play();
			clearCanvas();
		} catch (error) {
			console.log(error);
		}
	};

	onMount(() => {
		ctx = canvasElement.getContext("2d", {willReadFrequently : true}) as CanvasRenderingContext2D;
		ctx.fillStyle = "#ffffff"
		ctx.fillRect(0, 0, imgSize, imgSize)
	});

</script>


<div class="w-full flex items-center flex-col">
	<img src={pokemonJSON?.sprites.front_default} alt={pokemonJSON?.forms.name} />
</div>

<div class="flex w-full flex-col items-center">
	<div>
		<div class="mb-3">
			<!-- <Button class="bg-black" on:click={() => currColor = 'black'}>Black</Button> -->
			<ColorPicker 
				bind:rgb={currColorRgb}
				bind:hex={currColor}
			/>
			<Button class="bg-blue-500" on:click={() => drawType = DrawTypes.draw}>Draw</Button>
			<Button class="bg-purple-500" on:click={() => drawType = DrawTypes.fill}>Fill</Button>
		</div>
		<canvas
			class="items-center flex-initial shadow-lg shadow-slate-600 bg-poke_white-500 rounded-md"
			width={imgSize}
			height={imgSize}
			bind:this={canvasElement}
			on:mousedown={(e) => beginDraw(e)}
			on:mouseup={(e) => stopDraw(e)}
			on:mousemove={(e) => draw(e)}
			on:mouseenter={(e) => handleMouseEnter(e)}
		/>
	</div>
	<div class="mt-3">
		<Button on:click={() => submitCanvas()}>Submit</Button>
		<Button on:click={() => clearCanvas()}>Clear Canvas</Button>
	</div>
</div>