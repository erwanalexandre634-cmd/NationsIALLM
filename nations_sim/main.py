# -*- coding: utf-8 -*-
# Point d'entrée principal du jeu Nations AI Simulator
# Lance le jeu complet avec interface graphique

import pygame
import sys
import time

from world import World
from ui import GameUI
from game import Game
from llm_brain import LLMBrain
from config import TURN_DELAY


def main():
    """
    Fonction principale: initialise et lance le jeu.
    """
    print("="*60)
    print("🌍 NATIONS AI SIMULATOR")
    print("="*60)
    print()

    # Vérification 1: Ollama est-il lancé?
    print("🔍 Vérification d'Ollama...")
    brain = LLMBrain()

    if not brain.is_ollama_running():
        print("❌ ERREUR: Ollama ne répond pas!")
        print()
        print("📝 Pour lancer Ollama:")
        print("   1. Ouvre un nouveau terminal")
        print("   2. Lance: ollama serve")
        print("   3. Relance ce programme")
        print()
        input("Appuie sur ENTRÉE pour quitter...")
        sys.exit(1)

    print("✅ Ollama est actif!\n")

    # Génération du monde
    print("🌍 Génération du monde...")
    world = World()
    world.generate()
    print("✅ Monde généré!\n")

    # Création de l'interface
    print("🎨 Initialisation de l'interface...")
    ui = GameUI(world)
    print("✅ Interface prête!\n")

    # Création du jeu
    print("🎮 Initialisation du jeu...")
    game = Game(world, ui)
    print("✅ Jeu prêt!\n")

    print("="*60)
    print("🚀 LE JEU DÉMARRE!")
    print("="*60)
    print()
    print("📋 CONTRÔLES:")
    print("   - PAUSE: Met le jeu en pause")
    print("   - x1, x2, x5: Change la vitesse")
    print("   - Clic sur la carte: Sélectionne une nation")
    print("   - QUITTER: Ferme le jeu")
    print("   - ESC: Ferme le jeu")
    print()

    # Boucle principale
    running = True
    paused = False
    speed_multiplier = 1  # 1, 2, ou 5

    # Gestion du temps pour les tours
    last_turn_time = time.time()
    turn_delay = TURN_DELAY  # Délai entre les tours en secondes

    while running:
        # Gestion des événements Pygame
        for event in pygame.event.get():
            # Fermeture de la fenêtre
            if event.type == pygame.QUIT:
                running = False

            # Touches du clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    print(f"{'⏸️ PAUSE' if paused else '▶️ PLAY'}")

            # Clics de souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = ui.handle_click(event.pos)

                if action == "quit":
                    running = False

                elif action == "pause":
                    paused = not paused
                    ui.paused = paused
                    print(f"{'⏸️ PAUSE' if paused else '▶️ PLAY'}")

                elif action == "speed_1":
                    speed_multiplier = 1
                    ui.speed = 1
                    print("⏩ Vitesse: x1")

                elif action == "speed_2":
                    speed_multiplier = 2
                    ui.speed = 2
                    print("⏩ Vitesse: x2")

                elif action == "speed_5":
                    speed_multiplier = 5
                    ui.speed = 5
                    print("⏩ Vitesse: x5")

        # Si pas en pause et pas game over, avance le jeu
        if not paused and not game.game_over:
            current_time = time.time()
            adjusted_delay = turn_delay / speed_multiplier

            # Est-il temps de jouer un nouveau tour?
            if current_time - last_turn_time >= adjusted_delay:
                game.play_turn()
                last_turn_time = current_time

        # Si game over, affiche le message
        if game.game_over:
            if not paused:  # Pause automatique à la fin
                paused = True
                ui.paused = True

        # Affichage
        ui.draw(game.turn_number)
        ui.tick(60)  # Limite à 60 FPS

    # Fin du jeu
    pygame.quit()
    print("\n" + "="*60)
    if game.game_over and game.winner:
        print(f"🏆 VICTOIRE: {game.winner.name}")
    print("👋 Merci d'avoir joué à Nations AI Simulator!")
    print("="*60)


if __name__ == "__main__":
    """
    Point d'entrée: lance le jeu si ce fichier est exécuté.
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interruption par l'utilisateur (Ctrl+C)")
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuie sur ENTRÉE pour quitter...")
        pygame.quit()
        sys.exit(1)
