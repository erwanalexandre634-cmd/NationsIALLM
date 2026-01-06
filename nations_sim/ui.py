# -*- coding: utf-8 -*-
# Interface graphique avec Pygame
# Affiche la carte, le journal des événements, et les infos des nations

import pygame
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE,
    WORLD_WIDTH, WORLD_HEIGHT
)


class GameUI:
    """
    Gère toute l'interface graphique du jeu avec Pygame.
    """

    def __init__(self, world):
        """
        Initialise l'interface.

        Args:
            world (World): Le monde du jeu à afficher
        """
        # Initialisation de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🌍 Nations AI Simulator")
        self.clock = pygame.time.Clock()

        # Référence au monde
        self.world = world

        # Polices de texte
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)

        # Couleurs
        self.COLOR_BG = (30, 30, 40)  # Fond sombre
        self.COLOR_EMPTY = (80, 80, 90)  # Cases vides
        self.COLOR_BORDER = (100, 100, 110)  # Bordures
        self.COLOR_TEXT = (255, 255, 255)  # Texte blanc
        self.COLOR_PANEL = (40, 40, 50)  # Panneaux d'interface
        self.COLOR_BUTTON = (70, 130, 180)  # Boutons
        self.COLOR_BUTTON_HOVER = (100, 160, 210)  # Survol bouton

        # État de l'interface
        self.selected_nation = None  # Nation sélectionnée (clic)
        self.journal = []  # Liste des événements [(tour, texte, couleur, catégorie), ...]
        self.max_journal_lines = 20  # Nombre max de lignes affichées

        # Système de filtrage du journal
        self.journal_filter = "all"  # "all", "war", "diplomacy", "economy", "expansion", "internal"
        self.journal_categories = {
            "war": "⚔️",
            "diplomacy": "🤝",
            "economy": "💰",
            "expansion": "🗺️",
            "internal": "🏛️"
        }

        # État des boutons
        self.paused = False
        self.speed = 1  # 1, 2, ou 5

        # Système de notifications popup
        self.notifications = []  # Liste de {'text': str, 'time': float, 'color': tuple}

        # Zones de l'interface
        self.map_rect = pygame.Rect(10, 60, WORLD_WIDTH * CELL_SIZE, WORLD_HEIGHT * CELL_SIZE)
        self.journal_rect = pygame.Rect(WORLD_WIDTH * CELL_SIZE + 30, 60, 360, WORLD_HEIGHT * CELL_SIZE)
        self.info_rect = pygame.Rect(10, WORLD_HEIGHT * CELL_SIZE + 80, WINDOW_WIDTH - 20, 150)

    def add_to_journal(self, turn, text, color=(255, 255, 255), category="internal"):
        """
        Ajoute un événement au journal avec une catégorie.

        Args:
            turn (int): Numéro du tour
            text (str): Description de l'événement
            color (tuple): Couleur du texte RGB
            category (str): Catégorie de l'événement ("war", "diplomacy", "economy", "expansion", "internal")
        """
        self.journal.append((turn, text, color, category))

        # Limite le nombre de lignes (garde seulement les plus récentes)
        if len(self.journal) > 100:  # Garde 100 dans la mémoire
            self.journal = self.journal[-100:]

    def add_notification(self, text, duration=3, color=(255, 255, 255)):
        """
        Ajoute une notification popup temporaire.

        Args:
            text (str): Texte de la notification
            duration (int): Durée d'affichage en secondes
            color (tuple): Couleur du texte RGB
        """
        self.notifications.append({
            'text': text,
            'time': duration,
            'color': color
        })

    def draw(self, turn_number):
        """
        Dessine toute l'interface.

        Args:
            turn_number (int): Numéro du tour actuel
        """
        # Fond
        self.screen.fill(self.COLOR_BG)

        # Dessine les différentes parties
        self._draw_header(turn_number)
        self._draw_map()
        self._draw_journal()
        self._draw_info_panel()
        self._draw_notifications()

        # Met à jour l'affichage
        pygame.display.flip()

    def _draw_header(self, turn_number):
        """
        Dessine l'en-tête avec les contrôles et le numéro de tour.

        Args:
            turn_number (int): Numéro du tour
        """
        # Barre d'en-tête
        header_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 50)
        pygame.draw.rect(self.screen, self.COLOR_PANEL, header_rect)

        # Bouton PAUSE
        pause_text = "⏸ PAUSE" if not self.paused else "▶ PLAY"
        self._draw_button(20, 10, 120, 30, pause_text, "pause")

        # Boutons de vitesse
        self._draw_button(160, 10, 60, 30, "x1", "speed_1")
        self._draw_button(230, 10, 60, 30, "x2", "speed_2")
        self._draw_button(300, 10, 60, 30, "x5", "speed_5")

        # Numéro de tour (au centre)
        turn_text = self.font_medium.render(f"Tour: {turn_number}", True, self.COLOR_TEXT)
        turn_rect = turn_text.get_rect(center=(WINDOW_WIDTH // 2, 25))
        self.screen.blit(turn_text, turn_rect)

        # Bouton QUITTER (à droite)
        self._draw_button(WINDOW_WIDTH - 130, 10, 110, 30, "QUITTER", "quit")

    def _draw_button(self, x, y, width, height, text, button_id):
        """
        Dessine un bouton cliquable.

        Args:
            x, y (int): Position
            width, height (int): Taille
            text (str): Texte du bouton
            button_id (str): Identifiant du bouton
        """
        rect = pygame.Rect(x, y, width, height)

        # Couleur de survol si la souris est dessus
        mouse_pos = pygame.mouse.get_pos()
        color = self.COLOR_BUTTON_HOVER if rect.collidepoint(mouse_pos) else self.COLOR_BUTTON

        # Dessine le bouton
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, self.COLOR_BORDER, rect, 2, border_radius=5)

        # Texte centré
        text_surf = self.font_small.render(text, True, self.COLOR_TEXT)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def _draw_map(self):
        """
        Dessine la carte du monde (grille de territoires).
        """
        # Fond de la carte
        pygame.draw.rect(self.screen, self.COLOR_PANEL, self.map_rect)

        # Dessine chaque case
        for x in range(self.world.width):
            for y in range(self.world.height):
                nation = self.world.get_nation_at(x, y)

                # Position sur l'écran
                px = self.map_rect.x + x * CELL_SIZE
                py = self.map_rect.y + y * CELL_SIZE
                cell_rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)

                # Couleur de la case
                if nation:
                    color = nation.color
                else:
                    color = self.COLOR_EMPTY

                # Dessine la case
                pygame.draw.rect(self.screen, color, cell_rect)
                pygame.draw.rect(self.screen, self.COLOR_BORDER, cell_rect, 1)

                # Highlight si nation sélectionnée
                if nation and nation == self.selected_nation:
                    pygame.draw.rect(self.screen, (255, 255, 0), cell_rect, 3)

        # Bordure de la carte
        pygame.draw.rect(self.screen, self.COLOR_BORDER, self.map_rect, 2)

        # Légende de la carte (en bas à gauche de la carte)
        self._draw_map_legend()

    def _draw_map_legend(self):
        """
        Dessine la légende de la carte (liste des nations avec couleurs et territoires).
        """
        # Position de la légende (en bas à gauche de la carte)
        legend_x = self.map_rect.x
        legend_y = self.map_rect.bottom + 10

        # Titre de la légende
        legend_title = self.font_small.render("LÉGENDE:", True, self.COLOR_TEXT)
        self.screen.blit(legend_title, (legend_x, legend_y))

        y = legend_y + 20

        # Liste les nations vivantes
        for nation in self.world.nations:
            if nation.is_alive:
                # Carré coloré (15x15)
                color_rect = pygame.Rect(legend_x, y, 15, 15)
                pygame.draw.rect(self.screen, nation.color, color_rect)
                pygame.draw.rect(self.screen, self.COLOR_BORDER, color_rect, 1)

                # Nom + nombre de territoires
                territories = nation.get_territory_count()
                text = f"{nation.name}: {territories} territoires"
                label = self.font_small.render(text, True, self.COLOR_TEXT)
                self.screen.blit(label, (legend_x + 20, y - 2))

                y += 20

    def _draw_journal(self):
        """
        Dessine le journal des événements (à droite de la carte) avec filtres.
        """
        # Fond du journal
        pygame.draw.rect(self.screen, self.COLOR_PANEL, self.journal_rect)
        pygame.draw.rect(self.screen, self.COLOR_BORDER, self.journal_rect, 2)

        # Titre
        title = self.font_medium.render("📜 JOURNAL", True, self.COLOR_TEXT)
        self.screen.blit(title, (self.journal_rect.x + 10, self.journal_rect.y + 10))

        # Boutons de filtre (en haut du journal)
        button_y = self.journal_rect.y + 40
        button_x = self.journal_rect.x + 10

        filters = [
            ("Tous", "all"),
            ("⚔️", "war"),
            ("🤝", "diplomacy"),
            ("💰", "economy"),
            ("🗺️", "expansion")
        ]

        mouse_pos = pygame.mouse.get_pos()

        for i, (label, filter_name) in enumerate(filters):
            btn_x = button_x + i * 65
            btn_rect = pygame.Rect(btn_x, button_y, 60, 25)

            # Couleur si actif ou survol
            if self.journal_filter == filter_name:
                color = (70, 130, 180)  # Actif (bleu)
            elif btn_rect.collidepoint(mouse_pos):
                color = (60, 80, 100)  # Survol
            else:
                color = (50, 50, 60)  # Inactif

            # Dessine le bouton
            pygame.draw.rect(self.screen, color, btn_rect, border_radius=3)
            pygame.draw.rect(self.screen, self.COLOR_BORDER, btn_rect, 1, border_radius=3)

            # Texte du bouton
            text = self.font_small.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=btn_rect.center)
            self.screen.blit(text, text_rect)

        # Ligne de séparation
        pygame.draw.line(
            self.screen, self.COLOR_BORDER,
            (self.journal_rect.x + 10, self.journal_rect.y + 75),
            (self.journal_rect.right - 10, self.journal_rect.y + 75),
            1
        )

        # Filtre les événements selon la catégorie sélectionnée
        filtered_journal = self.journal
        if self.journal_filter != "all":
            filtered_journal = [
                entry for entry in self.journal
                if len(entry) >= 4 and entry[3] == self.journal_filter
            ]

        # Affiche les derniers événements filtrés (du plus récent au plus ancien)
        y_offset = self.journal_rect.y + 85
        for entry in reversed(filtered_journal[-self.max_journal_lines:]):
            if y_offset > self.journal_rect.bottom - 30:
                break

            # Extraction des données (gère les anciens formats sans catégorie)
            if len(entry) >= 4:
                turn, text, color, category = entry
            else:
                turn, text, color = entry
                category = "internal"

            # Texte de l'événement
            event_text = f"[T{turn}] {text}"
            lines = self._wrap_text(event_text, self.font_small, self.journal_rect.width - 20)

            for line in lines:
                text_surf = self.font_small.render(line, True, color)
                self.screen.blit(text_surf, (self.journal_rect.x + 10, y_offset))
                y_offset += 20

            y_offset += 5  # Espace entre les événements

    def _wrap_text(self, text, font, max_width):
        """
        Coupe un texte trop long en plusieurs lignes.

        Args:
            text (str): Texte à couper
            font (pygame.font.Font): Police
            max_width (int): Largeur max en pixels

        Returns:
            list: Liste de lignes
        """
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines if lines else [text]

    def _draw_info_panel(self):
        """
        Dessine le panneau d'informations de la nation sélectionnée (en bas).
        """
        # Fond du panneau
        pygame.draw.rect(self.screen, self.COLOR_PANEL, self.info_rect)
        pygame.draw.rect(self.screen, self.COLOR_BORDER, self.info_rect, 2)

        if self.selected_nation:
            nation = self.selected_nation

            # Titre avec le nom de la nation
            title = self.font_medium.render(f"🏛 {nation.name}", True, nation.color)
            self.screen.blit(title, (self.info_rect.x + 10, self.info_rect.y + 10))

            # Informations en colonnes
            y = self.info_rect.y + 45

            # Ligne 1: Leader, Armée, Or
            info1 = f"👑 Leader: {nation.leader_name}  |  ⚔️ Armée: {nation.army}  |  💰 Or: {nation.gold}"
            text1 = self.font_small.render(info1, True, self.COLOR_TEXT)
            self.screen.blit(text1, (self.info_rect.x + 10, y))

            # Ligne 2: Territoires, Personnalité
            y += 25
            info2 = f"📍 Territoires: {nation.get_territory_count()}  |  🎭 Personnalité: {nation.personality.capitalize()}"
            text2 = self.font_small.render(info2, True, self.COLOR_TEXT)
            self.screen.blit(text2, (self.info_rect.x + 10, y))

            # Ligne 3: Relations
            y += 25
            relations_text = "Relations: "
            for other_name, score in list(nation.relations.items())[:5]:  # Max 5 relations
                emoji = "🤝" if score > 30 else "⚔️" if score < -30 else "😐"
                relations_text += f"{emoji} {other_name}:{score:+d}  "

            text3 = self.font_small.render(relations_text, True, self.COLOR_TEXT)
            self.screen.blit(text3, (self.info_rect.x + 10, y))

        else:
            # Aucune nation sélectionnée
            msg = self.font_medium.render("Cliquez sur la carte pour sélectionner une nation", True, (150, 150, 150))
            msg_rect = msg.get_rect(center=self.info_rect.center)
            self.screen.blit(msg, msg_rect)

    def _draw_notifications(self):
        """
        Affiche les notifications popup temporaires en haut à droite.
        Les notifications s'affichent pendant quelques secondes puis disparaissent.
        """
        y = 60  # Commence juste en dessous de l'en-tête
        to_remove = []

        for i, notif in enumerate(self.notifications):
            # Prépare le texte
            text_surf = self.font_medium.render(notif['text'], True, notif['color'])
            text_rect = text_surf.get_rect()

            # Position en haut à droite
            bg_rect = pygame.Rect(
                WINDOW_WIDTH - text_rect.width - 40,
                y,
                text_rect.width + 30,
                40
            )

            # Fond semi-transparent
            bg_surf = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surf.set_alpha(200)
            bg_surf.fill((40, 40, 50))
            self.screen.blit(bg_surf, bg_rect.topleft)

            # Bordure colorée
            pygame.draw.rect(self.screen, notif['color'], bg_rect, 2, border_radius=5)

            # Texte centré
            self.screen.blit(text_surf, (bg_rect.x + 15, bg_rect.y + 10))

            # Décrémente le temps (appelé 60 fois par seconde)
            notif['time'] -= 1/60
            if notif['time'] <= 0:
                to_remove.append(i)

            y += 50  # Espace pour la notification suivante

        # Supprime les notifications expirées (en ordre inverse pour éviter les décalages d'index)
        for i in reversed(to_remove):
            self.notifications.pop(i)

    def handle_click(self, pos):
        """
        Gère un clic de souris.

        Args:
            pos (tuple): Position (x, y) du clic

        Returns:
            str: Action ("pause", "speed_1", "quit", etc.) ou None
        """
        x, y = pos

        # Clics sur les boutons de l'en-tête
        if 20 <= x <= 140 and 10 <= y <= 40:
            return "pause"
        if 160 <= x <= 220 and 10 <= y <= 40:
            return "speed_1"
        if 230 <= x <= 290 and 10 <= y <= 40:
            return "speed_2"
        if 300 <= x <= 360 and 10 <= y <= 40:
            return "speed_5"
        if WINDOW_WIDTH - 130 <= x <= WINDOW_WIDTH - 20 and 10 <= y <= 40:
            return "quit"

        # Clics sur les filtres du journal
        if self.journal_rect.collidepoint(pos):
            y_rel = y - self.journal_rect.y
            # Zone des boutons de filtre (y entre 40 et 65)
            if 40 <= y_rel <= 65:
                x_rel = x - self.journal_rect.x - 10
                if 0 <= x_rel < 60:
                    self.journal_filter = "all"
                    return None
                elif 65 <= x_rel < 125:
                    self.journal_filter = "war"
                    return None
                elif 130 <= x_rel < 190:
                    self.journal_filter = "diplomacy"
                    return None
                elif 195 <= x_rel < 255:
                    self.journal_filter = "economy"
                    return None
                elif 260 <= x_rel < 320:
                    self.journal_filter = "expansion"
                    return None

        # Clic sur la carte
        if self.map_rect.collidepoint(pos):
            # Calcule les coordonnées de la case
            cell_x = (x - self.map_rect.x) // CELL_SIZE
            cell_y = (y - self.map_rect.y) // CELL_SIZE

            # Sélectionne la nation à cette position
            nation = self.world.get_nation_at(cell_x, cell_y)
            if nation:
                self.selected_nation = nation

        return None

    def tick(self, fps=60):
        """
        Limite les FPS pour éviter de surcharger le CPU.

        Args:
            fps (int): Nombre d'images par seconde
        """
        self.clock.tick(fps)


