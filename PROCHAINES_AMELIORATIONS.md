# 🎨 Prochaines Améliorations - Guide Détaillé

Ce guide détaille les améliorations restantes à implémenter pour rendre le jeu encore plus agréable.

## ✅ Déjà Fait

- [x] **Nettoyage GitHub** - Fichiers obsolètes supprimés
- [x] **Nations adjacentes** - Grille 3x2 collée garantie
- [x] **Conquête du vide** - Action "expand" implémentée
- [x] **README propre** - Documentation claire
- [x] **Journal avec filtres** - 5 catégories cliquables (⚔️🤝💰🗺️🏛️)
- [x] **Prompt immersif** - Raisons contextuelles et narratives
- [x] **Légende carte** - Nations avec couleurs et territoires
- [x] **Notifications popup** - Événements importants en temps réel

---

## 🎯 À Implémenter

### 1️⃣ JOURNAL AVEC FILTRES (Priorité HAUTE)

#### Problème Actuel
Le journal affiche tout en vrac. Impossible de suivre un type d'événement spécifique.

#### Solution
Créer un système de catégories et filtres.

#### Fichier à Modifier: `ui.py`

**Étape A: Ajouter les catégories**

Dans la classe `GameUI.__init__()`:
```python
self.journal_filter = "all"  # "all", "wars", "diplomacy", "economy"
self.journal_categories = {
    "war": "⚔️",
    "diplomacy": "🤝",
    "economy": "💰",
    "expansion": "🗺️",
    "internal": "🏛️"
}
```

**Étape B: Modifier `add_to_journal()`**

Ajouter un paramètre `category`:
```python
def add_to_journal(self, turn, text, color, category="internal"):
    """
    Args:
        category (str): "war", "diplomacy", "economy", "expansion", "internal"
    """
    self.journal.append((turn, text, color, category))
```

**Étape C: Créer les boutons de filtre**

Dans `_draw_journal()`:
```python
# Position des boutons (en haut du journal)
button_y = self.journal_rect.y + 40
button_x = self.journal_rect.x + 10

# Boutons de filtre
filters = [
    ("Tous", "all"),
    ("⚔️", "war"),
    ("🤝", "diplomacy"),
    ("💰", "economy")
]

for i, (label, filter_name) in enumerate(filters):
    btn_x = button_x + i * 70
    btn_rect = pygame.Rect(btn_x, button_y, 60, 25)

    # Couleur si actif
    color = (70, 130, 180) if self.journal_filter == filter_name else (50, 50, 60)

    pygame.draw.rect(self.screen, color, btn_rect, border_radius=3)
    text = self.font_small.render(label, True, (255, 255, 255))
    self.screen.blit(text, (btn_x + 5, button_y + 5))
```

**Étape D: Gérer les clics sur les filtres**

Dans `handle_click()`:
```python
# Clic sur filtres journal
if self.journal_rect.collidepoint(pos):
    # Zone des boutons
    if 40 <= y - self.journal_rect.y <= 65:
        x_rel = x - self.journal_rect.x - 10
        if 0 <= x_rel < 70:
            self.journal_filter = "all"
        elif 70 <= x_rel < 140:
            self.journal_filter = "war"
        elif 140 <= x_rel < 210:
            self.journal_filter = "diplomacy"
        elif 210 <= x_rel < 280:
            self.journal_filter = "economy"
```

**Étape E: Filtrer l'affichage**

Dans `_draw_journal()`, avant d'afficher:
```python
# Filtre les événements
filtered_journal = self.journal
if self.journal_filter != "all":
    filtered_journal = [
        entry for entry in self.journal
        if len(entry) >= 4 and entry[3] == self.journal_filter
    ]

# Affiche les 20 derniers
for i, entry in enumerate(reversed(filtered_journal[-20:])):
    ...
```

**Étape F: Mettre à jour game.py**

