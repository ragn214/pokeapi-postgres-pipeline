import os
import requests
import psycopg
import logging

number_of_records = 2 # can be changed to any number from 1 to 1351, which is the total number of pokemon in the PokeAPI

connection = None
cursor = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

try:

    url = "https://pokeapi.co/api/v2/pokemon?limit=20"  # Start with the first page of results
    results = []
    page_url = url

    page_count = 0

    # Fetch pages of results until we have enough records or there are no more pages
    while page_url and len(results) < number_of_records:
        response = requests.get(page_url, timeout=15)
        response.raise_for_status()

        data = response.json()

        page_count += 1
        results.extend(data['results'])

        logging.info("Fetched page %s: %s records, %s collected so far",
            page_count,
            len(data['results']),
            len(results)
        ) 

        page_url = data['next']
        
    results = results[:number_of_records]

    logging.info(
        "Collected %s Pokemon from %s pages",
        len(results),
        page_count
    )

    # Connect to PostgreSQL database
    connection = psycopg.connect(
        host="localhost",
        port=5433,
        dbname="de_project",
        user="postgres",
        password=os.environ["POSTGRES_PASSWORD"]
    )
    logging.info("Connected to PostgreSQL")
    cursor = connection.cursor()

    processed = 0
    inserted = 0
    skipped = 0

    # loop through the first n pokemon and get their details
    for pokemon in results:
        detail_response = requests.get(
            pokemon['url'], 
            timeout=15
        )

        detail_response.raise_for_status()

        detail_data = detail_response.json()

        pokemon_record = {
            'id': detail_data['id'],
            'name': detail_data['name'],
            'height': detail_data['height'],
            'weight': detail_data['weight']
        }

        # Insert the record into the database, ignoring duplicates
        cursor.execute(
            """
            INSERT INTO pokemon (id, name, height, weight)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            (
                pokemon_record["id"],
                pokemon_record["name"],
                pokemon_record["height"],
                pokemon_record["weight"]
            )
        )

        # Update the processing counters
        processed += 1
        if cursor.rowcount == 1:
            inserted += 1
        else:
            skipped += 1

        if processed % 10 == 0:
            logging.info(
                "Progress: %s Pokemon processed", 
                processed
            )

        for pokemon_type in detail_data['types']:
            slot = pokemon_type['slot']
            type_name = pokemon_type['type']['name']
            type_url = pokemon_type['type']['url']
            type_id = int(type_url.rstrip('/').split('/')[-1])

            cursor.execute(
                """
                INSERT INTO types (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    type_id,
                    type_name
                )
            )

            cursor.execute(
                """
                INSERT INTO pokemon_types (pokemon_id, type_id, slot)
                VALUES (%s, %s, %s)
                ON CONFLICT (pokemon_id, type_id) DO NOTHING
                """,
                (
                    pokemon_record["id"],
                    type_id,
                    slot
                )
            )

    connection.commit()

    logging.info(
    "Processed %s Pokémon: %s inserted, %s skipped",
    processed,
    inserted,
    skipped
    )

# Handle exceptions and ensure resources are cleaned up
except requests.exceptions.RequestException as error:
    logging.error("API error: %s", error)
    if connection is not None:
        connection.rollback()
    raise

except psycopg.Error as error:
    logging.error("Database error: %s", error)
    if connection is not None:
        connection.rollback()
    raise

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()

logging.info("Pipeline complete")