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
    
    def play(self):
        """Lance la boucle de combat"""
        from utils import clear_screen, print_header, get_valid_input
        
        clear_screen()
        print_header(f"Combat - {self.player_name}")
        
        while True:
            monster = self.get_random_monster()
            monster['current_hp'] = monster['hp']
            
            clear_screen()
            print_header(f"Vague {self.waves + 1}")
            print(f"Un {monster['name']} apparaît!")
            print(f"PV: {monster['current_hp']}, ATK: {monster['attack']}, DEF: {monster['defense']}\n")
            
            input("Appuyez sur Entrée pour combattre...")
            
            defeated = self.fight(monster)
            
            if defeated:
                print(f"\nVous avez survécu {self.waves} vagues!")
                self.save_score()
                return
            else:
                self.waves += 1
                input("\nVictoire! Appuyez sur Entrée pour la prochaine vague...")
    
    def fight(self, monster):
        """Gère un combat complet"""
        from utils import clear_screen
        
        while True:
            clear_screen()
            print(f"=== Combat Vague {self.waves + 1} ===\n")
            
            print("Votre équipe:")
            for char in self.team:
                print(f"  {char['name']} - PV: {char['current_hp']}/{char['hp']}")
            
            print(f"\n{monster['name']} - PV: {monster['current_hp']}/{monster['hp']}\n")
            
            # Les personnages attaquent
            for char in self.team:
                damage = self.calculate_damage(char['attack'], monster['defense'])
                monster['current_hp'] -= damage
                print(f"{char['name']} attaque! Dégâts: {damage}")
            
            if monster['current_hp'] <= 0:
                print(f"\n{monster['name']} est vaincu!")
                return False
            
            input("\nAppuyez sur Entrée...")
            clear_screen()
            print(f"=== Combat Vague {self.waves + 1} ===\n")
            print("Votre équipe:")
            for char in self.team:
                print(f"  {char['name']} - PV: {char['current_hp']}/{char['hp']}")
            print(f"\n{monster['name']} - PV: {monster['current_hp']}/{monster['hp']}\n")
            
            # Le monstre attaque
            target = random.choice(self.team)
            damage = self.calculate_damage(monster['attack'], target['defense'])
            target['current_hp'] -= damage
            print(f"{monster['name']} attaque {target['name']}! Dégâts: {damage}")
            
            if all(char['current_hp'] <= 0 for char in self.team):
                print("\nVotre équipe est vaincue!")
                return True
            
            input("\nAppuyez sur Entrée...")
    
    def calculate_damage(self, attack, defense):
        """Calcule les dégâts"""
        damage = attack - defense
        if damage < 1:
            damage = 1
        variation = random.randint(-2, 2)
        damage = max(1, damage + variation)
        return damage
    
    def get_random_monster(self):
        """Retourne un monstre aléatoire"""
        return random.choice(MONSTERS).copy()
    
    def save_score(self):
        """Sauvegarde le score"""
        scores = self.db['scores']
        
        scores.insert_one({
            'player_name': self.player_name,
            'waves': self.waves
        })
        
        all_scores = list(scores.find().sort('waves', -1))
        if len(all_scores) > 3:
            ids_to_delete = [score['_id'] for score in all_scores[3:]]
            scores.delete_many({'_id': {'$in': ids_to_delete}})