Dans toutes les actions, ajouter la catégorie:
```python
# Exemple pour attaque
self.ui.add_to_journal(self.turn_number, result_text, color, "war")

# Exemple pour alliance
self.ui.add_to_journal(self.turn_number, result_text, color, "diplomacy")

# Exemple pour commerce
self.ui.add_to_journal(self.turn_number, result_text, (255, 215, 0), "economy")

# Exemple pour expansion
self.ui.add_to_journal(self.turn_number, result_text, (100, 255, 100), "expansion")
```

---

### 2️⃣ PANNEAU NATION DÉTAILLÉ (Priorité MOYENNE)

#### Solution
Quand on clique sur une nation, ouvrir un panneau popup avec toutes les infos.

#### Fichier à Modifier: `ui.py`

**Étape A: Variable pour le panneau**

Dans `__init__()`:
```python
self.detail_panel_open = False
self.detail_panel_nation = None
```

**Étape B: Créer la fonction de dessin**

```python
def _draw_detail_panel(self, nation):
    """Affiche un panneau détaillé pour une nation"""
    # Fond semi-transparent
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    self.screen.blit(overlay, (0, 0))

    # Panneau centré
    panel_rect = pygame.Rect(200, 100, 800, 600)
    pygame.draw.rect(self.screen, (40, 40, 50), panel_rect, border_radius=10)
    pygame.draw.rect(self.screen, (100, 100, 110), panel_rect, 3, border_radius=10)

    # Bouton fermer
    close_btn = pygame.Rect(panel_rect.right - 40, panel_rect.y + 10, 30, 30)
    pygame.draw.rect(self.screen, (180, 50, 50), close_btn, border_radius=5)
    close_text = self.font_medium.render("X", True, (255, 255, 255))
    self.screen.blit(close_text, (close_btn.x + 8, close_btn.y + 3))

    # Titre
    title = self.font_large.render(f"🏛 {nation.name}", True, nation.color)
    self.screen.blit(title, (panel_rect.x + 20, panel_rect.y + 20))

    # Stats (armée, or, territoires)
    y = panel_rect.y + 70
    stats_text = [
        f"⚔️ Armée: {nation.army}/100",
        f"💰 Or: {nation.gold}",
        f"📍 Territoires: {nation.get_territory_count()}",
        f"🎭 Personnalité: {nation.personality.capitalize()}"
    ]

    for stat in stats_text:
        text = self.font_medium.render(stat, True, (255, 255, 255))
        self.screen.blit(text, (panel_rect.x + 20, y))
        y += 30

    # Relations
    y += 20
    relations_title = self.font_medium.render("🤝 Relations:", True, (255, 255, 255))
    self.screen.blit(relations_title, (panel_rect.x + 20, y))
    y += 30

    for other_name, score in nation.relations.items():
        emoji = "🟢" if score > 30 else "🔴" if score < -30 else "🟡"
        rel_text = f"{emoji} {other_name}: {score:+d}"
        text = self.font_small.render(rel_text, True, (255, 255, 255))
        self.screen.blit(text, (panel_rect.x + 40, y))
        y += 25
```

**Étape C: Ouvrir/fermer le panneau**

Dans `handle_click()`:
```python
# Double-clic sur la carte = ouvrir panneau
if self.map_rect.collidepoint(pos):
    cell_x = (x - self.map_rect.x) // CELL_SIZE
    cell_y = (y - self.map_rect.y) // CELL_SIZE
    nation = self.world.get_nation_at(cell_x, cell_y)

    if nation:
        # Simple clic = sélection
        self.selected_nation = nation

        # Double-clic = panneau détaillé (à gérer avec pygame.MOUSEBUTTONDBLCLK)
        # Ou utiliser un bouton "Détails" dans le panneau info
```

---

### 3️⃣ PROMPT PLUS IMMERSIF (Priorité HAUTE)

#### Fichier à Modifier: `prompts.py`

**Remplacer le SYSTEM_PROMPT par:**

