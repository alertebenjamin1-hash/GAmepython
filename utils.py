import os


def clear_screen():
    """Efface l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(text):
    """Affiche un titre formaté"""
    print("\n" + "=" * 50)
    print(text.center(50))
    print("=" * 50 + "\n")


def get_valid_input(prompt, input_type=str, min_val=None, max_val=None):
    """Récupère une entrée valide de l'utilisateur"""
    while True:
        try:
            user_input = input(prompt)
            
            if input_type == int:
                value = int(user_input)
                if min_val is not None and value < min_val:
                    print(f"La valeur doit être au minimum {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"La valeur doit être au maximum {max_val}")
                    continue
                return value
            elif input_type == str:
                if not user_input.strip():
                    print("Veuillez entrer une valeur")
                    continue
                return user_input.strip()
        except ValueError:
            print("Entrée invalide. Veuillez réessayer.")


def ask_player_name():
    """Demande le nom du joueur"""
    return get_valid_input("Entrez votre nom de joueur : ", input_type=str)


def print_scores(scores):
    """Affiche les meilleurs scores"""
    print_header("Meilleurs Scores")
    if not scores:
        print("Aucun score enregistré")
        return
    
    for i, score in enumerate(scores, 1):
        print(f"{i}. {score['player_name']} - {score['waves']} vagues")
    print()
