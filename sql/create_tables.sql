CREATE TABLE pokemon (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    height INTEGER,
    weight INTEGER
);

CREATE TABLE types (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE pokemon_types (
    pokemon_id INTEGER,
    type_id INTEGER,
    slot INTEGER NOT NULL,

    PRIMARY KEY (pokemon_id, type_id),

    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY (type_id) REFERENCES types(id)
);