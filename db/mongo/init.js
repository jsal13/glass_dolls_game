db = new Mongo().getDB("glassdolls");

db.createCollection('factions', { capped: false });
