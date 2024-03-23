db = new Mongo().getDB("glassdolls");

db.createCollection('phrases', { capped: false });
ff