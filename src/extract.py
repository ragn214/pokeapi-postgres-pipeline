import os
import requests
import psycopg

# url = "https://pokeapi.co/api/v2/pokemon/clodsire" ### print the data for a specific pokemon
url = "https://pokeapi.co/api/v2/pokemon"  ### print the data for all pokemon


response = requests.get(url,params={'limit': 1351}) 
print(response.status_code)

data = response.json()

results = data['results'][:5]  ### print the first 5 pokemon
print(f"Fetched {len(results)} Pokémon")

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
            pokemon_record['id'],
            pokemon_record['name'],
            pokemon_record['height'],
            pokemon_record['weight']
        )
    )

print("Committing changes...")
connection.commit()

cursor.close()
connection.close()
print("Pipeline complete")

####### print some data from the API
# print(data.keys())
# print(data['results'][-1])
# print(len(data['results']))  ### length is 1351
# print(data['name'])
# print(data['height'])
# print(data['weight'])
# print(data['abilities'][0]['ability']['name'])
# print(data['id'])
# print(data['types'])