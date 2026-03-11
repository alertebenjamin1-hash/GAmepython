from pymongo import MongoClient
from db_init import db
from models import Combattant
from game import lancer_combat


def afficher_classement():
    print("\n---Top 3 SCORES ---")
    #on trie par vagues decroissantes (-1) et on limite aux 3 premiers
    scores = list(db.scores.find().sort("vagues", -1).limit(3))
    
    if not scores:
        print("Aucun score pour le moment. Soyez le premier !")
    else:
        for i, s in enumerate(scores, 1):
            print(f"{i}. {s['joueur']} - {s['vagues']} vagues")


def jouer():
    nom_joueur = input("Ton nom de guerrier : ")

    #recuperer les persos de la db
    persos_db = list(db.personnages.find())
    print("\nChoisissez 3 personnages :")
    # On affiche la liste avec les stats pour que le joueur puisse choisir
    for i, p in enumerate(persos_db):
        print(f"{i}- {p['name']} (ATK:{p['attack']} DEF:{p['defense']} PV:{p['hp']})")

    equipe = []
    indices_choisis = []

    # Boucle pour s'assurer que le joueur prend exactement 3 persos différents
    while len(equipe) < 3:
        try:
            choix = int(input(f"Numéro du perso {len(equipe)+1} : "))
            if choix not in indices_choisis and 0 <= choix < len(persos_db):
                p = persos_db[choix]
                equipe.append(Combattant(p['name'], p['attack'], p['defense'], p['hp']))
                indices_choisis.append(choix)
            else:
                print("Choix invalide ou déjà pris.")
        except ValueError:
            print("Entre un chiffre !")

    # On récupère la liste des monstres pour le combat
    monstres_db = list(db.monstres.find())

    # On lance le combat infini et on récupère le nombre de vagues atteint
    score_final = lancer_combat(equipe, monstres_db)

    # Sauvegarder
    db.scores.insert_one({"joueur": nom_joueur, "vagues": score_final})
    print(f"\nPartie finie ! Tu as survécu à {score_final} vagues.")
    afficher_classement()

# Menu Principal
if __name__ == "__main__":
    while True:
        print("\n=== MENU JEU VIDEO ===")
        print("1. Jouer")
        print("2. Voir le classement")
        print("3. Quitter")
        choix = input("Votre choix : ")

        if choix == "1": 
            jouer()
        elif choix == "2": 
            afficher_classement()
        elif choix == "3": 
            break

        else:
            print("Choix non reconnu, reessayer.")