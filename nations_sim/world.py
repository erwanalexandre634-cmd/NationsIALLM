# -*- coding: utf-8 -*-
# Génération et gestion de la carte du monde
# La carte est une grille 2D où chaque case appartient à une nation (ou est vide)

import random
from nation import Nation
from config import (
    WORLD_WIDTH, WORLD_HEIGHT, INITIAL_NATIONS,
    NATION_NAMES, NATION_COLORS, PERSONALITIES,
    INITIAL_ARMY, INITIAL_GOLD
)


class World:
    """
    Représente le monde du jeu : la carte et toutes les nations.
    """

    def __init__(self):
        """
        Crée un monde vide.
        """
        # Grille 2D: world_map[x][y] = Nation ou None
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT
        self.world_map = [[None for _ in range(self.height)] for _ in range(self.width)]

        # Liste des nations actives
        self.nations = []

    def generate(self):
        """
        Génère le monde:
        1. Crée les nations avec des personnalités aléatoires
        2. Place chaque nation sur la carte avec ~8 territoires
        """
        print("🌍 Génération du monde...")

        # Crée les nations
        personalities_list = list(PERSONALITIES.keys())

        for i in range(INITIAL_NATIONS):
            # Choisit une personnalité aléatoire
            personality = random.choice(personalities_list)

            # Crée la nation
            nation = Nation(
                name=NATION_NAMES[i],
                color=NATION_COLORS[i],
                leader_name=f"Leader {i+1}",  # Nom simple pour le leader
                personality=personality,
                personality_description=PERSONALITIES[personality]
            )

            # Initialise les ressources
            nation.army = INITIAL_ARMY
            nation.gold = INITIAL_GOLD

            self.nations.append(nation)

        print(f"✅ {len(self.nations)} nations créées")

        # Place les nations sur la carte
        self._place_nations_on_map()

        print("✅ Monde généré avec succès!")

    def _place_nations_on_map(self):
        """
        Place chaque nation sur la carte avec plusieurs territoires contigus.

        FIX BUG 2: Les nations sont maintenant placées en GRILLE 2x3 pour garantir
        qu'elles sont adjacentes les unes aux autres.

        Disposition:
        +--------+--------+--------+
        | Nation | Nation | Nation |
        |   0    |   1    |   2    |
        +--------+--------+--------+
        | Nation | Nation | Nation |
        |   3    |   4    |   5    |
        +--------+--------+--------+
        """
        territories_per_nation = 12  # Augmenté pour bien remplir chaque région

        # Définit les régions pour chaque nation (grille 2x3)
        # Carte 20x15 divisée en 6 régions de ~7x7
        regions = [
            (0, 0, 7, 7),      # Nation 0: Top-left
            (7, 0, 14, 7),     # Nation 1: Top-center
            (14, 0, 20, 7),    # Nation 2: Top-right
            (0, 7, 7, 15),     # Nation 3: Bottom-left
            (7, 7, 14, 15),    # Nation 4: Bottom-center
            (14, 7, 20, 15),   # Nation 5: Bottom-right
        ]

        for i, nation in enumerate(self.nations):
            if i >= len(regions):
                break  # Sécurité si plus de 6 nations

            x_min, y_min, x_max, y_max = regions[i]

            # Place un seed au centre de la région
            seed_x = (x_min + x_max) // 2
            seed_y = (y_min + y_max) // 2
            self._set_territory(seed_x, seed_y, nation)

            # Fait grandir le territoire dans la région
            for _ in range(territories_per_nation - 1):
                # Trouve une case adjacente libre DANS LA RÉGION
                new_territory = self._find_adjacent_free_cell_in_region(
                    nation, x_min, y_min, x_max, y_max
                )
                if new_territory:
                    x, y = new_territory
                    self._set_territory(x, y, nation)
                else:
                    # Si plus de place adjacente, place aléatoirement dans la région
                    attempts = 0
                    while attempts < 20:
                        rand_x = random.randint(x_min, x_max - 1)
                        rand_y = random.randint(y_min, y_max - 1)
                        if self.world_map[rand_x][rand_y] is None:
                            self._set_territory(rand_x, rand_y, nation)
                            break
                        attempts += 1

    def _set_territory(self, x, y, nation):
        """
        Assigne un territoire à une nation.

        Args:
            x (int): Coordonnée X
            y (int): Coordonnée Y
            nation (Nation): La nation qui possède ce territoire
        """
        self.world_map[x][y] = nation
        nation.add_territory(x, y)

    def _find_adjacent_free_cell(self, nation):
        """
        Trouve une case libre adjacente aux territoires de la nation.

        Args:
            nation (Nation): La nation dont on cherche une case adjacente

        Returns:
            tuple: (x, y) ou None si aucune case libre
        """
        # Liste toutes les cases adjacentes aux territoires de la nation
        adjacent_cells = []

        for tx, ty in nation.territories:
            # Les 4 voisins (haut, bas, gauche, droite)
            neighbors = [
                (tx - 1, ty), (tx + 1, ty),
                (tx, ty - 1), (tx, ty + 1)
            ]

            for nx, ny in neighbors:
                # Vérifie que c'est dans les limites de la carte
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Vérifie que la case est libre
                    if self.world_map[nx][ny] is None:
                        adjacent_cells.append((nx, ny))

        # Retourne une case aléatoire parmi les adjacentes libres
        if adjacent_cells:
            return random.choice(adjacent_cells)
        return None

    def _find_adjacent_free_cell_in_region(self, nation, x_min, y_min, x_max, y_max):
        """
        Trouve une case libre adjacente aux territoires de la nation,
        mais UNIQUEMENT dans une région définie.

        Args:
            nation (Nation): La nation dont on cherche une case adjacente
            x_min, y_min, x_max, y_max (int): Limites de la région

        Returns:
            tuple: (x, y) ou None si aucune case libre
        """
        # Liste toutes les cases adjacentes aux territoires de la nation
        adjacent_cells = []

        for tx, ty in nation.territories:
            # Les 4 voisins (haut, bas, gauche, droite)
            neighbors = [
                (tx - 1, ty), (tx + 1, ty),
                (tx, ty - 1), (tx, ty + 1)
            ]

            for nx, ny in neighbors:
                # Vérifie que c'est dans les limites de la RÉGION
                if x_min <= nx < x_max and y_min <= ny < y_max:
                    # Vérifie que la case est libre
                    if self.world_map[nx][ny] is None:
                        adjacent_cells.append((nx, ny))

        # Retourne une case aléatoire parmi les adjacentes libres
        if adjacent_cells:
            return random.choice(adjacent_cells)
        return None

    def get_nation_at(self, x, y):
        """
        Retourne la nation qui possède le territoire à (x, y).

        Args:
            x (int): Coordonnée X
            y (int): Coordonnée Y

        Returns:
            Nation: La nation propriétaire, ou None si vide
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.world_map[x][y]
        return None

    def get_nation_by_name(self, name):
        """
        Trouve une nation par son nom.

        Args:
            name (str): Nom de la nation

        Returns:
            Nation: La nation trouvée, ou None
        """
        for nation in self.nations:
            if nation.name == name:
                return nation
        return None

    def get_neighboring_nations(self, nation):
        """
        Retourne les nations qui sont voisines (ont un territoire adjacent).

        Args:
            nation (Nation): La nation dont on cherche les voisins

        Returns:
            list: Liste de nations voisines (sans doublons)
        """
        neighbors = set()  # Utilise un set pour éviter les doublons

        # Pour chaque territoire de la nation
        for tx, ty in nation.territories:
            # Regarde les 4 voisins
            for nx, ny in [(tx-1, ty), (tx+1, ty), (tx, ty-1), (tx, ty+1)]:
                neighbor_nation = self.get_nation_at(nx, ny)
                # Si c'est une nation différente
                if neighbor_nation and neighbor_nation != nation:
                    neighbors.add(neighbor_nation)

        return list(neighbors)

    def get_border_territories(self, nation, target_nation):
        """
        Retourne les territoires de 'nation' qui sont adjacents à 'target_nation'.
        Utile pour déterminer où attaquer.

        Args:
            nation (Nation): La nation attaquante
            target_nation (Nation): La nation cible

        Returns:
            list: Liste de coordonnées (x, y) des territoires frontaliers
        """
        border = []

        for tx, ty in nation.territories:
            # Regarde les 4 voisins
            for nx, ny in [(tx-1, ty), (tx+1, ty), (tx, ty-1), (tx, ty+1)]:
                neighbor = self.get_nation_at(nx, ny)
                if neighbor == target_nation:
                    border.append((tx, ty))
                    break  # Ce territoire est frontalier, pas besoin de chercher plus

        return border

    def transfer_territory(self, x, y, from_nation, to_nation):
        """
        Transfère un territoire d'une nation à une autre (conquête).

        Args:
            x (int): Coordonnée X
            y (int): Coordonnée Y
            from_nation (Nation): Nation qui perd le territoire
            to_nation (Nation): Nation qui gagne le territoire
        """
        # Retire le territoire de l'ancienne nation
        from_nation.remove_territory(x, y)

        # Ajoute le territoire à la nouvelle nation
        to_nation.add_territory(x, y)

        # Met à jour la carte
        self.world_map[x][y] = to_nation

    def get_alive_nations(self):
        """
        Retourne uniquement les nations encore en vie.

        Returns:
            list: Liste des nations vivantes
        """
        return [nation for nation in self.nations if nation.is_alive]

    def check_victory(self):
        """
        Vérifie si une nation a gagné.
        Conditions de victoire:
        1. Il ne reste qu'une seule nation vivante
        2. Ou une nation contrôle 70% de la carte

        Returns:
            Nation: La nation gagnante, ou None
        """
        alive = self.get_alive_nations()

        # Condition 1: Une seule nation reste
        if len(alive) == 1:
            return alive[0]

        # Condition 2: Une nation a 70% de la carte
        total_territories = sum(nation.get_territory_count() for nation in alive)
        for nation in alive:
            if nation.get_territory_count() / total_territories >= 0.7:
                return nation

        return None


# ===== TEST DU MODULE =====
if __name__ == "__main__":
    """
    Test de la génération du monde.
    Lance ce fichier avec: python world.py
    """
    print("🧪 Test de world.py\n")

    # Crée et génère le monde
    world = World()
    world.generate()

    print(f"\n📊 Statistiques du monde:")
    print(f"   Taille: {world.width}x{world.height} = {world.width * world.height} cases")
    print(f"   Nations: {len(world.nations)}")

    # Affiche chaque nation
    print("\n🗺️ Nations créées:")
    for nation in world.nations:
        neighbors = world.get_neighboring_nations(nation)
        neighbor_names = [n.name for n in neighbors]
        print(f"   - {nation.name} ({nation.personality}): {nation.get_territory_count()} territoires")
        print(f"     Voisins: {', '.join(neighbor_names) if neighbor_names else 'Aucun'}")

    # Compte les territoires occupés
    occupied = sum(nation.get_territory_count() for nation in world.nations)
    print(f"\n✅ Cases occupées: {occupied}/{world.width * world.height}")
    print(f"✅ Nations vivantes: {len(world.get_alive_nations())}")

    print("\n🎉 Tous les tests de world.py sont passés!")
