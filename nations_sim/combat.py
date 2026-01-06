# -*- coding: utf-8 -*-
# Système de combat entre nations
# Calcule les batailles et gère les conquêtes de territoires

import random
from config import ATTACK_COST_GOLD, ATTACK_COST_ARMY


def resolve_battle(attacker, defender):
    """
    Résout une bataille entre deux nations.

    Le calcul est simple:
    - Force de l'attaquant = armée + aléatoire(-15, +15)
    - Force du défenseur = armée + bonus défense + aléatoire(-15, +15)
    - Le plus fort gagne

    Args:
        attacker (Nation): La nation qui attaque
        defender (Nation): La nation qui défend

    Returns:
        bool: True si l'attaquant gagne, False sinon
    """
    # Calcul des forces avec une part d'aléatoire (représente le chaos de la guerre)
    attacker_force = attacker.army + random.randint(-15, 15)
    defender_force = defender.army + defender.defense_bonus + random.randint(-15, 15)

    # Compare les forces
    if attacker_force > defender_force:
        return True  # Victoire de l'attaquant
    else:
        return False  # Victoire du défenseur


def execute_attack(attacker, defender, world):
    """
    Exécute une attaque complète:
    1. Vérifie que l'attaquant a assez d'or et d'armée
    2. Paie le coût de l'attaque
    3. Résout la bataille
    4. Si victoire: conquiert un territoire
    5. Met à jour les relations

    Args:
        attacker (Nation): La nation qui attaque
        defender (Nation): La nation qui défend
        world (World): Le monde du jeu (pour transférer les territoires)

    Returns:
        dict: Résultat de l'attaque avec 'success', 'message', 'territory_conquered'
    """
    result = {
        'success': False,
        'message': '',
        'territory_conquered': None
    }

    # Vérification: L'attaquant a-t-il assez de ressources?
    if attacker.gold < ATTACK_COST_GOLD:
        result['message'] = f"Pas assez d'or! ({attacker.gold}/{ATTACK_COST_GOLD})"
        return result

    if attacker.army < ATTACK_COST_ARMY:
        result['message'] = f"Armée trop faible! ({attacker.army}/{ATTACK_COST_ARMY})"
        return result

    # Vérification: Les nations sont-elles voisines?
    if defender not in world.get_neighboring_nations(attacker):
        result['message'] = "Cible trop éloignée (pas de frontière commune)"
        return result

    # Coût de l'attaque (payé même si défaite)
    attacker.gold -= ATTACK_COST_GOLD
    attacker.army -= ATTACK_COST_ARMY

    # Résolution de la bataille
    attacker_wins = resolve_battle(attacker, defender)

    if attacker_wins:
        # VICTOIRE: Conquête d'un territoire
        conquered = steal_border_territory(attacker, defender, world)

        if conquered:
            x, y = conquered
            result['success'] = True
            result['territory_conquered'] = (x, y)
            result['message'] = f"Victoire! Territoire ({x},{y}) conquis!"

            # Le défenseur perd des troupes
            defender.army = max(0, defender.army - 10)

            # Les relations se dégradent fortement
            attacker.change_relation(defender.name, -30)
            defender.change_relation(attacker.name, -30)
        else:
            result['message'] = "Victoire tactique, mais aucun territoire conquis"
    else:
        # DÉFAITE
        result['message'] = "Défaite! L'attaque a échoué."

        # L'attaquant perd encore plus de troupes (punition pour avoir perdu)
        attacker.army = max(0, attacker.army - 10)

        # Relations dégradées (mais moins que si victoire)
        attacker.change_relation(defender.name, -20)
        defender.change_relation(attacker.name, -20)

    # Réinitialise le bonus de défense du défenseur (il était temporaire)
    defender.defense_bonus = 0

    return result


def steal_border_territory(attacker, defender, world):
    """
    Vole un territoire frontalier du défenseur.

    Args:
        attacker (Nation): La nation qui vole
        defender (Nation): La nation qui perd
        world (World): Le monde du jeu

    Returns:
        tuple: (x, y) du territoire volé, ou None si impossible
    """
    # Trouve tous les territoires du défenseur adjacents à l'attaquant
    target_territories = []

    for dx, dy in defender.territories:
        # Regarde les 4 voisins de ce territoire
        for nx, ny in [(dx-1, dy), (dx+1, dy), (dx, dy-1), (dx, dy+1)]:
            neighbor = world.get_nation_at(nx, ny)
            if neighbor == attacker:
                # Ce territoire du défenseur est adjacent à l'attaquant
                target_territories.append((dx, dy))
                break  # Un seul voisin suffit

    # Si on a trouvé des territoires conquérables
    if target_territories:
        # Choisit un territoire aléatoire
        stolen = random.choice(target_territories)
        x, y = stolen

        # Transfère le territoire
        world.transfer_territory(x, y, defender, attacker)

        return stolen

    return None


# ===== TEST DU MODULE =====
if __name__ == "__main__":
    """
    Test du système de combat.
    Lance ce fichier avec: python combat.py
    """
    print("🧪 Test de combat.py\n")

    # Import nécessaire pour le test
    from nation import Nation
    from world import World

    # Crée un monde simple
    world = World()
    world.generate()

    # Prend deux nations voisines
    nation1 = world.nations[0]
    nation2 = None

    # Trouve un voisin
    neighbors = world.get_neighboring_nations(nation1)
    if neighbors:
        nation2 = neighbors[0]

    if nation2:
        print(f"⚔️ Test de bataille:")
        print(f"   Attaquant: {nation1.name} (Armée: {nation1.army}, Or: {nation1.gold})")
        print(f"   Défenseur: {nation2.name} (Armée: {nation2.army}, Or: {nation2.gold})")
        print(f"   Territoires avant: {nation1.get_territory_count()} vs {nation2.get_territory_count()}\n")

        # Exécute l'attaque
        result = execute_attack(nation1, nation2, world)

        print(f"📜 Résultat: {result['message']}")
        print(f"   Territoires après: {nation1.get_territory_count()} vs {nation2.get_territory_count()}")
        print(f"   Armées après: {nation1.army} vs {nation2.army}")

        if result['success']:
            print(f"✅ Territoire {result['territory_conquered']} conquis!")
        else:
            print(f"❌ Attaque échouée")

        print("\n🎉 Test de combat.py terminé!")
    else:
        print("⚠️ Impossible de trouver deux nations voisines pour tester")
