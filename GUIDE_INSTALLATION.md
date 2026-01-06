# 📖 Guide d'Installation - Nations AI Simulator

## Étape 1️⃣ : Installer Ollama

### Sur Linux (recommandé)
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Sur Windows
Télécharge et installe depuis : https://ollama.com/download/windows

### Sur Mac
```bash
brew install ollama
```

---

## Étape 2️⃣ : Télécharger un modèle LLM

Après l'installation d'Ollama, télécharge un modèle IA :

### Option 1 : llama3.2 (recommandé)
```bash
ollama pull llama3.2
```
- Taille : ~2 GB
- Bon équilibre vitesse/qualité
- **Choix recommandé pour la plupart des PCs**

### Option 2 : llama3.2:1b (plus léger)
```bash
ollama pull llama3.2:1b
```
- Taille : ~1.3 GB
- Plus rapide sur les PCs faibles
- Un peu moins "intelligent" mais suffisant

### Option 3 : mistral (alternatif)
```bash
ollama pull mistral
```
- Taille : ~4 GB
- Très performant, mais plus lourd

**⏱️ Le téléchargement peut prendre 5-15 minutes selon ta connexion.**

---

## Étape 3️⃣ : Installer Python et les dépendances

### Vérifier que Python est installé
```bash
python3 --version
```
Il faut Python 3.8 ou plus récent.

### Installer les dépendances du projet
```bash
cd nations_sim
pip install -r requirements.txt
```

Cela installe :
- `requests` : pour communiquer avec Ollama
- `pygame` : pour l'interface graphique (utilisé plus tard)

---

## Étape 4️⃣ : Lancer Ollama

**IMPORTANT:** Ollama doit tourner en arrière-plan pendant que tu utilises le simulateur.

### Sur Linux/Mac
Ouvre un terminal et lance :
```bash
ollama serve
```

Laisse ce terminal ouvert. Tu verras des messages comme :
```
Listening on 127.0.0.1:11434
```

### Sur Windows
Ollama se lance automatiquement au démarrage. Tu n'as rien à faire !

---

## Étape 5️⃣ : Tester que tout fonctionne

Dans un **nouveau terminal** (garde le premier ouvert avec `ollama serve`), lance :

```bash
cd nations_sim
python test_llm.py
```

Tu devrais voir :
```
✅ Ollama est actif!
🤖 Test du modèle llama3.2...
✅ Réponse du LLM: ...
✅ DÉCISION REÇUE:
   Action: attack
   Cible: République Verte
   Raison: Ils sont affaiblis après leur attaque ratée
🎉 Le LLM fonctionne parfaitement!
```

Si tu vois ça, **BRAVO !** L'étape 1 est terminée ! 🎉

---

## ❌ Problèmes courants

### "Ollama ne répond pas"
**Cause :** Ollama n'est pas lancé
**Solution :** Lance `ollama serve` dans un terminal

### "Connection refused" ou "localhost:11434"
**Cause :** Ollama n'est pas démarré
**Solution :** Vérifie que `ollama serve` tourne

### "model 'llama3.2' not found"
**Cause :** Le modèle n'est pas téléchargé
**Solution :** Lance `ollama pull llama3.2`

### Le test est très lent (>30 secondes)
**Cause :** Ton PC est peut-être un peu faible pour le modèle
**Solution :**
1. Édite `config.py`
2. Change `LLM_MODEL = "llama3.2"` en `LLM_MODEL = "llama3.2:1b"`
3. Télécharge le modèle plus léger : `ollama pull llama3.2:1b`

### "No module named 'requests'"
**Cause :** Les dépendances Python ne sont pas installées
**Solution :** `pip install -r requirements.txt`

---

## 📁 Structure du projet après installation

```
nations_sim/
├── config.py          ✅ Configuration du jeu
├── prompts.py         ✅ Templates pour le LLM
├── llm_brain.py       ✅ Communication avec Ollama
├── test_llm.py        ✅ Script de test
├── requirements.txt   ✅ Dépendances Python
├── README.md          ✅ Documentation
├── .gitignore         ✅ Fichiers ignorés par git
│
├── nation.py          ⏳ (Prochaine étape)
├── world.py           ⏳ (Prochaine étape)
└── main.py            ⏳ (Prochaine étape)
```

---

## ✅ Prochaines étapes

Une fois que `test_llm.py` fonctionne, tu es prêt pour :
1. **Étape 2** : Créer la carte du monde
2. **Étape 3** : Créer les nations et la boucle de jeu
3. **Étape 4** : Implémenter les actions (guerre, alliance, etc.)
4. **Étape 5** : Interface graphique
5. **Étape 6** : Compilation en .exe

**Continue avec confiance ! La base est solide. 🚀**
