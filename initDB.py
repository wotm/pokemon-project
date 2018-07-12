#!usr/bin/python3

from __future__ import print_function
from mysql.connector import errorcode
import mysql.connector


DB_NAME = 'pokemon_project'
TABLES = {}

cnx = mysql.connector.connect(user='root')
cursor = cnx.cursor()

# Store tables in a dictionary
TABLES['pokemon'] = (
    "CREATE TABLE `pokemon` ("
    "`id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
    "`pokemon_id` INT(3) NOT NULL ,"
    "`label` VARCHAR(100) NOT NULL,"
    "`total` INT(3) NOT NULL,"
    "`hp` INT(3) NOT NULL,"
    "`attack` INT(3) NOT NULL,"
    "`defense` INT(3) NOT NULL,"
    "`speed_attack` INT(3) NOT NULL,"
    "`speed_defense` INT(3) NOT NULL,"    
    "`speed` INT(3) NOT NULL"
    ")")

TABLES['type_pok'] = (
    "CREATE TABLE `type_pok` ("
    "`id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
    "`label` VARCHAR(100) NOT NULL"
    ")")

TABLES['pokemon_type'] = (
    "CREATE TABLE `pokemon_type` ("
    "`type_id` INT  NOT NULL,"
    "`pokemon_id` INT NOT NULL,"
    "PRIMARY KEY (`type_id`, `pokemon_id`),"
    "FOREIGN KEY(`type_id`) REFERENCES `type_pok`(`id`) ON DELETE CASCADE,"
    "FOREIGN KEY(`pokemon_id`) REFERENCES `pokemon`(`id`) ON DELETE CASCADE"
    ")")


# Creating database
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

# Connection to the database
def connect_database():
    try:
        cnx.database = DB_NAME
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

# Creation of the tables from the dictionary
def create_tables():
    # erasing all of the datas in case of refreshing page
    cursor.execute("""SET FOREIGN_KEY_CHECKS=0""")
    cursor.execute("""TRUNCATE TABLE pokemon""")
    cursor.execute("""TRUNCATE TABLE type_pok""")
    cursor.execute("""TRUNCATE TABLE pokemon_type""")
    cursor.execute("""SET FOREIGN_KEY_CHECKS=1""")

    for name, ddl in TABLES.items():
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
                print(err.msg)
        else:
            print("OK")
    cursor.close()
    cnx.close()