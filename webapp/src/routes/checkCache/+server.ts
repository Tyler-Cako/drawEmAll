import sqlite3 from 'sqlite3';


const db = new sqlite3.Database("../../lib/db/cache.db");

export async function GET({ request }: { request: Request }) {
    const pokemonName = request.headers.get('pokemon');

    const query = `SELECT * FROM POKEMON WHERE NAME == ${pokemonName}`;

    const statement = db.get(query);

    console.log(statement);

    if (statement) return statement;

    // Cache miss
    const pokemonReq = await fetch(`https://pokeapi.co/api/v2/pokemon/${currentPokemon}`);
    const pokemonJSON = await pokemonReq.json();

    console.log(pokemonJSON);

    return pokemonJSON;
}