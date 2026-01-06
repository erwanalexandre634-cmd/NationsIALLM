#!/usr/bin/env python3
# Script de test pour vérifier que le LLM fonctionne correctement

from llm_brain import LLMBrain, test_ollama_connection
from prompts import build_decision_prompt
from config import PERSONALITIES


def test_nation_decision():
    """
    Simule une nation et lui demande de prendre une décision.
    C'est un test pour voir si le LLM répond correctement.
    """
    print("\n" + "="*60)
    print("🧪 TEST: Simulation d'une décision de nation")
    print("="*60 + "\n")

    # Création d'un "faux" objet nation pour le test
    class FakeNation:
        def __init__(self):
            self.name = "Empire Rouge"
            self.leader_name = "Empereur Marcus"
            self.personality_description = PERSONALITIES["agressif"]
            self.army = 60
            self.gold = 180
            self.territories = 8
            self.relations = {
                "République Verte": -40,  # En conflit
                "Royaume Bleu": 20,       # Neutre/positif
            }

    # Création d'un état du monde fictif
    world_state = {
        'turn': 12,
        'attack_cost_gold': 20,
        'attack_cost_army': 10,
        'neighbors': {
            'République Verte': {
                'army': 30,  # Plus faible que nous
                'gold': 150,
                'territories': 5
            },
            'Royaume Bleu': {
                'army': 70,  # Plus fort que nous
                'gold': 200,
                'territories': 10
            }
        }
    }

    recent_event = "République Verte a attaqué un de tes territoires au tour précédent mais a échoué."

    # Création du cerveau LLM
    brain = LLMBrain()

    # Construction du prompt
    nation = FakeNation()
    prompt = build_decision_prompt(nation, world_state, recent_event)

    print("📝 PROMPT ENVOYÉ AU LLM:")
    print("-" * 60)
    print(prompt)
    print("-" * 60 + "\n")

    # Demande de décision
    print("🤖 Demande de décision au LLM...")
    print("   (Cela peut prendre quelques secondes)\n")

    decision = brain.ask_decision(prompt)

    # Affichage du résultat
    if decision and brain.validate_decision(decision):
        print("✅ DÉCISION REÇUE:")
        print(f"   Action: {decision['action']}")
        print(f"   Cible: {decision['target']}")
        print(f"   Raison: {decision['reason']}")
        print("\n🎉 Le LLM fonctionne parfaitement!")
        return True
    else:
        print("❌ ÉCHEC: Le LLM n'a pas pu donner une décision valide")
        if decision:
            print(f"   Réponse reçue: {decision}")
        return False


def main():
    """Fonction principale du test"""
    # Test 1: Connexion de base
    print("\n" + "🔍 ÉTAPE 1: Vérification de la connexion Ollama" + "\n")
    if not test_ollama_connection():
        print("\n⚠️ Résolution:")
        print("   1. Assure-toi qu'Ollama est installé")
        print("   2. Lance 'ollama serve' dans un terminal")
        print("   3. Télécharge un modèle: 'ollama pull llama3.2'")
        return

    # Test 2: Décision de nation
    print("\n" + "🔍 ÉTAPE 2: Test d'une décision de nation" + "\n")
    success = test_nation_decision()

    # Résumé
    print("\n" + "="*60)
    if success:
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("   Tu peux passer à l'étape suivante du développement.")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("   Vérifie les erreurs ci-dessus.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
