# 🌍 Nations AI Simulator

Un simulateur où **6 nations contrôlées par des LLM réels** (via Ollama) interagissent, se font la guerre, s'allient et conquièrent des territoires.

## 🎮 Ce que fait le jeu

- **6 nations avec IA** : Chaque nation a une personnalité (agressif, diplomate, marchand, etc.)
- **Décisions LLM réelles** : Les nations prennent des décisions via Ollama (pas de scripts if/else)
- **Guerres et conquêtes** : Les territoires changent de mains en direct
- **Diplomatie** : Alliances, trahisons, commerce
- **Interface temps réel** : Carte colorée + journal des événements + stats

## 🚀 Installation Rapide

### 1. Installe Ollama (moteur LLM gratuit)

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows : Télécharge depuis https://ollama.com
```

### 2. Télécharge un modèle LLM

```bash
ollama pull llama3.2
# OU si ton PC est lent :
ollama pull llama3.2:1b
```

### 3. Installe les dépendances Python

```bash
cd nations_sim
pip install -r requirements.txt
```

## ▶️ Lancer le Jeu

### Terminal 1 : Lance Ollama
```bash
ollama serve
```
> Laisse ce terminal ouvert

### Terminal 2 : Lance le jeu
```bash
cd nations_sim
python main.py
```

### Windows : Double-clic
Lance `LANCER_JEU.bat` (Ollama doit tourner avant)

## 🎮 Contrôles

| Bouton/Touche | Action |
|---------------|--------|
| **PAUSE** | Met le jeu en pause |
| **x1, x2, x5** | Change la vitesse |
| **Clic sur carte** | Sélectionne une nation |
| **ESC** | Ferme le jeu |
| **ESPACE** | Pause/Reprend |

## 📊 Ce que tu vois

### Carte (gauche)
- Chaque couleur = une nation
- Les territoires changent de couleur quand conquis

### Journal (droite)
- Décisions des nations en temps réel
- Batailles, alliances, commerce
- **POURQUOI** chaque nation agit (raisons du LLM)

### Panneau infos (bas)
- Stats de la nation sélectionnée
- Armée, or, territoires, relations

## 🏆 Conditions de Victoire

Une nation gagne si :
- Elle est la **seule survivante**
- Elle contrôle **70% de la carte**

## ⚙️ Configuration

Modifie `nations_sim/config.py` pour :
- Changer le modèle LLM (`LLM_MODEL`)
- Ajuster la vitesse (`TURN_DELAY`)
- Modifier le nombre de nations (`INITIAL_NATIONS`)

## 🐛 Problèmes Courants

**"Ollama ne répond pas"**
→ Lance `ollama serve` dans un terminal

**Jeu trop lent**
→ Change `LLM_MODEL = "llama3.2:1b"` dans `config.py`

**"No module named pygame"**
→ `pip install pygame`

## 🧠 Comment ça marche

Chaque tour (toutes les 3 secondes) :
1. **Chaque nation "réfléchit"** via Ollama (5-10 secondes par nation)
2. **Le LLM décide** : attaquer, s'allier, commercer, construire, défendre
3. **Les actions s'exécutent** : batailles, conquêtes, alliances
4. **Le monde évolue** : l'or augmente, les relations changent

Les décisions sont **vraiment prises par le LLM**, pas par des règles programmées !

## 📁 Structure du Projet

```
nations_sim/
├── config.py          # Configuration du jeu
├── prompts.py         # Templates pour le LLM
├── llm_brain.py       # Communication avec Ollama
├── nation.py          # Classe Nation
├── world.py           # Carte du monde
├── combat.py          # Système de combat
├── ui.py              # Interface Pygame
├── game.py            # Logique du jeu
├── main.py            # Point d'entrée
└── requirements.txt   # Dépendances
```

## 🎯 Fonctionnalités

- ✅ Threading asynchrone (UI fluide même pendant les décisions LLM)
- ✅ 6 nations avec personnalités distinctes
- ✅ Système de combat avec conquête de territoires
- ✅ Relations dynamiques entre nations (-100 à +100)
- ✅ Économie (or par territoire, coût des actions)
- ✅ Interface responsive (60 FPS)
- ✅ Journal des événements en temps réel
- ✅ Contrôles de vitesse (x1, x2, x5)

## 📝 Notes

- **Gratuit à 100%** : Tout tourne sur ton PC (Ollama local)
- **IA réelle** : Les décisions sont vraiment prises par un LLM
- **Fascinant** : Lis les raisons des nations, c'est la magie du jeu !

## 🤝 Contribution

Projet développé avec Claude Code pour explorer l'IA dans les jeux de stratégie.

---

**Bon jeu ! Regarde les nations se battre, s'allier et conquérir le monde ! 🌍⚔️🤝**
