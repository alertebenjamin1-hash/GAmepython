import os
from pymongo import MongoClient
from game import Game
from utils import clear_screen, print_header, print_scores, get_valid_input, ask_player_name


def main_menu()
    
     try:
        while True:
            clear_screen()
            print_header("Jeu de Combat")
            print("1. Démarrer une nouvelle partie")
            print("2. Voir les meilleurs scores")
            print("3. Quitter")

              if choice == "1":
                clear_screen()
                print_header("Nouvelle Partie")

                name = ask_player_name()
                game.player_name = name

                # Création de l'équipe
                game.create_team()

                # Lancement du jeu
                game.play()