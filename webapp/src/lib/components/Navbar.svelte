<script>
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
	import { base } from '$app/paths';
</script>

<Navbar class="bg-poke_yellow-500">
	<NavBrand href="/">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
			>Draw'em All</span
		>
	</NavBrand>
	<NavHamburger />
	<NavUl>
		<NavLi href={base + '/'}>Draw</NavLi>
		<NavLi href={base + '/training'}>Training</NavLi>
		<NavLi href={base + '/about'}>About</NavLi>
	</NavUl>
</Navbar>
