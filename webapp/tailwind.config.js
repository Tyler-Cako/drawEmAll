import 'flowbite/plugin';

const config = {
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		'./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'
	],

	plugins: [require('flowbite/plugin')],

	darkMode: 'selector',

	theme: {
		extend: {
			colors: {
				// flowbite-svelte
				primary: {
					50: '#ffffff',
					100: '#ffffff',
					200: '#ffffff',
					300: '#ffffff',
					400: '#ffffff',
					500: '#ffffff',
					600: '#ffffff',
					700: '#8c8c8c',
					800: '#8c8c8c',
					900: '#8c8c8c'
				},
				poke_red: {
					400: '#ea5c50',
					500: '#fc332f'
				},
				poke_white: {
					500: '#feffff'
				},
				poke_yellow: {
					500: '##FFCB05'
				},
				poke_blue: {
					400: '#3D7DCA',
					500: '#003A70'
				}
			}
		}
	}
};

module.exports = config;
