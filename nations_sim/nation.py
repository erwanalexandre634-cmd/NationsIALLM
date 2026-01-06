# -*- coding: utf-8 -*-
# Classe représentant une nation dans le simulateur
# Une nation = un nom, une couleur, une personnalité, des territoires, une armée, de l'or

class Nation:
    """
    Représente une nation dans le jeu.
    Chaque nation a une IA (LLM) qui prend les décisions.
    """

    def __init__(self, name, color, leader_name, personality, personality_description):
        """
        Crée une nouvelle nation.

        Args:
            name (str): Nom de la nation (ex: "Empire Rouge")
            color (tuple): Couleur RGB (ex: (255, 0, 0))
            leader_name (str): Nom du leader (ex: "Empereur Marcus")
            personality (str): Type de personnalité (ex: "agressif")
            personality_description (str): Description complète pour le LLM
        """
        # Identité de la nation
        self.name = name
        self.color = color
        self.leader_name = leader_name
        self.personality = personality
        self.personality_description = personality_description

        # Territoires possédés (liste de coordonnées (x, y))
        self.territories = []

        # Ressources militaires et économiques
        self.army = 50  # Force militaire (0-100)
        self.gold = 200  # Richesse

        # Relations avec les autres nations (dictionnaire)
        # Exemple: {"Empire Vert": -50, "Royaume Bleu": 30}
        # -100 = ennemi juré, 0 = neutre, +100 = allié
        self.relations = {}

        # État de la nation
        self.is_alive = True  # False si elle n'a plus de territoire

        # Bonus temporaire (ex: si elle fait "defend", +20 défense pour 1 tour)
        self.defense_bonus = 0

    def add_territory(self, x, y):
        """
        Ajoute un territoire à la nation.
        Appelé lors de la génération du monde ou lors d'une conquête.

        Args:
            x (int): Coordonnée X du territoire
            y (int): Coordonnée Y du territoire
        """
        if (x, y) not in self.territories:
            self.territories.append((x, y))

    def remove_territory(self, x, y):
        """
        Retire un territoire (quand il est conquis par un ennemi).

        Args:
            x (int): Coordonnée X du territoire
            y (int): Coordonnée Y du territoire
        """
        if (x, y) in self.territories:
            self.territories.remove((x, y))

        # FIX BUG 5: Si la nation n'a plus de territoire, elle meurt
        if len(self.territories) == 0:
            self.is_alive = False

    def get_territory_count(self):
        """
        Retourne le nombre de territoires possédés.

        Returns:
            int: Nombre de territoires
        """
        return len(self.territories)

    def change_relation(self, other_nation_name, delta):
        """
        Change la relation avec une autre nation.

        Args:
            other_nation_name (str): Nom de l'autre nation
            delta (int): Changement (ex: +30 pour améliorer, -50 pour dégrader)
        """
        # Si la relation n'existe pas encore, elle commence à 0
        if other_nation_name not in self.relations:
            self.relations[other_nation_name] = 0

        # Applique le changement
        self.relations[other_nation_name] += delta

        # Limite entre -100 et +100
        self.relations[other_nation_name] = max(-100, min(100, self.relations[other_nation_name]))

    def get_relation(self, other_nation_name):
        """
        Récupère la relation avec une autre nation.

        Args:
            other_nation_name (str): Nom de l'autre nation

        Returns:
            int: Score de relation (-100 à +100)
        """
        return self.relations.get(other_nation_name, 0)

    def __str__(self):
        """
        Représentation textuelle de la nation (pour le debug).

        Returns:
            str: Description de la nation
        """
        status = "Vivante" if self.is_alive else "Morte"
        return f"{self.name} ({status}) - {len(self.territories)} territoires, {self.army} armée, {self.gold} or"

    def __repr__(self):
        """Pour afficher la nation dans la console de debug"""
        return self.__str__()


# ===== TEST DU MODULE =====
if __name__ == "__main__":
    """
    Test de la classe Nation.
    Lance ce fichier avec: python nation.py
    """
    print("🧪 Test de la classe Nation\n")

    # Création d'une nation de test
    nation = Nation(
        name="Empire Rouge",
        color=(255, 0, 0),
        leader_name="Empereur Marcus",
        personality="agressif",
        personality_description="Tu aimes conquérir et dominer."
    )

    print(f"✅ Nation créée: {nation}")

    # Test: Ajout de territoires
    nation.add_territory(5, 3)
    nation.add_territory(6, 3)
    nation.add_territory(5, 4)
    print(f"✅ Territoires ajoutés: {nation.get_territory_count()} territoires")

    # Test: Relations
    nation.change_relation("Royaume Bleu", 30)
    nation.change_relation("Empire Vert", -50)
    print(f"✅ Relation avec Royaume Bleu: {nation.get_relation('Royaume Bleu')}")
    print(f"✅ Relation avec Empire Vert: {nation.get_relation('Empire Vert')}")

    # Test: Perte de territoire
    nation.remove_territory(5, 3)
    print(f"✅ Territoire perdu: {nation.get_territory_count()} territoires restants")

    # Test: Mort de la nation
    nation.remove_territory(6, 3)
    nation.remove_territory(5, 4)
    print(f"✅ Tous les territoires perdus: Nation vivante? {nation.is_alive}")

    print("\n🎉 Tous les tests de nation.py sont passés!")
