# 🌍 Nations AI Simulator

Un simulateur où des nations contrôlées par de **vrais LLM** (via Ollama) interagissent entre elles.

## 🚀 Installation rapide

### 1. Installer Ollama
```bash
# Sur Linux
curl -fsSL https://ollama.com/install.sh | sh

# Télécharger le modèle LLM (choisis-en un)
ollama pull llama3.2        # Recommandé (2GB)
ollama pull llama3.2:1b     # Plus léger (1.3GB)
```

### 2. Installer les dépendances Python
```bash
cd nations_sim
pip install -r requirements.txt
```

### 3. Lancer Ollama
```bash
# Dans un terminal séparé, lance:
ollama serve
```

### 4. Tester que tout fonctionne
```bash
python llm_brain.py
```

Tu devrais voir:
```
✅ Ollama est actif!
🤖 Test du modèle llama3.2...
✅ Réponse du LLM: {...}
```

## 📝 Fichiers du projet

- `config.py` - Configuration (vitesse, nombre de nations, etc.)
- `prompts.py` - Templates de prompts pour le LLM
- `llm_brain.py` - Communication avec Ollama
- `nation.py` - *(À venir)* Classe Nation
- `world.py` - *(À venir)* Carte du monde
- `main.py` - *(À venir)* Boucle principale du jeu

## ⚙️ Configuration

Modifie `config.py` pour:
- Changer le modèle LLM utilisé (`LLM_MODEL`)
- Ajuster la vitesse du jeu (`TURN_DELAY`)
- Modifier le nombre de nations (`INITIAL_NATIONS`)

## 🐛 Problèmes courants

**Erreur: "Ollama ne répond pas"**
→ Lance `ollama serve` dans un terminal

**Erreur: "model not found"**
→ Télécharge le modèle: `ollama pull llama3.2`

**Timeout du LLM**
→ Ton PC est peut-être lent, essaie `llama3.2:1b` (plus rapide)
