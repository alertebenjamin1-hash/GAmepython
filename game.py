import random
from models import Combattant

def lancer_combat(equipe, liste_monstres_db):
    vagues = 0
    equipe_vivante = True

    while equipe_vivante:
        # 1. Choisir un monstre au hasard
        m_data = random.choice(liste_monstres_db)
        # on appels db_init
        monstre = Combattant(m_data['name'], m_data['attack'], m_data['defense'], m_data['hp'])
        
        print(f"\n--- VAGUE {vagues + 1} : Un {monstre.nom} approche ! ---")
        
        # Boucle du combat actuel
        while monstre.est_en_vie() and equipe_vivante:
            # Tour des personnages
            for perso in equipe:
                if perso.est_en_vie():
                    degats = perso.attaquer(monstre)
                    print(f" > {perso.nom} attaque et inflige {degats} dégâts au {monstre.nom}.")
            
            if not monstre.est_en_vie():
                print(f"Le {monstre.nom} est mort !")
                vagues += 1
                break

            # Tour du monstre (il attaque un membre au hasard)
            vivants = [p for p in equipe if p.est_en_vie()]
            if vivants:
                cible = random.choice(vivants)
                degats_m = monstre.attaquer(cible)
                print(f" ! {monstre.nom} frappe {cible.nom} (-{degats_m} PV).")
            else:
                equipe_vivante = False

            # Vérifier si l'équipe est KO
            if not any(p.est_en_vie() for p in equipe):
                equipe_vivante = False
                print("Toute l'équipe est au tapis...")

    return vagues