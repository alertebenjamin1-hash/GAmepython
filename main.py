import os
from pymongo import MongoClient
from game import Game
# On importe les outils dont on a besoin depuis utils.py
from utils import clear_screen, print_header, get_valid_input

def main():
   # 1. L'adresse de ta base de données (l'URI)
    URI = "mongodb+srv://alertebenjamin1_db_user:Mongo123456@cluster0.riwg8o7.mongodb.net/?appName=Cluster0"
    
    # 2. Création du client MongoDB
    client = MongoClient(URI)

     # Sélection de la base de données
    db = client['jeu_combat_db']
     # Cette boucle permet d'afficher le menu tant que le joueur
    while True:
        clear_screen()
        print_header("MENU PRINCIPAL - JEU DE COMBAT")
        print("1. Démarrer une nouvelle partie")
        print("2. Voir les meilleurs scores")
        print("3. Quitter")
        
        choix = input("\nfaite un choix (1, 2 ou 3) : ")

        # Le joueur saisit son nom, crée son équipe,
        # puis le combat infini peut commencer.

        if choix == "1":
            clear_screen()
            print_header("NOUVELLE PARTIE")

            # Saisie du nom du joueur
            nom = input("Entrez votre nom de guerrier : ")
            
            # On crée l'objet Game avec la base de données et le nom
            mon_jeu = Game(db, nom)
            
            # Choisir les persos
            mon_jeu.create_team()
            
            # Lancer le jeu
            mon_jeu.lancer_le_jeu()
            
            input("\nPartie terminée ! Appuyez sur Entrée pour revenir au menu...")
            # AFFICHER LE CLASSEMENT
        elif choix == "2":
            clear_screen()
            print_header("MEILLEURS SCORES")
            # On va chercher les 3 meilleurs dans la base
            scores = list(db['scores'].find().sort('vagues', -1).limit(3))
            
            for s in scores:
                print(f"- {s['nom']} : {s['vagues']} vagues survécues")
            
            input("\nAppuyez sur Entrée pour quitter...")
       
        # Fin propre du programme.

        elif choix == "3":
            print("Merci d'avoir joué ! À bientôt.")
            break
       
# C'est ce qui lance tout le programme
if __name__ == "__main__":
    main()