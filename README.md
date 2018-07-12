# API REST Pokemon

This API is about Pokemons let us to retrieve datas from the following [website](https://pokemondb.net/pokedex/all) thanks to the [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) python library in order to store pokemon informations in a database so as to generate a CRUD with [Hug](https://github.com/timothycrosley/hug), a Python API development.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system

### Prerequisites

The architecture of the project folder is the following one : 

* api.py
* init.py
* initDB.py

After you retrieved the project files on your machine with 
a *git clone git@github.com:romain-renard/pokemon_project.git* (with ssh), you have to set up your apache and mySQL server.

Moreover, you will need [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/), [Hug](https://github.com/timothycrosley/hug), [Mysql Connector](https://pypi.org/project/mysql-connector-python/) and [Python 3.6.5](https://www.python.org/downloads/release/python-365/) to run the application.

### Installing

After the previous steps, you are ready to face of the future executing the *initDB.py* script which will completely create the database (which named *pokemon_project*) on your local server. It's configured by default on the root user without password.

```
cnx = mysql.connector.connect(user='root')
```

You are able to modify the line 11 in *initDB.py* file to change the connection to the database if it's necessary.

Now, the database is created and you just need to start the API server with the following command (always in the project folder) :

```
hug -f api.py
```

You should reach the application on this url : 
```
http://localhost:8000/
```

I imagine you want to test the API so you have to know there is a CRUD with the following actions : 

* /createPokemon
* /updatePokemon
* /deletePokemon

By default, the GET action is working on the root */*.
In order to be clear, this is an example to list all of the pokemons : 

```
http://localhost:8000/
```

If you want to add or update a pokemon you need to change the URL with the actions we saw before and you have to pass JSON datas to the API through the request thanks to a tool like [Postman](https://www.getpostman.com).

Here, an example of a valid JSON data-set for a create :


	{
 		"id": 918,
 		"label": "Pikachu",
 		"types": ["Eclair", "Fighting"]
 		"total": 100,
 		"hp": 100,
 		"attack": 100,
 		"defense": 100,
 		"speed_attack": 100,
 		"speed_defense": 100,
 		"speed": 100
	}
  
Here, an example of a valid JSON data-set for an update :

	{
		"id": 1,
		"id_pokemon": 100,
		"label": "Carapuce",
		"types": ["Poison", "Electric"],
		"total": 500,
		"hp": 500,
		"attack": 500,
		"defense": 500,
		"speed_attack": 500,
		"speed_defense": 100,
		"speed": 100
	}

And if you want to delete an entry :

```
http://localhost:8000/deletePokemon?id=1
```

## Built with

* [Hug](https://github.com/timothycrosley/hug) - The python API REST
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - The python library for pulling data out of HTML and XML files

## Authors

* **wotm** - *Initial work* - [wotm](https://github.com/wotm)

## Acknowledgments

* *Goats are really powerful !*
* *Gotta catch em' all !*
* *Never give up !*