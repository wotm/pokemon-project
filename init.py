#!usr/bin/python3

from bs4 import BeautifulSoup
import requests
import initDB
import mysql.connector
import re

initDB.connect_database()
initDB.create_tables()

url = "https://pokemondb.net/pokedex/all"

conn = mysql.connector.connect(host="localhost",user="root",password="", database="pokemon_project")
cursor = conn.cursor()

response = requests.get(url)
html = str(response.content)
soup = BeautifulSoup(html, "html.parser")

tab = soup.find(id="pokedex")

# parser HTML
for currentTR in tab.find_all("tr"):
    pokemon = []
    for currentTD in currentTR.find_all("td"):
        pokemon.append(currentTD.text)

    pokemonParam = []
    # to avoid an out of range
    if len(pokemon) == 10:
        pokemonParam = (pokemon[0], pokemon[1], pokemon[3], pokemon[4], pokemon[5], pokemon[6], pokemon[7], pokemon[8], pokemon[9])
        # retrieving each type which begins with an uppercase letter
        pokemonTypes = re.findall('[A-Z][^A-Z]*', pokemon[2])


        typeListIds = []
        for i in range(0, len(pokemonTypes)):
            cursor.execute("""SELECT count(*) FROM type_pok WHERE label LIKE %s """, ("%" + pokemonTypes[i] + "%",))
            resultsCount = cursor.fetchone()[0]

            # if the type doesn't exists we store it in db
            if resultsCount == 0:
                cursor.execute("""INSERT INTO type_pok (label) VALUES (%s)""", [pokemonTypes[i]])
                typeListIds.append(cursor.lastrowid)

            # if the type is existing we retrieve its id
            else:
                cursor.execute("""SELECT id FROM type_pok WHERE label LIKE (%s)""", ("%" + pokemonTypes[i] + "%",))
                typeId = cursor.fetchone()[0]
                typeListIds.append(typeId)

        # add pokemon in db
        cursor.execute("""INSERT INTO pokemon (pokemon_id, label, total, hp, attack, defense, speed_attack, speed_defense, speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", pokemonParam)
        pokemonId = cursor.lastrowid

        # add pokemon/type relation in db
        for i in range(0, len(typeListIds)):
            cursor.execute("""INSERT INTO pokemon_type (type_id, pokemon_id) VALUES (%s, %s)""", (typeListIds[i], pokemonId))

conn.commit()
cursor.close()
conn.close()
