# ✅ GUIDE DE TEST - Bugs Corrigés

## 🎯 3 Bugs Critiques Corrigés

Ce guide te permet de vérifier que les 3 bugs critiques sont bien corrigés :
1. **BUG 1 - UI FREEZE** : Interface bloquée pendant les décisions LLM
2. **BUG 2 - NATIONS SANS VOISINS** : Nations trop éloignées
3. **BUG 3 - TARGETS INVALIDES** : LLM invente des noms de nations

---

## 🧪 TEST 1 : Vérifier les Nations Adjacentes (BUG 2)

### Commande :
```bash
cd nations_sim
python world.py
```

### Résultat ATTENDU :
```
🌍 Génération du monde...
✅ 6 nations créées
✅ Monde généré avec succès!

📊 Statistiques du monde:
   Taille: 20x15 = 300 cases
   Nations: 6

🗺️ Nations créées:
   - Empire Rouge (agressif): 12 territoires
     Voisins: République Verte, Royaume Bleu      ✅ AU MOINS 2 VOISINS
   - République Verte (marchand): 12 territoires
     Voisins: Empire Rouge, Royaume Bleu, Sultanat Jaune  ✅ AU MOINS 2 VOISINS
   [...]
```

### ✅ CRITÈRE DE RÉUSSITE :
- **Chaque nation a AU MOINS 2 voisins**
- **Aucune nation avec "Voisins: Aucun"**

---

## 🧪 TEST 2 : Vérifier l'UI Responsive (BUG 1)

### Commande :
```bash
cd nations_sim
python main.py
```

### Procédure de Test :

1. **Le jeu démarre** → Une fenêtre Pygame s'ouvre
2. **Attends 2 secondes** → Tu vois "[Nation] réfléchit..." dans le journal
3. **PENDANT QUE LES NATIONS RÉFLÉCHISSENT :**
   - ✅ Clique sur le bouton **PAUSE**
   - ✅ Clique sur le bouton **x2**
   - ✅ Clique sur le bouton **x5**
   - ✅ Clique sur la carte pour sélectionner une nation
   - ✅ Déplace la souris (le curseur doit être fluide)

