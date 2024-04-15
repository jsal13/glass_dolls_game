CREATE TABLE spells (
    id SERIAL PRIMARY KEY,
    spell VARCHAR,
    syllables VARCHAR
);

CREATE TABLE puzzles (
    id SERIAL PRIMARY KEY,
    content VARCHAR,
    solution VARCHAR
);