# Communication avec Ollama (le cerveau LLM des nations)

import requests
import json
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
        except requests.exceptions.RequestException:
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

            # Envoi de la requête
            response = requests.post(
                f"{self.url}/api/generate",
                json=payload,
                timeout=30  # 30 secondes max par décision
            )

            if response.status_code != 200:
                print(f"❌ Erreur Ollama: Status {response.status_code}")
                return None

            # Récupération de la réponse
            result = response.json()
            llm_response = result.get("response", "").strip()

            # Tentative de parser le JSON
            # Le LLM devrait renvoyer quelque chose comme:
            # {"action": "attack", "target": "Empire Rouge", "reason": "Ils sont faibles"}
            decision = self._parse_json_response(llm_response)

            return decision

        except requests.exceptions.Timeout:
            print("⏱️ Timeout: Ollama met trop de temps à répondre")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion à Ollama: {e}")
            return None
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            return None

    def _parse_json_response(self, text):
        """
        Parse la réponse du LLM pour extraire le JSON.
        Gère les cas où le LLM ajoute du texte avant/après le JSON.

        Args:
            text (str): La réponse brute du LLM

        Returns:
            dict: Le JSON parsé, ou None si impossible
        """
        try:
            # Cas 1: Le texte est directement du JSON valide
            return json.loads(text)
        except json.JSONDecodeError:
            # Cas 2: Le JSON est enrobé de texte, on essaie de l'extraire
            try:
                # Cherche le premier { et le dernier }
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end > start:
                    json_str = text[start:end]
                    return json.loads(json_str)
            except json.JSONDecodeError:
                pass

            # Cas 3: Impossible de parser
            print(f"⚠️ Réponse LLM non-JSON: {text[:100]}...")
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
