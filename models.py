class Combattant:
    def __init__(self, nom, atk, defense, pv):
        self.nom = nom
        self.atk = atk
        self.defense = defense
        self.pv = pv

    def est_en_vie(self):
        #on verifie les pv sont superieur a 0
        return self.pv > 0

    def attaquer(self, cible):
        #Formule simple : Dégâts = Atk de l'attaquant - Def de la cible 
        degats =self.atk - cible.defense
        if degats < 0: 
            degats = 0   

        cible.pv -= degats
        return degats    

       