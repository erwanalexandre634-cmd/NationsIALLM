# 🚀 COMMENT LANCER LE JEU

## ✅ CHECKLIST AVANT DE LANCER

### 1️⃣ Ollama doit être installé et lancé

**Installation (si pas encore fait) :**
```bash
# Sur Linux
curl -fsSL https://ollama.com/install.sh | sh

# Télécharge le modèle LLM
ollama pull llama3.2
```

**Lancer Ollama :**
```bash
# IMPORTANT: Lance ça dans un terminal et laisse-le ouvert
ollama serve
```

Tu devrais voir :
```
Listening on 127.0.0.1:11434
```

✅ **Laisse ce terminal ouvert pendant que tu joues!**

---

### 2️⃣ Dépendances Python installées

```bash
cd nations_sim
pip install -r requirements.txt
```

Cela installe :
- `requests` (pour communiquer avec Ollama)
- `pygame` (pour l'interface graphique)

---

## 🎮 LANCER LE JEU

### Méthode 1 : Directement avec Python

```bash
cd nations_sim
python main.py
```

### Méthode 2 : Depuis Windows (double-clic)

Si tu es sur Windows, tu peux créer un fichier `LANCER_JEU.bat` :

```batch
@echo off
cd nations_sim
python main.py
pause
```

Ensuite, double-clique sur `LANCER_JEU.bat`.

---

## 🎯 CE QUI SE PASSE QUAND TU LANCES

1. **Vérification d'Ollama**
   - Le jeu vérifie qu'Ollama est lancé
   - Si pas lancé → message d'erreur

2. **Génération du monde**
   - Crée 6 nations avec des personnalités aléatoires
   - Place les territoires sur la carte

3. **Lancement de l'interface**
   - Une fenêtre Pygame s'ouvre (1200x800 pixels)
   - Tu vois la carte colorée avec les nations

4. **Le jeu démarre automatiquement**
   - Chaque tour (toutes les 3 secondes par défaut)
   - Les nations prennent des décisions via le LLM
   - Tu vois les actions dans le journal à droite

---

## 🎮 CONTRÔLES DU JEU

| Bouton/Touche | Action |
|---------------|--------|
| **PAUSE** | Met le jeu en pause/reprend |
| **x1** | Vitesse normale (1 tour toutes les 3s) |
| **x2** | Vitesse rapide (1 tour toutes les 1.5s) |
| **x5** | Vitesse très rapide (1 tour toutes les 0.6s) |
| **Clic sur la carte** | Sélectionne une nation pour voir ses infos |
| **QUITTER** | Ferme le jeu |
| **ESC** | Ferme le jeu |
| **ESPACE** | Pause/Reprend (raccourci clavier) |

---

## 📊 COMMENT LIRE L'INTERFACE

### Carte (à gauche)
- Chaque couleur = une nation
- Clic sur un territoire = voir les infos de cette nation

### Journal (à droite)
Les événements s'affichent en temps réel :
```
[T5] Empire Rouge: attack → République Verte (Ils sont faibles)
⚔️ Empire Rouge conquiert (12,7) de République Verte!
[T5] République Verte: build_army (Je dois me défendre)
⚔️ République Verte recrute des troupes (+20 armée)
```

### Panneau d'infos (en bas)
Quand tu sélectionnes une nation :
- 👑 Leader / ⚔️ Armée / 💰 Or
- 📍 Nombre de territoires / 🎭 Personnalité
- Relations avec les autres nations

---

## 🏁 CONDITIONS DE VICTOIRE

Une nation gagne si :
1. **Elle est la seule survivante** (toutes les autres éliminées)
2. **Elle contrôle 70% de la carte** (domination totale)

Le jeu se met automatiquement en pause à la fin.

---

## ⚠️ PROBLÈMES COURANTS

### ❌ "Ollama ne répond pas!"
**Solution :**
1. Ouvre un nouveau terminal
2. Lance `ollama serve`
3. Relance le jeu

### ❌ "No module named 'pygame'"
**Solution :**
```bash
pip install pygame
```

### ❌ "No module named 'requests'"
**Solution :**
```bash
pip install requests
```

### ❌ Le jeu est très lent (>10s par tour)
**Causes possibles :**
1. Ton PC est un peu faible pour `llama3.2`
2. Ollama met du temps à répondre

**Solutions :**
1. Change le modèle dans `config.py` :
   ```python
   LLM_MODEL = "llama3.2:1b"  # Plus léger
   ```
2. Télécharge le modèle plus léger :
   ```bash
   ollama pull llama3.2:1b
   ```

### ❌ La fenêtre se fige
**Cause :** Pygame a crashé ou Ollama ne répond plus

**Solution :**
1. Ferme le jeu (ESC ou ferme la fenêtre)
2. Vérifie qu'Ollama tourne toujours
3. Relance le jeu

### ❌ Erreur "target invalide"
**Cause :** Le LLM a donné un nom de nation qui n'existe pas

**Solution :** Normal, le jeu gère cette erreur automatiquement. La nation ne fera rien ce tour-là.

---

## 🎉 PROFITE DU JEU!

Laisse tourner le jeu et observe les nations interagir :
- Les nations agressives attaquent
- Les nations diplomates forment des alliances
- Les nations marchandes commercent
- Les nations paranoïaques se défendent

**C'est fascinant de voir les décisions du LLM!** 🧠

---

## 📝 NOTES IMPORTANTES

1. **Ollama DOIT tourner** avant de lancer le jeu
2. **Chaque tour prend quelques secondes** (le LLM réfléchit)
3. **Le journal est la partie la plus intéressante** (lis les raisons!)
4. **Tu peux mettre en pause** pour lire tranquillement
5. **Le jeu est déterministe sauf l'aléatoire des combats**

---

## 🐛 RAPPORT DE BUGS

Si tu rencontres un problème :
1. Note l'erreur exacte
2. Vérifie qu'Ollama tourne
3. Regarde la console pour les messages d'erreur

Le jeu ne devrait PAS crasher. S'il crashe, c'est probablement :
- Ollama qui s'est arrêté
- Une erreur réseau
- Un problème de parsing JSON du LLM (déjà géré normalement)

---

**Bon jeu! 🌍⚔️🤝**
