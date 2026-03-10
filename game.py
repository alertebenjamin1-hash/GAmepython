import random
from db_init import MONSTERS


class Game:
    """Gère la logique du jeu et les combats"""
    
    def __init__(self, db, player_name):
        self.db = db
        self.player_name = player_name
        self.team = []
        self.waves = 0
        
    def create_team(self):
        """Permet au joueur de créer son équipe"""
        from utils import clear_screen, print_header, get_valid_input
        
        characters = self.db['characters'].find()
        characters_list = list(characters)
        
        clear_screen()
        print_header("Création de l'équipe")
        print("Sélectionnez 3 personnages pour votre équipe\n")
        
        team = []
        selected_indices = set()
        
        for slot in range(1, 4):
            clear_screen()
            print_header(f"Sélection personnage {slot}/3")
            
            # Afficher les personnages disponibles
            print("Personnages disponibles:")
            for i, char in enumerate(characters_list):
                status = "(SÉLECTIONNÉ)" if i in selected_indices else ""
                print(f"{i+1}. {char['name']} - ATK: {char['attack']}, DEF: {char['defense']}, PV: {char['hp']} {status}")
            
            print("\nEquipe actuelle:")
            for i, member in enumerate(team, 1):
                print(f"{i}. {member['name']} - ATK: {member['attack']}, DEF: {member['defense']}, PV: {member['hp']}")
            
            choice = get_valid_input(f"\nChoisissez un personnage (1-{len(characters_list)}): ", input_type=int, min_val=1, max_val=len(characters_list))
            choice_index = choice - 1
            
            if choice_index in selected_indices:
                print("Ce personnage est déjà sélectionné!")
                slot -= 1
                input("Appuyez sur Entrée...")
            else:
                selected_indices.add(choice_index)
                character = characters_list[choice_index].copy()
                character['current_hp'] = character['hp']
                team.append(character)
        
        self.team = team
    
    def lancer_le_jeu(self):
        # On récupère les monstres simplement
        liste_monstres = list(self.db['monsters'].find())
        
        # Tant qu'on a au moins un perso vivant dans l'équipe
        while len(self.team) > 0:
            self.waves = self.waves + 1 # On avance d'une vague
            
            # On pioche un monstre au pif
            monstre_actuel = random.choice(liste_monstres).copy()
            pv_monstre = monstre_actuel['hp']
            
            print(f"\n--- VAGUE {self.waves} ---")
            print(f"Vous affrontez : {monstre_actuel['name']} (PV: {pv_monstre})")

            # La bagarre continue tant que le monstre et l'équipe sont en vie
            while pv_monstre > 0 and len(self.team) > 0:
                input("\nAppuyez sur Entrée pour attaquer...")

                # 1. CHAQUE PERSO DE L'EQUIPE ATTAQUE
                for perso in self.team:
                    if pv_monstre > 0:
                        # Calcul tout simple : Attaque moins Defense
                        degats = perso['attack'] - monstre_actuel['defense']
                        if degats < 1: degats = 1 # On fait au moins 1 de dégât
                        
                        pv_monstre = pv_monstre - degats
                        print(f"{perso['name']} tape le monstre ! Il reste {pv_monstre} PV au monstre.")

                # 2. LE MONSTRE REPOND (s'il est encore vivant)
                if pv_monstre > 0:
                    # Il choisit quelqu'un au hasard dans l'équipe
                    cible = random.choice(self.team)
                    degats_monstre = monstre_actuel['attack'] - cible['defense']
                    if degats_monstre < 1: degats_monstre = 1
                    
                    cible['hp'] = cible['hp'] - degats_monstre
                    print(f"Le monstre attaque {cible['name']} ! Il lui reste {cible['hp']} PV.")

                    # Si le perso meurt, on l'enlève de la liste
                    if cible['hp'] <= 0:
                        print(f"DOMMAGE : {cible['name']} est mort...")
                        self.team.remove(cible)

            if pv_monstre <= 0:
                print("Bien joué ! Monstre mort.")
            else:
                print("GAME OVER... Vous avez perdu.")

        # Quand c'est fini, on enregistre le score
        self.db['scores'].insert_one({
            'nom': self.player_name,
            'vagues': self.waves - 1
        })
        print(f"Score enregistré : {self.waves - 1} vagues.")