### ✅ CRITÈRES DE RÉUSSITE :
- **La fenêtre NE FREEZE JAMAIS** (même pendant les décisions)
- **Tu peux cliquer sur PAUSE immédiatement** (réaction instantanée)
- **Le journal s'affiche en temps réel** avec "[Nation] réfléchit..."
- **Les décisions arrivent progressivement** (pas toutes d'un coup)

### ❌ ÉCHEC si :
- La fenêtre freeze pendant 5-10 secondes
- Tu ne peux pas cliquer pendant que les nations pensent
- Le curseur se transforme en sablier Windows

---

## 🧪 TEST 3 : Vérifier les Targets Valides (BUG 3)

### Commande :
```bash
cd nations_sim
python main.py
```

### Procédure de Test :

1. **Lance le jeu**
2. **Laisse tourner 5-10 tours**
3. **Lis le journal à droite**

### Résultat ATTENDU :

Le journal doit afficher des messages comme :
```
[Tour 3] Empire Rouge: attack → République Verte (Ils sont faibles)
⚔️ Empire Rouge conquiert (8,5) de République Verte!

[Tour 4] Royaume Bleu: ally → Sultanat Jaune (Alliance stratégique)
🤝 Royaume Bleu et Sultanat Jaune forment une alliance!

[Tour 5] République Verte: trade → Empire Rouge (Or nécessaire)
💰 République Verte commerce avec Empire Rouge (+30 or chacun)
```

### ✅ CRITÈRES DE RÉUSSITE :
- **Tous les noms de cibles sont valides** :
  - Empire Rouge ✅
  - République Verte ✅
  - Royaume Bleu ✅
  - Sultanat Jaune ✅
  - Empire Violet ✅
  - Principauté Orange ✅

### ❌ ÉCHEC si tu vois :
```
❌ Cible invalide: Sultanat de Roumana n'existe pas ou est morte
❌ Cible invalide: Principauté Bleue n'existe pas ou est morte
❌ Cible invalide: Empire Azur n'existe pas ou est morte
```

---

## 🧪 TEST 4 : Test de Stabilité (20+ tours)

### Commande :
```bash
cd nations_sim
python main.py
```

### Procédure :

1. **Lance le jeu**
2. **Clique sur x5** (vitesse rapide)
3. **Laisse tourner pendant 5 minutes** (environ 20-30 tours)

### ✅ CRITÈRES DE RÉUSSITE :
- Le jeu **ne crash pas**
- L'UI reste **fluide** (60 FPS)
- Les décisions **continuent à arriver**
- La carte **se met à jour** (territoires changent de couleur)
- Le journal **s'affiche correctement**

---

## 🎮 TEST 5 : Test des Contrôles

### Procédure :

Pendant que le jeu tourne, teste TOUS les contrôles :

| Action | Test | Résultat attendu |
|--------|------|------------------|
| **Clic PAUSE** | Clique pendant une décision LLM | ✅ Pause immédiate |
| **Clic x1** | Change la vitesse | ✅ Affiche "Vitesse: x1" |
| **Clic x2** | Change la vitesse | ✅ Affiche "Vitesse: x2" |
| **Clic x5** | Change la vitesse | ✅ Affiche "Vitesse: x5" |
| **Clic carte** | Clique sur un territoire | ✅ Sélectionne la nation |
| **ESC** | Appuie sur Échap | ✅ Ferme le jeu |
| **ESPACE** | Appuie sur Espace | ✅ Pause/Reprend |

---

## 📊 CHECKLIST FINALE

Coche toutes les cases pour valider que les bugs sont corrigés :

### BUG 1 - UI FREEZE :
- [ ] La fenêtre ne freeze jamais
- [ ] Je peux cliquer sur PAUSE pendant les décisions LLM
- [ ] Le curseur est fluide en permanence
- [ ] Le journal affiche "[Nation] réfléchit..." en temps réel
- [ ] Les boutons répondent instantanément

### BUG 2 - NATIONS SANS VOISINS :
- [ ] Chaque nation a AU MOINS 2 voisins (test `python world.py`)
- [ ] Aucune nation affiche "Voisins: Aucun"
- [ ] Les nations peuvent s'attaquer mutuellement
- [ ] Des conquêtes de territoires ont lieu

### BUG 3 - TARGETS INVALIDES :
- [ ] Aucun message "Cible invalide" dans le journal
- [ ] Tous les noms de cibles existent réellement
- [ ] Les attaques réussissent (pas d'erreur de target)

### STABILITÉ :
- [ ] Le jeu tourne sans crash pendant 20+ tours
- [ ] L'interface reste fluide (60 FPS)
- [ ] La mémoire ne sature pas (pas de leak)

---

## ⚠️ SI UN TEST ÉCHOUE

### BUG 1 toujours présent (UI freeze) :
**Symptôme :** La fenêtre freeze encore
**Vérification :** Regarde la console, tu devrais voir "✅ [Nation] a décidé"
**Solution :** Vérifie que `game.py` utilise bien le threading

### BUG 2 toujours présent (pas de voisins) :
**Symptôme :** Nations avec "Voisins: Aucun"
**Vérification :** Lance `python world.py` plusieurs fois
**Solution :** Vérifie que `world.py` utilise bien les régions fixes

### BUG 3 toujours présent (targets invalides) :
**Symptôme :** Messages "Cible invalide" dans le journal
**Vérification :** Regarde le prompt envoyé au LLM (console)
**Solution :** Vérifie que le prompt contient "NATIONS EXISTANTES"

---

## 🎉 SI TOUS LES TESTS PASSENT

**FÉLICITATIONS !** 🎊

Les 3 bugs critiques sont corrigés :
- ✅ **UI fluide et responsive** (pas de freeze)
- ✅ **Nations adjacentes** (peuvent s'attaquer)
- ✅ **Targets toujours valides** (pas de noms inventés)

**Le jeu est maintenant JOUABLE et AGRÉABLE !**

Tu peux maintenant :
1. **Laisser tourner le jeu et observer** les décisions des LLM
2. **Expérimenter avec les vitesses** (x1, x2, x5)
3. **Sélectionner des nations** pour voir leurs stats
4. **Profiter du spectacle** des guerres et alliances ! ⚔️🤝

---

## 📝 NOTES IMPORTANTES

### Performance normale :
- **Chaque décision LLM prend 3-10 secondes** (c'est normal)
- **Les décisions arrivent progressivement** (pas toutes d'un coup)
- **Le journal se remplit au fur et à mesure**

### Si c'est trop lent :
- Change le modèle dans `config.py` :
  ```python
  LLM_MODEL = "llama3.2:1b"  # Plus rapide
  ```
- Puis télécharge-le :
  ```bash
  ollama pull llama3.2:1b
  ```

### Console de debug :
Pendant que le jeu tourne, regarde la console pour voir :
```
🏛️ Empire Rouge réfléchit...
✅ Empire Rouge a décidé: attack → République Verte
⚔️ Bataille: Empire Rouge vs République Verte
```

---

**Bon test ! 🧪**
