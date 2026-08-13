import os
import requests
import psycopg
import logging

number_of_records = 50 # can be changed to any number from 1 to 1351, which is the total number of pokemon in the PokeAPI

connection = None
cursor = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

try:
    # Fetch data from the PokeAPI
    url = "https://pokeapi.co/api/v2/pokemon"  
    response = requests.get(url,params={'limit': 1351}, timeout=15) 
    # print(response.status_code)
    response.raise_for_status()
    data = response.json()
    results = data['results'][:number_of_records]  
    logging.info("Fetched %s pokemon from PokeAPI", len(results))

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
        
    connection.commit()

    logging.info(
    "Processed %s Pokémon: %s inserted, %s skipped",
    processed,
    inserted,
    skipped
    )

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