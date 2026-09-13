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

SELECT
	p.id,
	p.name,
	COUNT(pt.type_id) AS type_count
FROM pokemon p
JOIN pokemon_types pt
	ON p.id = pt.pokemon_id
GROUP BY p.id, p.name
HAVING COUNT(pt.type_id) = 2
ORDER BY p.id;

SELECT
	t.name,
	COUNT(pt.pokemon_id) AS pokemon_count
FROM types t
JOIN pokemon_types as pt
	ON t.id = pt.type_id
WHERE pt.slot = 1
GROUP BY t.name
HAVING COUNT(pt.pokemon_id) >= 3
ORDER BY pokemon_count DESC;

select *
from pokemon_types;

	