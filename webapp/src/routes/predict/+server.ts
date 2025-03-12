import tf from '@tensorflow/tfjs-node';
import path from 'path';
import { fileURLToPath } from 'url';

// Manually define __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const modelPath = path.resolve(__dirname, 'well_trained_model/model.json');
const modelUrl = `file://${modelPath}`;

console.log('test1');

//ill move this later
const pokemonArr = [
	'Abra',
	'Aerodactyl',
	'Alakazam',
	'Arbok',
	'Arcanine',
	'Articuno',
	'Beedrill',
	'Bellsprout',
	'Blastoise',
	'Bulbasaur',
	'Butterfree',
	'Caterpie',
	'Chansey',
	'Charizard',
	'Charmander',
	'Charmeleon',
	'Clefable',
	'Clefairy',
	'Cloyster',
	'Cubone',
	'Dewgong',
	'Diglett',
	'Ditto',
	'Dodrio',
	'Doduo',
	'Dragonair',
	'Dragonite',
	'Dratini',
	'Drowzee',
	'Dugtrio',
	'Eevee',
	'Ekans',
	'Electabuzz',
	'Electrode',
	'Exeggcute',
	'Exeggutor',
	'Farfetchd',
	'Fearow',
	'Flareon',
	'Gastly',
	'Gengar',
	'Geodude',
	'Gloom',
	'Golbat',
	'Goldeen',
	'Golduck',
	'Graveler',
	'Grimer',
	'Growlithe',
	'Gyarados',
	'Haunter',
	'Hitmonchan',
	'Hitmonlee',
	'Horsea',
	'Hypno',
	'Ivysaur',
	'Jigglypuff',
	'Jolteon',
	'Jynx',
	'Kabutops',
	'Kadabra',
	'Kakuna',
	'Kangaskhan',
	'Kingler',
	'Koffing',
	'Lapras',
	'Lickitung',
	'Machamp',
	'Machoke',
	'Machop',
	'Magikarp',
	'Magmar',
	'Magnemite',
	'Magneton',
	'Mankey',
	'Marowak',
	'Meowth',
	'Metapod',
	'Mew',
	'Mewtwo',
	'Moltres',
	'MrMime',
	'Nidoking',
	'Nidoqueen',
	'Nidorina',
	'Nidorino',
	'Ninetales',
	'Oddish',
	'Omanyte',
	'Omastar',
	'Parasect',
	'Pidgeot',
	'Pidgeotto',
	'Pidgey',
	'Pikachu',
	'Pinsir',
	'Poliwag',
	'Poliwhirl',
	'Poliwrath',
	'Ponyta',
	'Porygon',
	'Primeape',
	'Psyduck',
	'Raichu',
	'Rapidash',
	'Raticate',
	'Rattata',
	'Rhydon',
	'Rhyhorn',
	'Sandshrew',
	'Sandslash',
	'Scyther',
	'Seadra',
	'Seaking',
	'Seel',
	'Shellder',
	'Slowbro',
	'Slowpoke',
	'Snorlax',
	'Spearow',
	'Squirtle',
	'Starmie',
	'Staryu',
	'Tangela',
	'Tauros',
	'Tentacool',
	'Tentacruel',
	'Vaporeon',
	'Venomoth',
	'Venonat',
	'Venusaur',
	'Victreebel',
	'Vileplume',
	'Voltorb',
	'Vulpix',
	'Wartortle',
	'Weedle',
	'Weepinbell',
	'Weezing',
	'Wigglytuff',
	'Zapdos',
	'Zubat'
];

export async function POST({ request }: { request: Request }) {
	const reqBlob = await request.blob();

	console.log('test2');

	try {
		console.log('test3');
		const arrayBuffer = await reqBlob.arrayBuffer();

		// Convert ArrayBuffer to Uint8Array
		const uint8Array = new Uint8Array(arrayBuffer);

		console.log('test4');
		// Decode image into a tensor
		let imageTensor = tf.node.decodeImage(uint8Array, 3);

		console.log('test5');
		imageTensor = tf.image.resizeBilinear(imageTensor, [128, 128]);
		// imageTensor = imageTensor.div(255.0);
		console.log('test6');
		imageTensor = imageTensor.expandDims(0);

		console.log(imageTensor.shape);
		console.log(imageTensor);
		try {
			const model = await tf.loadLayersModel(modelUrl);
			console.log('Model loaded successfully');
			const prediction = model.predict(imageTensor);
			const best_pred = tf.argMax(prediction, 1).dataSync()[0];
			console.log(prediction); // Print the prediction
			console.log(pokemonArr[best_pred]);

			return new Response(pokemonArr[best_pred]);
		} catch (error) {
			console.error('Model failed to load: ', error);
		}
	} catch (error) {
		console.log(`${error}`);
	}

	return new Response('Prediction failed');
}


