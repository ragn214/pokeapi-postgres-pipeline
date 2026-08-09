import os
import requests
import psycopg

# Fetch data from the PokeAPI
url = "https://pokeapi.co/api/v2/pokemon"  
response = requests.get(url,params={'limit': 1351}) 
print(response.status_code)
data = response.json()
results = data['results'][:5]  
print(f"Fetched {len(results)} Pokémon")

connection = None
cursor = None

try:
    # Connect to PostgreSQL database
    connection = psycopg.connect(
        host="localhost",
        port=5433,
        dbname="de_project",
        user="postgres",
        password=os.environ["POSTGRES_PASSWORD"]
    )
    print("Connected to PostgreSQL")
    cursor = connection.cursor()

    # loop through the first 5 pokemon and get their details
    for pokemon in results:
        detail_response = requests.get(pokemon['url'])
        detail_data = detail_response.json()

        pokemon_record = {
            'id': detail_data['id'],
            'name': detail_data['name'],
            'height': detail_data['height'],
            'weight': detail_data['weight']
        }
        print(pokemon_record)

        cursor.execute(
            """
            INSERT INTO pokemon (id, name, height, weight)
            VALUES (%s, %s, %s, %s)
            """,
            (
                pokemon_record["id"],
                pokemon_record["name"],
                pokemon_record["height"],
                pokemon_record["weight"]
            )
        )

    print("Committing changes...")
    connection.commit()

except psycopg.Error as error:
    print(f"Database error: {error}")
    if connection is not None:
        connection.rollback()
    raise

finally:
    if cursor is not None:
        cursor.close()
        print("Cursor closed")
    if connection is not None:
        connection.close()
        print("Connection closed")

print("Pipeline complete")