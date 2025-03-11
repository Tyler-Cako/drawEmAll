import tf from '@tensorflow/tfjs-node';
import path from 'path';
import { fileURLToPath } from 'url';

// Manually define __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const modelPath = path.resolve(__dirname, 'well_trained_model/model.json');
const modelUrl = `file://${modelPath}`;

//ill move this later
const indexToPokemon = {
	0: 'Abra',
	1: 'Aerodactyl',
	2: 'Alakazam',
	3: 'Arbok',
	4: 'Arcanine',
	5: 'Articuno',
	6: 'Beedrill',
	7: 'Bellsprout',
	8: 'Blastoise',
	9: 'Bulbasaur',
	10: 'Butterfree',
	11: 'Caterpie',
	12: 'Chansey',
	13: 'Charizard',
	14: 'Charmander',
	15: 'Charmeleon',
	16: 'Clefable',
	17: 'Clefairy',
	18: 'Cloyster',
	19: 'Cubone',
	20: 'Dewgong',
	21: 'Diglett',
	22: 'Ditto',
	23: 'Dodrio',
	24: 'Doduo',
	25: 'Dragonair',
	26: 'Dragonite',
	27: 'Dratini',
	28: 'Drowzee',
	29: 'Dugtrio',
	30: 'Eevee',
	31: 'Ekans',
	32: 'Electabuzz',
	33: 'Electrode',
	34: 'Exeggcute',
	35: 'Exeggutor',
	36: 'Farfetchd',
	37: 'Fearow',
	38: 'Flareon',
	39: 'Gastly',
	40: 'Gengar',
	41: 'Geodude',
	42: 'Gloom',
	43: 'Golbat',
	44: 'Goldeen',
	45: 'Golduck',
	46: 'Graveler',
	47: 'Grimer',
	48: 'Growlithe',
	49: 'Gyarados',
	50: 'Haunter',
	51: 'Hitmonchan',
	52: 'Hitmonlee',
	53: 'Horsea',
	54: 'Hypno',
	55: 'Ivysaur',
	56: 'Jigglypuff',
	57: 'Jolteon',
	58: 'Jynx',
	59: 'Kabutops',
	60: 'Kadabra',
	61: 'Kakuna',
	62: 'Kangaskhan',
	63: 'Kingler',
	64: 'Koffing',
	65: 'Lapras',
	66: 'Lickitung',
	67: 'Machamp',
	68: 'Machoke',
	69: 'Machop',
	70: 'Magikarp',
	71: 'Magmar',
	72: 'Magnemite',
	73: 'Magneton',
	74: 'Mankey',
	75: 'Marowak',
	76: 'Meowth',
	77: 'Metapod',
	78: 'Mew',
	79: 'Mewtwo',
	80: 'Moltres',
	81: 'MrMime',
	82: 'Nidoking',
	83: 'Nidoqueen',
	84: 'Nidorina',
	85: 'Nidorino',
	86: 'Ninetales',
	87: 'Oddish',
	88: 'Omanyte',
	89: 'Omastar',
	90: 'Parasect',
	91: 'Pidgeot',
	92: 'Pidgeotto',
	93: 'Pidgey',
	94: 'Pikachu',
	95: 'Pinsir',
	96: 'Poliwag',
	97: 'Poliwhirl',
	98: 'Poliwrath',
	99: 'Ponyta',
	100: 'Porygon',
	101: 'Primeape',
	102: 'Psyduck',
	103: 'Raichu',
	104: 'Rapidash',
	105: 'Raticate',
	106: 'Rattata',
	107: 'Rhydon',
	108: 'Rhyhorn',
	109: 'Sandshrew',
	110: 'Sandslash',
	111: 'Scyther',
	112: 'Seadra',
	113: 'Seaking',
	114: 'Seel',
	115: 'Shellder',
	116: 'Slowbro',
	117: 'Slowpoke',
	118: 'Snorlax',
	119: 'Spearow',
	120: 'Squirtle',
	121: 'Starmie',
	122: 'Staryu',
	123: 'Tangela',
	124: 'Tauros',
	125: 'Tentacool',
	126: 'Tentacruel',
	127: 'Vaporeon',
	128: 'Venomoth',
	129: 'Venonat',
	130: 'Venusaur',
	131: 'Victreebel',
	132: 'Vileplume',
	133: 'Voltorb',
	134: 'Vulpix',
	135: 'Wartortle',
	136: 'Weedle',
	137: 'Weepinbell',
	138: 'Weezing',
	139: 'Wigglytuff',
	140: 'Zapdos',
	141: 'Zubat'
};

export async function POST({ request }: { request: Request }) {
	let postRes = new Response();

	const reqBlob = await request.blob();

	try {
		const arrayBuffer = await reqBlob.arrayBuffer();

		// Convert ArrayBuffer to Uint8Array
		const uint8Array = new Uint8Array(arrayBuffer);

		// Decode image into a tensor
		let imageTensor = tf.node.decodeImage(uint8Array, 3);

		imageTensor = tf.image.resizeBilinear(imageTensor, [128, 128]);
		// imageTensor = imageTensor.div(255.0);
		imageTensor = imageTensor.expandDims(0);

		console.log(imageTensor.shape);
		console.log(imageTensor);
		try {
			let model;
			model = await tf.loadLayersModel(modelUrl);
			console.log('Model loaded successfully');
			// model.summary();
			const prediction = model.predict(imageTensor);
			let best_pred = tf.argMax(prediction, 1).dataSync()[0];
			console.log(prediction); // Print the prediction
			console.log(indexToPokemon[best_pred]);
		} catch (error) {
			console.error('Model failed to load: ', error);
		}

		// const response = await fetch('http://localhost:7071/api/predict_pokemon', {
		// 	method: 'POST',
		// 	body: reqBlob
		// });

		// if (response.ok) {
		// 	return response;
		// } else {
		// 	throw new Error(response.toString());
		// }
	} catch (error) {
		console.log(`${error}`);
	}

	return postRes;
}

// let model;
// (async function loadModel() {
//     try {
//         model = await tf.loadLayersModel('this_one_is_good/model.json'); // No 'file://' prefix needed in the browser
//         console.log("Model loaded successfully");
//         model.summary(); // No need for console.log()
//     } catch (error) {
//         console.error("Model failed to load: ", error);
//     }
// })();
