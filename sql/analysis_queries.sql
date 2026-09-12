SELECT *
FROM pokemon
ORDER BY id;

SELECT *
FROM types
ORDER BY id;

SELECT *
FROM pokemon_types
ORDER BY pokemon_id;

SELECT COUNT(*)
FROM pokemon;

SELECT COUNT(*)
FROM types;

SELECT COUNT(*)
FROM pokemon_types;

SELECT
    pokemon.name,
    types.name,
    pokemon_types.slot
FROM pokemon
JOIN pokemon_types
    ON pokemon.id = pokemon_types.pokemon_id
JOIN types
    ON pokemon_types.type_id = types.id
ORDER BY pokemon.id, pokemon_types.slot;

SELECT
    t.name,
    COUNT(p.id) AS pokemon_count
FROM pokemon p
JOIN pokemon_types pt
    ON p.id = pt.pokemon_id
JOIN types t
    ON pt.type_id = t.id
GROUP BY t.name
HAVING COUNT(p.id) >= 5
ORDER BY pokemon_count DESC, t.name ASC;
