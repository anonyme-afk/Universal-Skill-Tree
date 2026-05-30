""" ust.skills.smarthome """\nfrom __future__ import annotations\nimport os\nimport json\nfrom ust.core.registry import skill\n\n@skill(\n    name="ha_get_states",\n    branch="smarthome",\n    description="Récupère les états de tous les appareils Home Assistant",\n    parameters={},\n)\ndef ha_get_states() -> list:
    # --- P&P Checks ---
    if not os.getenv("HA_URL"):
        return "Erreur Plug & Play : clé API manquante (HA_URL). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("HA_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (HA_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        r = requests.get(f"{os.getenv('HA_URL')}/api/states",
            headers={"Authorization": f"Bearer {os.getenv('HA_TOKEN')}"})
        return r.json()
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="ha_turn_on",\n    branch="smarthome",\n    description="Allume un appareil Home Assistant (lumière, switch...)",\n    parameters={
    "properties": {
        "entity_id": {
            "type": "string"
        }
    },
    "required": [
        "entity_id"
    ]
},\n)\ndef ha_turn_on(entity_id: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("HA_URL"):
        return "Erreur Plug & Play : clé API manquante (HA_URL). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("HA_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (HA_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        domain = entity_id.split(".")[0]
        r = requests.post(f"{os.getenv('HA_URL')}/api/services/{domain}/turn_on",
            headers={"Authorization": f"Bearer {os.getenv('HA_TOKEN')}"},
            json={"entity_id": entity_id})
        return f"Allumé : {entity_id} (status {r.status_code})"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="ha_turn_off",\n    branch="smarthome",\n    description="Éteint un appareil Home Assistant",\n    parameters={
    "properties": {
        "entity_id": {
            "type": "string"
        }
    },
    "required": [
        "entity_id"
    ]
},\n)\ndef ha_turn_off(entity_id: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("HA_URL"):
        return "Erreur Plug & Play : clé API manquante (HA_URL). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("HA_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (HA_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        domain = entity_id.split(".")[0]
        r = requests.post(f"{os.getenv('HA_URL')}/api/services/{domain}/turn_off",
            headers={"Authorization": f"Bearer {os.getenv('HA_TOKEN')}"},
            json={"entity_id": entity_id})
        return f"Éteint : {entity_id} (status {r.status_code})"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="ha_set_light_color",\n    branch="smarthome",\n    description="Change la couleur d'une lumière Home Assistant",\n    parameters={
    "properties": {
        "entity_id": {
            "type": "string"
        },
        "rgb": {
            "type": "array"
        },
        "brightness": {
            "type": "integer"
        }
    },
    "required": [
        "entity_id",
        "rgb"
    ]
},\n)\ndef ha_set_light_color(entity_id: str, rgb: list, brightness: int = 255) -> str:
    # --- P&P Checks ---
    if not os.getenv("HA_URL"):
        return "Erreur Plug & Play : clé API manquante (HA_URL). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("HA_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (HA_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    try:
        return "Skipped because truncated"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


