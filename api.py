#!usr/bin/python3

import hug
import mysql.connector


@hug.get('/', output=hug.output_format.json)
def pokemonList():
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="pokemon_project")
    cursor = conn.cursor()
    # list of all pokemons with theirs types
    cursor.execute("""SELECT p.pokemon_id , p.label, GROUP_CONCAT(tp.label SEPARATOR ', '), p.total, p.hp, p.attack, p.defense, p.speed_attack, p.speed_defense, p.speed FROM pokemon as p, type_pok as tp, pokemon_type as pt WHERE p.id = pt.pokemon_id AND pt.type_id = tp.id GROUP BY p.id""")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    pokemonList = []
    for pokemon in results:
        pokemonList.append(pokemon)

    return pokemonList


@hug.post('/createPokemon')
def createPokemon(body):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="pokemon_project")
    cursor = conn.cursor()

    # list of the pokemon and types datas
    pokemonDatas = []
    for attribute, value in body.items():
        pokemonDatas.append(value)

    # list of the pokemon infos
    pokemonParam = (pokemonDatas[0], pokemonDatas[1], pokemonDatas[3], pokemonDatas[4], pokemonDatas[5], pokemonDatas[6], pokemonDatas[7], pokemonDatas[8], pokemonDatas[9])

    typeListIds = []
    types = pokemonDatas[2]

    for i in range(0, len(types)):
        cursor.execute("""SELECT count(*) FROM type_pok WHERE label LIKE %s """, ("%" + types[i] + "%",))
        resultsCount = cursor.fetchone()[0]

        # if the type doesn't exists we store it in db
        if resultsCount == 0:
            cursor.execute("""INSERT INTO type_pok (label) VALUES (%s)""", [types[i]])
            typeListIds.append(cursor.lastrowid)

        # if the type is existing we retrieve its id
        else:
            cursor.execute("""SELECT id FROM type_pok WHERE label LIKE (%s)""", ("%" + types[i] + "%",))
            typeId = cursor.fetchone()[0]
            typeListIds.append(typeId)

    # add pokemon in db
    cursor.execute("""INSERT INTO pokemon (pokemon_id, label, total, hp, attack, defense, speed_attack, speed_defense, speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",pokemonParam)
    pokemonId = cursor.lastrowid

    # add pokemon/type relation in db
    for i in range(0, len(typeListIds)):
        cursor.execute("""INSERT INTO pokemon_type (type_id, pokemon_id) VALUES (%s, %s)""", (typeListIds[i], pokemonId))

    conn.commit()
    cursor.close()
    conn.close()


@hug.put('/updatePokemon')
def updatePokemon(body):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="pokemon_project")
    cursor = conn.cursor()

    # list of the pokemons infos to update
    pokemonDatas = []
    for attribute, value in body.items():
        pokemonDatas.append(value)

    # list of the pokemon infos
    pokemonParam = (pokemonDatas[1], pokemonDatas[2], pokemonDatas[4], pokemonDatas[5], pokemonDatas[6], pokemonDatas[7], pokemonDatas[8], pokemonDatas[9], pokemonDatas[10], pokemonDatas[0])

    typeListIds = []
    types = pokemonDatas[3]

    for i in range(0, len(types)):
        cursor.execute("""SELECT count(*) FROM type_pok WHERE label LIKE %s """, ("%" + types[i] + "%",))
        resultsCount = cursor.fetchone()[0]

        # if the type doesn't exists we store it in db
        if resultsCount == 0:
            cursor.execute("""INSERT INTO type_pok (label) VALUES (%s)""", [types[i]])
            typeListIds.append(cursor.lastrowid)

        # if the type is existing we retrieve its id
        else:
            cursor.execute("""SELECT id FROM type_pok WHERE label LIKE (%s)""", ("%" + types[i] + "%",))
            typeId = cursor.fetchone()[0]
            typeListIds.append(typeId)

    # update pokemon in db
    cursor.execute("""UPDATE pokemon SET pokemon_id = %s, label = %s, total = %s, hp =  %s, attack = %s, defense = %s, speed_attack = %s, speed_defense = %s, speed = %s WHERE id = %s""", pokemonParam)

    # check if type to update is the same as the one in db
    for i in range(0, len(typeListIds)):
        cursor.execute("""SELECT count(*) FROM pokemon_type WHERE type_id = %s AND pokemon_id = %s""", (typeListIds[i], pokemonDatas[0]))
        resultsCount = cursor.fetchone()[0]
        # we store it in db if it's a new one
        if resultsCount == 0:
            # update pokemon/type relation in db
            cursor.execute("""INSERT INTO pokemon_type (type_id, pokemon_id) VALUES (%s, %s)""", (typeListIds[i], pokemonDatas[0]))

    conn.commit()
    cursor.close()
    conn.close()

@hug.delete('/deletePokemon')
def deletePokemon(id):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="pokemon_project")
    cursor = conn.cursor()
    # deleting pokemon from the db with the id
    cursor.execute("""DELETE FROM pokemon WHERE id = %s""", (id,))
    conn.commit()
    cursor.close()
    conn.close()


