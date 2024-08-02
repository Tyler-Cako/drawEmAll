<script>
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
</script>

<Navbar class="bg-poke_yellow-500">
	<NavBrand href="/">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
			>Draw'em All</span
		>
	</NavBrand>
	<NavHamburger />
	<NavUl>
		<NavLi href="/">Draw</NavLi>
		<NavLi href="/training">Training</NavLi>
		<NavLi href="/about">About</NavLi>
	</NavUl>
</Navbar>