```python
SYSTEM_PROMPT = """Tu es l'intelligence artificielle qui contrôle une nation dans un jeu de stratégie médiéval.
Tu incarnes VRAIMENT ton leader avec sa personnalité unique.

RÈGLES IMPORTANTES:
1. Prends des décisions STRATÉGIQUES basées sur la situation
2. Tes raisons doivent être des PHRASES COMPLÈTES et IMMERSIVES
3. Utilise le nom EXACT des nations (copie-colle de la liste fournie)
4. Pense à LONG TERME: alliances, vengeances, opportunités

EXEMPLES DE BONNES RAISONS (immersives et contextuelles):
- "Le Royaume Bleu m'a trahi au tour 5. Il est temps de me venger et de reprendre mes territoires"
- "La République Verte est mon fidèle allié depuis le début. Je dois l'aider contre notre ennemi commun"
- "Mon trésor est vide après la guerre. Le commerce avec le Sultanat me permettra de reconstruire mon armée"
- "L'Empire Violet est affaibli par sa guerre contre le Royaume Bleu. C'est le moment parfait pour attaquer"
- "J'ai assez de territoires. Je vais fortifier mes frontières avant la prochaine attaque"

EXEMPLES DE MAUVAISES RAISONS (à ÉVITER):
- "Attaquer pour défendre" (incohérent)
- "Action stratégique" (trop vague, sans contexte)
- "Construire armée" (pas de phrase, pas de raison)
- "Pour gagner" (évident, pas utile)

Réponds UNIQUEMENT en JSON valide, sans texte avant ou après:
{
  "action": "attack/ally/trade/build_army/defend/expand/nothing",
  "target": "nom_exact_de_la_nation ou null",
  "reason": "ta justification COMPLÈTE et IMMERSIVE en 10-20 mots"
}"""
```

---

### 4️⃣ LÉGENDE DE LA CARTE (Priorité BASSE)

#### Fichier à Modifier: `ui.py`

**Dans `_draw_map()`, ajouter après la carte:**

```python
# Légende (en bas à gauche de la carte)
legend_x = self.map_rect.x
legend_y = self.map_rect.bottom + 10

legend_title = self.font_small.render("LÉGENDE:", True, (255, 255, 255))
self.screen.blit(legend_title, (legend_x, legend_y))

y = legend_y + 20
for nation in self.world.nations:
    if nation.is_alive:
        # Carré coloré
        color_rect = pygame.Rect(legend_x, y, 15, 15)
        pygame.draw.rect(self.screen, nation.color, color_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), color_rect, 1)

        # Nom + nombre de territoires
        text = f"{nation.name}: {nation.get_territory_count()}"
        label = self.font_small.render(text, True, (255, 255, 255))
        self.screen.blit(label, (legend_x + 20, y))

        y += 20
```

---

### 5️⃣ NOTIFICATIONS POPUP (Priorité MOYENNE)

#### Solution
Afficher des notifications temporaires pour les événements importants.

#### Fichier à Modifier: `ui.py`

**Étape A: Structure de notification**

Dans `__init__()`:
```python
self.notifications = []  # Liste de (texte, temps_restant, couleur)
```

**Étape B: Ajouter une notification**

```python
def add_notification(self, text, duration=3, color=(255, 255, 255)):
    """
    Args:
        duration (int): Durée en secondes
    """
    self.notifications.append({
        'text': text,
        'time': duration,
        'color': color
    })
```

**Étape C: Afficher et mettre à jour**

```python
def _draw_notifications(self):
    """Affiche les notifications en haut à droite"""
    y = 60
    to_remove = []

    for i, notif in enumerate(self.notifications):
        # Fond semi-transparent
        text_surf = self.font_medium.render(notif['text'], True, notif['color'])
        text_rect = text_surf.get_rect()

        bg_rect = pygame.Rect(
            WINDOW_WIDTH - text_rect.width - 40,
            y,
            text_rect.width + 30,
            40
        )

        # Fond
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surf.set_alpha(200)
        bg_surf.fill((40, 40, 50))
        self.screen.blit(bg_surf, bg_rect.topleft)

        # Bordure
        pygame.draw.rect(self.screen, notif['color'], bg_rect, 2, border_radius=5)

        # Texte
        self.screen.blit(text_surf, (bg_rect.x + 15, bg_rect.y + 10))

        # Décrémente le temps
        notif['time'] -= 1/60  # Appelé 60 fois par seconde
        if notif['time'] <= 0:
            to_remove.append(i)

        y += 50

    # Supprime les notifications expirées
    for i in reversed(to_remove):
        self.notifications.pop(i)
```