# ===== TEST DU MODULE =====
if __name__ == "__main__":
    """
    Test de l'interface (affiche le monde sans IA).
    Lance ce fichier avec: python ui.py
    """
    from world import World

    print("🧪 Test de ui.py")
    print("⚠️ Ferme la fenêtre ou appuie sur ÉCHAP pour quitter\n")

    # Crée un monde
    world = World()
    world.generate()

    # Crée l'interface
    ui = GameUI(world)

    # Ajoute quelques événements de test au journal
    ui.add_to_journal(1, "Empire Rouge attaque République Verte!", (255, 100, 100), "war")
    ui.add_to_journal(1, "Bataille gagnée! Territoire conquis.", (100, 255, 100), "war")
    ui.add_to_journal(2, "Royaume Bleu propose alliance à Sultanat Jaune", (100, 100, 255), "diplomacy")
    ui.add_to_journal(2, "Alliance acceptée!", (100, 255, 255), "diplomacy")
    ui.add_to_journal(3, "Commerce entre nations", (255, 215, 0), "economy")
    ui.add_to_journal(3, "Expansion territoriale", (100, 255, 100), "expansion")

    # Boucle de test
    running = True
    turn = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = ui.handle_click(event.pos)
                if action == "quit":
                    running = False
                elif action:
                    print(f"Bouton cliqué: {action}")

        # Dessine
        ui.draw(turn)
        ui.tick()

    pygame.quit()
    print("✅ Test de ui.py terminé!")
