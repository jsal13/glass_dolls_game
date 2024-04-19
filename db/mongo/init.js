db = new Mongo().getDB("glassdolls");

db.createCollection('factions', { capped: false });
db.createCollection('puzzles', { capped: false });