**Dans `draw()`, appeler:**
```python
self._draw_notifications()
```

**Étape D: Utiliser dans game.py**

```python
# Lors d'une guerre déclarée
self.ui.add_notification(f"⚔️ {attacker.name} attaque {target.name}!", 4, (255, 100, 100))

# Lors d'une alliance
self.ui.add_notification(f"🤝 {nation1.name} et {nation2.name} s'allient!", 4, (100, 255, 255))

# Lors d'une victoire
self.ui.add_notification(f"🏆 {winner.name} GAGNE!", 10, (255, 215, 0))
```

---

## 📝 Ordre d'Implémentation Recommandé

1. **Journal avec filtres** (30 min) → Améliore immédiatement la lisibilité
2. **Prompt plus immersif** (5 min) → Raisons plus intéressantes
3. **Notifications popup** (20 min) → Événements importants visibles
4. **Légende carte** (10 min) → Aide à comprendre qui est qui
5. **Panneau détaillé** (40 min) → Bonus pour les curieux

**Total estimé: ~2h de développement**

---

## 🧪 Tests Après Implémentation

### Test du Journal
```bash
python main.py
```
1. Clique sur [⚔️] → Doit afficher seulement les guerres
2. Clique sur [🤝] → Doit afficher seulement les alliances
3. Clique sur [💰] → Doit afficher seulement l'économie

### Test des Notifications
1. Attends qu'une nation attaque
2. Une notification doit apparaître en haut à droite
3. Elle doit disparaître après 3-4 secondes

### Test du Prompt
1. Lis les raisons dans le journal
2. Elles doivent être des phrases complètes
3. Exemples: "Je me venge de..." au lieu de "Attaque stratégique"

---

## 💡 Idées Bonus (Si Tu as du Temps)

- **Statistiques globales** : Afficher "Guerres actives: 2", "Alliances: 3"
- **Mode replay** : Sauvegarde de la partie pour la rejouer
- **Graphiques** : Évolution des territoires dans le temps
- **Sons** : Bruitages pour les batailles/alliances
- **Personnalisation** : Choisir les noms/couleurs avant de commencer

---

## 🎉 Session de Développement Complétée

### Améliorations Implémentées (2h de dev)

**1. Journal avec Filtres ✅**
- 5 boutons de filtrage cliquables (Tous, ⚔️Guerre, 🤝Diplo, 💰Éco, 🗺️Expansion)
- Catégorisation automatique de tous les événements
- Filtrage en temps réel avec highlight du filtre actif
- Rétrocompatibilité avec anciens événements

**2. Prompt LLM Immersif ✅**
- SYSTEM_PROMPT enrichi avec exemples concrets
- 5 exemples de bonnes raisons contextuelles
- 4 exemples de mauvaises raisons à éviter
- Longueur augmentée à 10-20 mots pour plus de détails

**3. Légende de la Carte ✅**
- Affichage dynamique des nations vivantes
- Carré coloré + nom + nombre de territoires
- Position en bas à gauche de la carte
- Mise à jour automatique quand une nation est éliminée

**4. Notifications Popup ✅**
- Système de notifications temporaires en haut à droite
- Notifications pour: attaques, éliminations, alliances, victoire
- Fond semi-transparent avec bordure colorée
- Durées personnalisées (3-10 secondes)
- Disparition automatique et empilage vertical

### Résultat Final

Le jeu est maintenant **beaucoup plus lisible et agréable**:
- ✅ Journal organisé et filtrable
- ✅ Raisons IA plus narratives et immersives
- ✅ Événements importants visibles instantanément
- ✅ Identification rapide des nations sur la carte

**Le simulateur Nations AI est maintenant COMPLET et FONCTIONNEL ! 🌍⚔️🤝**

---

**Bon jeu ! Regarde les nations se battre, s'allier et conquérir le monde ! 🚀**
