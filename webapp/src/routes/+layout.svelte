<script>
	import '../app.css';

	$: innerWidth = 0;
</script>

<svelte:window bind:innerWidth />

<div class="min-h-screen min-w-fit bg-[url(bg.jpg)] bg-cover bg-[position:center]">
	{#if innerWidth >= 768}
		<div class="flex align-center justify-center h-full">
			<div class="w-9/12 h-full">
				<slot />
			</div>
		</div>
	{:else}
		<div class="flex align-center justify-center h-full">
			<div class="w-11/12 h-full">
				<slot />
			</div>
		</div>
	{/if}
</div>
