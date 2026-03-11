from pymongo import MongoClient

# connexion
client = MongoClient("mongodb+srv://alertebenjamin1_db_user:Mongo123456@cluster0.riwg8o7.mongodb.net/")
db = client['mon_jeu_combat']

def reset_base():
    # on vide 
    db.personnages.drop()
    db.monstres.drop()
    db.scores.drop()


# Données initiales rééquilibrées
CHARACTERS = [
    {"name": "Paladin", "attack": 20, "defense": 12, "hp": 120},
    {"name": "Chevalier", "attack": 22, "defense": 10, "hp": 110},
    {"name": "Berserker", "attack": 28, "defense": 6, "hp": 90},
    {"name": "Archer", "attack": 25, "defense": 7, "hp": 85},
    {"name": "Sorcier", "attack": 30, "defense": 4, "hp": 75},
    {"name": "Guerrier", "attack": 24, "defense": 8, "hp": 100},
    {"name": "Moine", "attack": 22, "defense": 9, "hp": 95},
    {"name": "Voleur", "attack": 27, "defense": 5, "hp": 80},
    {"name": "Chasseur", "attack": 23, "defense": 8, "hp": 90},
    {"name": "Druide", "attack": 21, "defense": 9, "hp": 100}
]

MONSTERS = [
    {"name": "Gobelin", "attack": 18, "defense": 6, "hp": 150},
    {"name": "Orc", "attack": 22, "defense": 8, "hp": 180},
    {"name": "Dragon", "attack": 25, "defense": 12, "hp": 200},
    {"name": "Zombie", "attack": 20, "defense": 7, "hp": 160},
    {"name": "Troll", "attack": 23, "defense": 10, "hp": 190},
    {"name": "Spectre", "attack": 24, "defense": 6, "hp": 170},
    {"name": "Golem", "attack": 21, "defense": 14, "hp": 210},
    {"name": "Vampire", "attack": 26, "defense": 9, "hp": 175},
    {"name": "Loup-garou", "attack": 24, "defense": 8, "hp": 185},
    {"name": "Squelette", "attack": 19, "defense": 7, "hp": 155}
]


db.personnages.insert_many(CHARACTERS)
db.monstres.insert_many(MONSTERS)

print("Base de données prête !")

if __name__ == "__main__":
    reset_base()




