import unittest
import sqlite3
import json
import os
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    print(path)
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# Creates list of species ID's and numbers
def create_species_table(cur, conn):

    species = ["Rabbit",
    "Dog",
    "Cat",
    "Boa Constrictor",
    "Chinchilla",
    "Hamster",
    "Cobra",
    "Parrot",
    "Shark",
    "Goldfish",
    "Gerbil",
    "Llama",
    "Hare"
    ]

    cur.execute("DROP TABLE IF EXISTS Species")
    cur.execute("CREATE TABLE Species (id INTEGER PRIMARY KEY, title TEXT)")
    for i in range(len(species)):
        cur.execute("INSERT INTO Species (id,title) VALUES (?,?)",(i,species[i]))
    conn.commit()

# TASK 1
# CREATE TABLE FOR PATIENTS IN DATABASE
def create_patients_table(cur, conn):
    cur.execute('drop table if exists Patients')
    cur.execute('create table Patients (pet_id INTEGER PRIMARY KEY, name TEXT, species_id INTEGER, age INTEGER, cuteness INTEGER, aggressivity INTEGER)')
    conn.commit()


# ADD FLUFFLE TO THE TABLE
def add_fluffle(cur, conn):
    cur.execute('insert into Patients(pet_id, name, species_id, age, cuteness, aggressivity) values(?, ?, ?, ?, ?, ?)', (0, "fluffle", 0, 3, 90, 100))
    conn.commit()
    

# TASK 2
# CODE TO ADD JSON TO THE TABLE
# ASSUME TABLE ALREADY EXISTS
def add_pets_from_json(filename, cur, conn):
    
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(filename)
    file_data = f.read()
    f.close()
    pets = json.loads(file_data)

    # THE REST IS UP TO YOU
    for pet in pets:
        res = cur.execute('SELECT id FROM Species WHERE title = ?', (pet['species'],))
        id = res.fetchone()[0]
        cur.execute('INSERT INTO Patients(name, species_id, age, cuteness, aggressivity) VALUES(?, ?, ?, ?, ?)', 
            (
            pet['name'], 
            id, 
            pet['age'], 
            pet['cuteness'], 
            pet['aggressiveness']
            )
        )
        conn.commit()

# TASK 3
# CODE TO OUTPUT NON-AGGRESSIVE PETS
def non_aggressive_pets(aggressiveness, cur, conn):
    res = cur.execute('SELECT name FROM Patients WHERE aggressivity <= ?', (aggressiveness,))
    conn.commit()
    return list(res)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('animal_hospital.db')
    create_species_table(cur, conn)

    create_patients_table(cur, conn)
    add_fluffle(cur, conn)
    add_pets_from_json('pets.json', cur, conn)
    ls = (non_aggressive_pets(10, cur, conn))
    print(ls)
    
    
if __name__ == "__main__":
    main()

