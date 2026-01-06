# Configuration du simulateur Nations AI

# ===== LLM Configuration =====
OLLAMA_URL = "http://localhost:11434"  # URL par défaut d'Ollama
LLM_MODEL = "llama3.2"  # Le modèle à utiliser (change si tu as pris llama3.2:1b)
LLM_TEMPERATURE = 0.7  # Créativité de l'IA (0.0 = robotique, 1.0 = créatif)

# ===== Monde =====
WORLD_WIDTH = 20  # Largeur de la carte en cases
WORLD_HEIGHT = 15  # Hauteur de la carte
INITIAL_NATIONS = 6  # Nombre de nations au départ

# ===== Jeu =====
TURN_DELAY = 3  # Secondes entre chaque tour (3s = tu peux lire les événements)
INITIAL_ARMY = 50  # Armée de départ pour chaque nation
INITIAL_GOLD = 200  # Or de départ
GOLD_PER_TERRITORY = 10  # Or gagné par territoire possédé, chaque tour
ARMY_COST = 5  # Coût en or pour recruter 10 soldats

# ===== Combat =====
ATTACK_COST_GOLD = 20  # Coût en or pour attaquer
ATTACK_COST_ARMY = 10  # Soldats perdus en attaquant (même si tu gagnes)

# ===== Interface =====
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CELL_SIZE = 40  # Taille d'une case en pixels

# ===== Personnalités disponibles =====
PERSONALITIES = {
    "agressif": "Tu aimes conquérir et dominer. La guerre t'excite, tu veux être le plus puissant.",
    "diplomate": "Tu préfères négocier et créer des alliances. La paix est plus profitable que la guerre.",
    "marchand": "L'or est ta priorité. Tu veux commercer et t'enrichir avant tout.",
    "paranoïaque": "Tu te méfies de tous. Tu veux une armée forte pour te défendre.",
    "opportuniste": "Tu attaques les faibles et évites les forts. Tu suis toujours ton intérêt."
}

# ===== Couleurs des nations (Rouge, Vert, Bleu, Jaune, Violet, Orange) =====
NATION_COLORS = [
    (220, 50, 50),   # Rouge
    (50, 200, 50),   # Vert
    (50, 100, 220),  # Bleu
    (230, 200, 50),  # Jaune
    (180, 50, 200),  # Violet
    (255, 140, 50),  # Orange
]

# ===== Noms des nations (générés aléatoirement) =====
NATION_NAMES = [
    "Empire Rouge",
    "République Verte",
    "Royaume Bleu",
    "Sultanat Jaune",
    "Empire Violet",
    "Principauté Orange"
]
