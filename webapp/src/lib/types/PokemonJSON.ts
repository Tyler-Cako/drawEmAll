export type PokemonJSON = {
	sprites: Sprites;
	cries: Cries;
	forms: Forms;
};

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
