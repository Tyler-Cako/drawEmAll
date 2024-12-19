export type PokemonJSON = {
	sprites: Sprites;
	cries: Cries;
	forms: Forms;
};

export type PixelData = {
	width: number;
	height: number;
	data: Uint32Array;
};

export const enum DrawTypes {
	draw = 'draw',
	fill = 'fill',
	erase = 'erase'
}

export type CanvasPt = [number, number];

type Sprites = {
	front_default: string;
};

type Cries = {
	latest: string;
	legacy: string;
};

type Forms = {
	name: string;
};
