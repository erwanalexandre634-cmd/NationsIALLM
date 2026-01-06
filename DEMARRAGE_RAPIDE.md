# ⚡ Démarrage Rapide - Nations AI Simulator

## 🎯 Objectif de l'Étape 1
Installer Ollama (le moteur LLM gratuit) et vérifier que tout fonctionne.

---

## 📋 Checklist d'installation

### ☑️ 1. Installer Ollama
```bash
# Sur Linux (copie-colle cette commande)
curl -fsSL https://ollama.com/install.sh | sh
```

### ☑️ 2. Télécharger un modèle IA
```bash
# Modèle recommandé (2GB, bon compromis)
ollama pull llama3.2

# OU modèle léger si ton PC rame (1.3GB)
ollama pull llama3.2:1b
```

### ☑️ 3. Lancer Ollama en arrière-plan
```bash
# Lance ça dans un terminal, garde-le ouvert
ollama serve
```

Tu devrais voir :
```
Listening on 127.0.0.1:11434
```
✅ C'est bon ! Laisse ce terminal ouvert.

### ☑️ 4. Installer les dépendances Python
```bash
# Dans un NOUVEAU terminal
cd nations_sim
pip install -r requirements.txt
```

### ☑️ 5. Tester que tout marche
```bash
python test_llm.py
```

**Résultat attendu :**
```
🔍 ÉTAPE 1: Vérification de la connexion Ollama
✅ Ollama est actif!
🤖 Test du modèle llama3.2...
✅ Réponse du LLM: {...}

🔍 ÉTAPE 2: Test d'une décision de nation

📝 PROMPT ENVOYÉ AU LLM:
[...un long texte décrivant la situation...]

🤖 Demande de décision au LLM...

✅ DÉCISION REÇUE:
   Action: attack
   Cible: République Verte
   Raison: Ils m'ont attaqué et sont affaiblis, c'est le moment

🎉 Le LLM fonctionne parfaitement!
✅ TOUS LES TESTS RÉUSSIS!
```

---

## 🎉 Si tu vois ça = SUCCÈS !

L'Étape 1 est **TERMINÉE** ! Tu as :
- ✅ Installé Ollama (moteur LLM local gratuit)
- ✅ Téléchargé un modèle IA (le "cerveau" des nations)
- ✅ Vérifié que le LLM peut prendre des décisions

**La base est solide. Les nations pourront "penser" ! 🧠**

---

## 🔧 Dépannage Express

| Problème | Solution |
|----------|----------|
| `Ollama ne répond pas` | Lance `ollama serve` dans un terminal |
| `model not found` | Lance `ollama pull llama3.2` |
| `Connection refused` | Vérifie qu'Ollama tourne avec `ollama serve` |
| Test très lent (>30s) | Change `LLM_MODEL` dans `config.py` pour `"llama3.2:1b"` |
| `No module named requests` | Lance `pip install -r requirements.txt` |

---

## 📂 Fichiers créés (Étape 1)

```
nations_sim/
├── config.py          # Configuration (modèle LLM, vitesse, etc.)
├── prompts.py         # Templates de prompts pour l'IA
├── llm_brain.py       # Communication avec Ollama
├── test_llm.py        # Script de test (lance celui-ci!)
├── requirements.txt   # Dépendances Python
└── README.md          # Documentation
```

---

## 🚀 Prochaine étape

Une fois que `test_llm.py` affiche `✅ TOUS LES TESTS RÉUSSIS!`, on peut passer à :

**Étape 2 : Créer la carte du monde**
- Grille hexagonale/carrée
- Affichage Pygame
- Génération de territoires

**Dis-moi quand tu es prêt et je commence l'Étape 2 ! 🗺️**
