<script>
	import '../app.css';
	import Navbar from '$lib/components/Navbar.svelte';
</script>

<div class="h-screen">
	<Navbar />
	<div class="flex align-center justify-center bg-poke_blue-400 h-full">
		<div class="w-9/12 h-full">
			<slot />
		</div>
	</div>
</div>
