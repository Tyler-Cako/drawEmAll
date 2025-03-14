const tf = require("@tensorflow/tfjs-node");
const http = require('http');

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

let model;

// Load the model
(async () => {
  const modelUrl = `file://normalized_model_54299/model.json`;
  model = await tf.loadLayersModel(modelUrl);
  console.log("Model loaded successfully.");
})();

const server = http.createServer(async (req, res) => {
  if (req.method === "POST" && req.url === "/predict") {
    let chunks = [];
    req.on("data", chunk => {
        chunks.push(chunk);
    });

    req.on("end", async () => {
      try {
        // Combinate chunks
        const buffer = Buffer.concat(chunks);
    
        // Convert buffer to Uint8Array
        const uint8Array = new Uint8Array(buffer);
    
        // Decode image into a tensor
        let imageTensor = tf.node.decodeImage(uint8Array, 3);
    
        imageTensor = tf.image.resizeBilinear(imageTensor, [128, 128]);
        imageTensor = imageTensor.div(255.0);
    
        imageTensor = imageTensor.expandDims(0);
    
        const prediction = model.predict(imageTensor);
        const best_pred = tf.argMax(prediction, 1).dataSync()[0];
  
        console.log(pokemonArr[best_pred]);
  
        res.writeHead(200, { "Content-Type": "text/plain" });
        res.end(pokemonArr[best_pred]);

        return;

      } catch (error) {
        res.writeHead(400, { "Content-Type": "text/plain" });
        res.end("Error");
        console.log(`${error}`);
      }
    });
    
    } else {
        res.writeHead(404, { "Content-Type": "text/plain" });
        res.end("Not Found");
    }
});


const PORT = 3000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
