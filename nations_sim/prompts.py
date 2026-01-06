# Templates de prompts pour le LLM

SYSTEM_PROMPT = """Tu es l'intelligence artificielle qui contrôle une nation dans un jeu de stratégie.
Tu dois prendre UNE décision par tour.
Réponds UNIQUEMENT en JSON valide, sans texte avant ou après.
Format exact attendu:
{
  "action": "attack/ally/trade/build_army/defend/nothing",
  "target": "nom_exact_de_la_nation ou null",
  "reason": "ta justification en maximum 15 mots"
}"""


def build_decision_prompt(nation, world_state, recent_event):
    """
    Construit le prompt complet pour une décision de nation.

    Args:
        nation: Objet Nation qui doit prendre une décision
        world_state: Dict contenant l'état du monde (autres nations, etc.)
        recent_event: Dernier événement important concernant cette nation

    Returns:
        str: Le prompt complet à envoyer au LLM
    """

    # FIX BUG 3: Liste de TOUTES les nations existantes (pour éviter les noms inventés)
    all_nations_list = []
    if 'all_nations' in world_state:
        for nation_name, nation_info in world_state['all_nations'].items():
            all_nations_list.append(f"- {nation_name}")
    all_nations_text = "\n".join(all_nations_list) if all_nations_list else ""

    # Liste des voisins
    neighbors_list = []
    for neighbor_name, neighbor_info in world_state['neighbors'].items():
        neighbors_list.append(
            f"- {neighbor_name}: Armée {neighbor_info['army']}, "
            f"Or {neighbor_info['gold']}, Territoires {neighbor_info['territories']}"
        )
    neighbors_text = "\n".join(neighbors_list) if neighbors_list else "Aucun voisin proche"

    # Relations
    relations_list = []
    for other_nation, relation_score in nation.relations.items():
        emoji = "🤝" if relation_score > 50 else "⚔️" if relation_score < -30 else "😐"
        relations_list.append(f"{emoji} {other_nation}: {relation_score:+d}")
    relations_text = "\n".join(relations_list) if relations_list else "Aucune relation établie"

    # Événement récent
    event_text = recent_event if recent_event else "Rien de notable"

    # Construction du prompt
    prompt = f"""Tu es {nation.leader_name}, dirigeant de {nation.name}.
Ta personnalité: {nation.personality_description}

=== SITUATION ACTUELLE ===
- Ton armée: {nation.army}/100
- Ton or: {nation.gold}
- Tes territoires: {nation.get_territory_count()}
- Tour actuel: {world_state['turn']}

=== NATIONS EXISTANTES (utilise ces noms EXACTEMENT) ===
{all_nations_text}

=== TES VOISINS PROCHES (tu ne peux attaquer QUE tes voisins) ===
{neighbors_text}

=== TES RELATIONS ===
{relations_text}

=== ÉVÉNEMENT RÉCENT ===
{event_text}

=== ACTIONS POSSIBLES ===
- "attack": Attaquer une nation voisine (coûte {world_state['attack_cost_gold']} or et {world_state['attack_cost_army']} soldats)
- "ally": Proposer une alliance à une nation
- "trade": Commercer avec une nation (tu gagnes de l'or, l'autre aussi)
- "build_army": Recruter des troupes (coûte de l'or)
- "defend": Fortifier tes frontières (+ défense au prochain tour)
- "nothing": Attendre et économiser

Que décides-tu? Réponds UNIQUEMENT en JSON:
{{
  "action": "...",
  "target": "nom_exact_nation ou null",
  "reason": "..."
}}"""

    return prompt


def build_simple_test_prompt():
    """Prompt simple pour tester si Ollama fonctionne"""
    return """Tu es un assistant. Réponds UNIQUEMENT en JSON:
{
  "status": "ok",
  "message": "Je fonctionne correctement"
}"""
