# -*- coding: utf-8 -*-
# Communication avec Ollama (le cerveau LLM des nations)
# VERSION CORRIGÉE avec parsing JSON robuste

import requests
import json
import re  # Pour extraction regex si JSON incomplet
from config import OLLAMA_URL, LLM_MODEL, LLM_TEMPERATURE
from prompts import SYSTEM_PROMPT


class LLMBrain:
    """
    Classe qui gère la communication avec Ollama.
    Chaque nation utilisera cette classe pour "penser" et prendre des décisions.
    """

    def __init__(self):
        self.url = OLLAMA_URL
        self.model = LLM_MODEL
        self.temperature = LLM_TEMPERATURE

    def is_ollama_running(self):
        """
        Vérifie si Ollama est bien lancé et accessible.

        Returns:
            bool: True si Ollama répond, False sinon
        """
        try:
            response = requests.get(f"{self.url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def ask_decision(self, prompt):
        """
        Envoie un prompt à Ollama et récupère la décision en JSON.

        Args:
            prompt (str): Le prompt décrivant la situation de la nation

        Returns:
            dict: La décision au format {"action": "...", "target": "...", "reason": "..."}
                  Ou None si erreur
        """
        try:
            # Construction de la requête pour Ollama
            payload = {
                "model": self.model,
                "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}",
                "stream": False,  # On veut la réponse complète d'un coup
                "options": {
                    "temperature": self.temperature
                }
            }

            # Envoi de la requête (timeout augmenté à 60s pour les PCs lents)
            response = requests.post(
                f"{self.url}/api/generate",
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                print(f"❌ Erreur Ollama: Status {response.status_code}")
                return None

            # Récupération de la réponse
            result = response.json()
            llm_response = result.get("response", "").strip()

            # Tentative de parser le JSON (avec plusieurs méthodes)
            decision = self._parse_json_response(llm_response)

            return decision

        except requests.exceptions.Timeout:
            print("⏱️ Timeout: Ollama met trop de temps à répondre")
            return None
        except Exception as e:
            print(f"❌ Erreur LLM: {e}")
            return None

    def _parse_json_response(self, text):
        """
        Parse la réponse du LLM pour extraire le JSON.
        Gère les cas où le LLM ajoute du texte avant/après le JSON,
        ou quand le JSON est incomplet.

        Args:
            text (str): La réponse brute du LLM

        Returns:
            dict: Le JSON parsé, ou None si impossible
        """
        text = text.strip()

        # MÉTHODE 1: Essai direct
        try:
            return json.loads(text)
        except:
            pass

        # MÉTHODE 2: Cherche le JSON dans le texte
        start = text.find('{')
        if start == -1:
            return None

        json_part = text[start:]

        # FIX BUG 1: Si JSON incomplet (manque le }), on l'ajoute
        if json_part.count('{') > json_part.count('}'):
            json_part = json_part + '}'

        end = json_part.rfind('}') + 1
        json_str = json_part[:end]

        # Nettoie les retours à la ligne qui cassent parfois le JSON
        json_str = json_str.replace('\n', ' ').replace('\r', '')

        try:
            return json.loads(json_str)
        except:
            pass

        # MÉTHODE 3: Extraction manuelle avec regex (dernier recours)
        try:
            action_match = re.search(r'"action"\s*:\s*"([^"]+)"', text)
            target_match = re.search(r'"target"\s*:\s*"([^"]*)"', text)
            reason_match = re.search(r'"reason"\s*:\s*"([^"]+)"', text)

            if action_match:
                return {
                    "action": action_match.group(1),
                    "target": target_match.group(1) if target_match else None,
                    "reason": reason_match.group(1) if reason_match else "Aucune raison"
                }
        except:
            pass

        # Si tout échoue
        print(f"⚠️ Impossible de parser la réponse LLM: {text[:100]}...")
        return None

    def validate_decision(self, decision):
        """
        Vérifie que la décision du LLM est valide.

        Args:
            decision (dict): La décision à valider

        Returns:
            bool: True si valide, False sinon
        """
        if not decision:
            return False

        # Vérification des champs requis
        required_fields = ["action", "target", "reason"]
        if not all(field in decision for field in required_fields):
            print(f"⚠️ Décision invalide: champs manquants. Reçu: {decision}")
            return False

        # Vérification que l'action est valide
        valid_actions = ["attack", "ally", "trade", "build_army", "defend", "nothing"]
        if decision["action"] not in valid_actions:
            print(f"⚠️ Action invalide: {decision['action']}")
            return False

        return True

    def get_default_decision(self):
        """
        Retourne une décision par défaut si le LLM échoue.

        Returns:
            dict: Décision "ne rien faire"
        """
        return {
            "action": "nothing",
            "target": None,
            "reason": "En attente d'instructions"
        }


# ===== FONCTION DE TEST =====
def test_ollama_connection():
    """
    Fonction simple pour tester si Ollama fonctionne.
    Lance cette fonction pour vérifier ton installation.
    """
    print("🧪 Test de connexion à Ollama...")
    brain = LLMBrain()

    # Vérification 1: Ollama est-il lancé?
    if not brain.is_ollama_running():
        print("❌ Ollama ne répond pas!")
        print("   Assure-toi qu'Ollama est installé et lancé.")
        print("   Lance: ollama serve")
        return False

    print("✅ Ollama est actif!")

    # Vérification 2: Le modèle peut-il répondre?
    print(f"🤖 Test du modèle {LLM_MODEL}...")
    test_prompt = """Tu es un test. Réponds en JSON:
{
  "status": "ok",
  "message": "Je fonctionne"
}"""

    decision = brain.ask_decision(test_prompt)

    if decision:
        print(f"✅ Réponse du LLM: {decision}")
        return True
    else:
        print("❌ Le LLM n'a pas pu répondre correctement")
        print(f"   Vérifie que le modèle '{LLM_MODEL}' est bien téléchargé:")
        print(f"   ollama pull {LLM_MODEL}")
        return False


if __name__ == "__main__":
    # Si tu lances ce fichier directement, il teste Ollama
    test_ollama_connection()
