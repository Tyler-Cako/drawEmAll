<script>
	import '../app.css';
	import Navbar from '$lib/components/Navbar.svelte';
</script>

<div class="h-screen">
	<Navbar />
	<div class="flex align-center justify-center bg-blue-500">
		<div class="w-9/12 bg-purple-500">
			<slot />
		</div>
	</div>
</div>
