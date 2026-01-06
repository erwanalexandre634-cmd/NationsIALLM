# -*- coding: utf-8 -*-
# Logique principale du jeu
# Orchestre les tours, les décisions LLM, les actions, l'économie

import random
import threading  # FIX BUG 1: Threading pour appels LLM asynchrones
from llm_brain import LLMBrain
from prompts import build_decision_prompt
from combat import execute_attack
from config import (
    GOLD_PER_TERRITORY, ARMY_COST,
    ATTACK_COST_GOLD, ATTACK_COST_ARMY
)


class Game:
    """
    Gère la logique du jeu:
    - Tours de jeu
    - Décisions des nations (via LLM)
    - Exécution des actions
    - Économie
    - Conditions de victoire
    """

    def __init__(self, world, ui):
        """
        Initialise le jeu.

        Args:
            world (World): Le monde du jeu
            ui (GameUI): L'interface graphique
        """
        self.world = world
        self.ui = ui
        self.llm_brain = LLMBrain()

        # État du jeu
        self.turn_number = 0
        self.game_over = False
        self.winner = None

        # Historique des événements récents (pour le prompt LLM)
        # Format: {"Nation": "événement"}
        self.recent_events = {}

        # FIX BUG 1: Variables pour le threading des décisions LLM
        self.pending_decisions = {}  # {nation_name: decision} - Décisions reçues
        self.nations_thinking = set()  # Nations en train de "penser" (thread actif)
        self.nations_waiting = []  # Nations qui attendent de jouer ce tour

    def play_turn(self):
        """
        FIX BUG 1: Joue un tour de manière ASYNCHRONE (ne bloque pas l'UI).

        Fonctionnement:
        1. Au premier appel: Lance les threads de décision pour toutes les nations
        2. Aux appels suivants: Exécute les décisions reçues
        3. Quand toutes les décisions sont exécutées: Termine le tour

        Cette fonction ne bloque JAMAIS, même si les LLM prennent 10 secondes.
        """
        # Si c'est le début d'un nouveau tour, lance les décisions
        if not self.nations_waiting and len(self.nations_thinking) == 0:
            self.turn_number += 1
            print(f"\n{'='*60}")
            print(f"🎮 TOUR {self.turn_number}")
            print(f"{'='*60}")

            # Log dans le journal
            self.ui.add_to_journal(self.turn_number, f"--- Tour {self.turn_number} ---", (200, 200, 200), "internal")

            # Mélange l'ordre des nations (équité)
            nations = self.world.get_alive_nations()
            random.shuffle(nations)
            self.nations_waiting = list(nations)

            # Lance les threads de décision pour TOUTES les nations en parallèle
            for nation in self.nations_waiting:
                if nation.is_alive:
                    self._request_decision_async(nation)

        # Exécute les décisions qui sont prêtes
        executed = []
        for nation in list(self.nations_waiting):
            # Si la décision est prête
            if nation.name in self.pending_decisions:
                decision = self.pending_decisions.pop(nation.name)

                # Exécute l'action
                self._execute_decision(nation, decision)

                # Marque comme exécutée
                executed.append(nation)

        # Retire les nations dont la décision a été exécutée
        for nation in executed:
            if nation in self.nations_waiting:
                self.nations_waiting.remove(nation)

        # Si toutes les décisions sont exécutées, termine le tour
        if len(self.nations_waiting) == 0 and len(self.nations_thinking) == 0:
            # Économie: Chaque nation gagne de l'or selon ses territoires
            self._update_economy()

            # Vérifie si quelqu'un a gagné
            self._check_victory()

    def _request_decision_async(self, nation):
        """
        FIX BUG 1: Demande à l'IA de prendre une décision EN ARRIÈRE-PLAN (threading).

        Cette fonction lance un thread qui appelle le LLM sans bloquer l'UI.
        Quand la décision est prête, elle est stockée dans self.pending_decisions.

        Args:
            nation (Nation): La nation qui doit décider
        """
        # Marque cette nation comme "en train de réfléchir"
        self.nations_thinking.add(nation.name)

        # Log dans le journal
        thinking_text = f"{nation.name} réfléchit..."
        self.ui.add_to_journal(self.turn_number, thinking_text, (150, 150, 150), "internal")

        def think():
            """
            Fonction exécutée dans le thread :
            1. Construit le prompt
            2. Appelle le LLM (BLOQUANT, mais dans un thread séparé)
            3. Stocke la décision
            """
            # Construit l'état du monde pour le prompt
            world_state = self._build_world_state(nation)

            # Récupère l'événement récent concernant cette nation
            recent_event = self.recent_events.get(nation.name, None)

            # Construit le prompt
            prompt = build_decision_prompt(nation, world_state, recent_event)

            # Demande au LLM (BLOQUE ici, mais seulement ce thread)
            decision = self.llm_brain.ask_decision(prompt)

            # Valide la décision
            if not self.llm_brain.validate_decision(decision):
                print(f"⚠️ Décision invalide pour {nation.name}, action par défaut")
                decision = self.llm_brain.get_default_decision()

            print(f"✅ {nation.name} a décidé: {decision['action']} → {decision['target']}")

            # Stocke la décision (thread-safe car dict.assignment est atomique en Python)
            self.pending_decisions[nation.name] = decision

            # Retire de la liste "en train de penser"
            self.nations_thinking.discard(nation.name)

        # Lance le thread
        thread = threading.Thread(target=think, daemon=True)
        thread.start()

    def _build_world_state(self, nation):
        """
        Construit un dictionnaire avec l'état du monde pour le prompt LLM.

        Args:
            nation (Nation): La nation qui demande l'info

        Returns:
            dict: État du monde
        """
        # Trouve les voisins
        neighbors = self.world.get_neighboring_nations(nation)
        neighbors_info = {}

        for neighbor in neighbors:
            neighbors_info[neighbor.name] = {
                'army': neighbor.army,
                'gold': neighbor.gold,
                'territories': neighbor.get_territory_count()
            }

        # FIX BUG 3: Ajoute la liste de TOUTES les nations pour éviter les noms inventés
        all_nations_info = {}
        for other_nation in self.world.get_alive_nations():
            if other_nation != nation:  # Exclut la nation elle-même
                all_nations_info[other_nation.name] = {
                    'is_alive': other_nation.is_alive
                }

        return {
            'turn': self.turn_number,
            'neighbors': neighbors_info,
            'all_nations': all_nations_info,  # NOUVEAU: Liste de toutes les nations
            'attack_cost_gold': ATTACK_COST_GOLD,
            'attack_cost_army': ATTACK_COST_ARMY
        }

    def _execute_decision(self, nation, decision):
        """
        Exécute l'action décidée par la nation.

        Args:
            nation (Nation): La nation qui agit
            decision (dict): La décision à exécuter
        """
        action = decision['action']
        target_name = decision['target']
        reason = decision['reason']

        # Log de la décision
        log_text = f"{nation.name}: {action}"
        if target_name:
            log_text += f" → {target_name}"
        log_text += f" ({reason})"

        # Détermine la catégorie selon l'action
        category_map = {
            "attack": "war",
            "ally": "diplomacy",
            "trade": "economy",
            "expand": "expansion",
            "build_army": "internal",
            "defend": "internal",
            "nothing": "internal"
        }
        category = category_map.get(action, "internal")

        self.ui.add_to_journal(self.turn_number, log_text, nation.color, category)

        # Exécute selon l'action
        if action == "attack":
            self._action_attack(nation, target_name, reason)

        elif action == "ally":
            self._action_ally(nation, target_name, reason)

        elif action == "trade":
            self._action_trade(nation, target_name, reason)

        elif action == "build_army":
            self._action_build_army(nation, reason)

        elif action == "defend":
            self._action_defend(nation, reason)

        elif action == "expand":
            self._action_expand(nation, reason)

        elif action == "nothing":
            # Ne rien faire (économie d'or)
            pass

    def _action_attack(self, attacker, target_name, reason):
        """
        Exécute une attaque.

        Args:
            attacker (Nation): Nation attaquante
            target_name (str): Nom de la nation cible
            reason (str): Raison de l'attaque
        """
        # FIX BUG 6: Vérifie que la cible existe
        target = self.world.get_nation_by_name(target_name)
        if not target or not target.is_alive:
            result_text = f"❌ Cible invalide: {target_name} n'existe pas ou est morte"
            self.ui.add_to_journal(self.turn_number, result_text, (255, 100, 100), "war")
            return

        # Exécute l'attaque
        result = execute_attack(attacker, target, self.world)

        # Log du résultat
        if result['success']:
            x, y = result['territory_conquered']
            result_text = f"⚔️ {attacker.name} conquiert ({x},{y}) de {target.name}!"
            color = (100, 255, 100)

            # Enregistre l'événement pour les deux nations
            self.recent_events[attacker.name] = f"Tu as conquis un territoire de {target.name}"
            self.recent_events[target.name] = f"{attacker.name} t'a attaqué et a conquis un territoire"
        else:
            result_text = f"🛡️ {target.name} repousse l'attaque de {attacker.name}"
            color = (255, 150, 100)

            self.recent_events[attacker.name] = f"Ton attaque contre {target.name} a échoué"
            self.recent_events[target.name] = f"Tu as repoussé l'attaque de {attacker.name}"

        self.ui.add_to_journal(self.turn_number, result_text, color, "war")

        # Si le défenseur est mort
        if not target.is_alive:
            death_text = f"💀 {target.name} a été éliminé par {attacker.name}!"
            self.ui.add_to_journal(self.turn_number, death_text, (255, 50, 50), "war")

    def _action_ally(self, nation, target_name, reason):
        """
        Propose une alliance.

        Args:
            nation (Nation): Nation qui propose
            target_name (str): Nom de la nation cible
            reason (str): Raison de l'alliance
        """
        target = self.world.get_nation_by_name(target_name)
        if not target or not target.is_alive:
            return

        # L'autre nation accepte si relations > -20
        current_relation = target.get_relation(nation.name)

        if current_relation > -20:
            # Alliance acceptée
            nation.change_relation(target_name, 50)
            target.change_relation(nation.name, 50)

            result_text = f"🤝 {nation.name} et {target_name} forment une alliance!"
            self.ui.add_to_journal(self.turn_number, result_text, (100, 255, 255), "diplomacy")

            self.recent_events[nation.name] = f"{target_name} a accepté ton alliance"
            self.recent_events[target_name] = f"{nation.name} te propose une alliance (acceptée)"
        else:
            # Alliance refusée
            result_text = f"❌ {target_name} refuse l'alliance avec {nation.name}"
            self.ui.add_to_journal(self.turn_number, result_text, (200, 200, 200), "diplomacy")

            self.recent_events[nation.name] = f"{target_name} a refusé ton alliance"

    def _action_trade(self, nation, target_name, reason):
        """
        Commerce avec une autre nation.

        Args:
            nation (Nation): Nation qui commerce
            target_name (str): Nom de la nation cible
            reason (str): Raison du commerce
        """
        target = self.world.get_nation_by_name(target_name)
        if not target or not target.is_alive:
            return

        # Les deux gagnent de l'or
        gold_gain = 30
        nation.gold += gold_gain
        target.gold += gold_gain

        # Améliore les relations
        nation.change_relation(target_name, 10)
        target.change_relation(nation.name, 10)

        result_text = f"💰 {nation.name} commerce avec {target_name} (+{gold_gain} or chacun)"
        self.ui.add_to_journal(self.turn_number, result_text, (255, 215, 0), "economy")

        self.recent_events[nation.name] = f"Tu as commercé avec {target_name}"
        self.recent_events[target_name] = f"{nation.name} a commercé avec toi"

    def _action_build_army(self, nation, reason):
        """
        Recrute des troupes.

        Args:
            nation (Nation): Nation qui recrute
            reason (str): Raison du recrutement
        """
        cost = 50
        if nation.gold >= cost:
            nation.gold -= cost
            nation.army += 20
            nation.army = min(100, nation.army)  # Max 100

            result_text = f"⚔️ {nation.name} recrute des troupes (+20 armée)"
            self.ui.add_to_journal(self.turn_number, result_text, (200, 200, 255), "internal")

            self.recent_events[nation.name] = "Tu as renforcé ton armée"
        else:
            result_text = f"❌ {nation.name} n'a pas assez d'or pour recruter"
            self.ui.add_to_journal(self.turn_number, result_text, (200, 200, 200), "internal")

    def _action_defend(self, nation, reason):
        """
        Fortifie les défenses.

        Args:
            nation (Nation): Nation qui se défend
            reason (str): Raison de la défense
        """
        nation.defense_bonus = 20

        result_text = f"🛡️ {nation.name} fortifie ses défenses (+20 défense)"
        self.ui.add_to_journal(self.turn_number, result_text, (150, 150, 255), "internal")

        self.recent_events[nation.name] = "Tu as fortifié tes défenses"

    def _action_expand(self, nation, reason):
        """
        Conquête d'une case vide adjacente (expansion territoriale).
        GRATUIT et sans risque - permet de grandir sans guerre.

        Args:
            nation (Nation): Nation qui s'étend
            reason (str): Raison de l'expansion
        """
        # Trouve les cases vides adjacentes
        empty_cells = self.world.get_adjacent_empty_cells(nation)

        if empty_cells:
            # Choisit une case aléatoire
            x, y = random.choice(empty_cells)

            # Conquiert la case
            self.world._set_territory(x, y, nation)

            result_text = f"🗺️ {nation.name} s'étend vers ({x},{y})"
            self.ui.add_to_journal(self.turn_number, result_text, (100, 255, 100), "expansion")

            self.recent_events[nation.name] = f"Tu as conquis un territoire vide en ({x},{y})"
        else:
            result_text = f"⚠️ {nation.name} ne peut pas s'étendre (pas de case vide adjacente)"
            self.ui.add_to_journal(self.turn_number, result_text, (200, 200, 200), "expansion")

    def _update_economy(self):
        """
        Met à jour l'économie: chaque nation gagne de l'or selon ses territoires.
        """
        for nation in self.world.get_alive_nations():
            # FIX BUG 5: Vérifie qu'il y a au moins 1 territoire
            if nation.get_territory_count() > 0:
                gold_income = nation.get_territory_count() * GOLD_PER_TERRITORY
                nation.gold += gold_income

    def _check_victory(self):
        """
        Vérifie si une nation a gagné.
        """
        winner = self.world.check_victory()

        if winner:
            self.game_over = True
            self.winner = winner

            victory_text = f"🏆 {winner.name} a gagné la partie!"
            self.ui.add_to_journal(self.turn_number, victory_text, (255, 215, 0), "internal")
            print(f"\n{'='*60}")
            print(f"🏆 VICTOIRE: {winner.name} a gagné!")
            print(f"{'='*60}")


# ===== TEST DU MODULE =====
if __name__ == "__main__":
    """
    Test du jeu (sans interface graphique).
    Lance ce fichier avec: python game.py
    """
    print("🧪 Test de game.py (mode console)\n")

    from world import World

    # Mock UI simple pour le test
    class MockUI:
        def add_to_journal(self, turn, text, color, category="internal"):
            print(f"[Tour {turn}] [{category}] {text}")

    # Crée le monde
    world = World()
    world.generate()

    # Crée le jeu
    ui = MockUI()
    game = Game(world, ui)

    # Vérifie qu'Ollama est lancé
    if not game.llm_brain.is_ollama_running():
        print("❌ Ollama ne répond pas! Lance 'ollama serve' d'abord.")
    else:
        print("✅ Ollama actif, le jeu peut démarrer!\n")

        # Joue 3 tours de test
        for i in range(3):
            input(f"\nAppuie sur ENTRÉE pour jouer le tour {i+1}...")
            game.play_turn()

        print("\n✅ Test de game.py terminé!")
