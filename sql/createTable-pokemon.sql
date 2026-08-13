CREATE TABLE pokemon (
	id INTEGER PRIMARY KEY,
	name VARCHAR(100),
	height INTEGER,
	weight INTEGER
);

SELECT * FROM pokemon
ORDER BY id;

BEGIN;

INSERT INTO pokemon (id, name, height, weight)
VALUES (6, 'test-pokemon', 10, 10);

INSERT INTO pokemon (id, name, height, weight)
VALUES (1, 'duplicate', 10, 10);

ROLLBACK;

DELETE FROM pokemon
WHERE id > 5;

SELECT COUNT(*)
FROM pokemon;

SELECT id, name
FROM pokemon
ORDER BY id;