""" ust.skills.api """\nfrom __future__ import annotations\nimport os\nimport json\nfrom ust.core.registry import skill\n\n@skill(\n    name="call_rest_api",\n    branch="api",\n    description="Appelle une API REST générique (GET/POST/PUT/DELETE)",\n    parameters={
    "properties": {
        "url": {
            "type": "string"
        },
        "method": {
            "type": "string"
        },
        "headers": {
            "type": "object"
        },
        "body": {
            "type": "object"
        }
    },
    "required": [
        "url"
    ]
},\n)\ndef call_rest_api(url: str, method: str = "GET", headers: dict = {}, body: dict = {}) -> dict:
    # --- P&P Checks ---
    try:
        import requests
        r = requests.request(method, url, headers=headers, json=body or None, timeout=10)
        try:
            return r.json()
        except:
            return {"status": r.status_code, "text": r.text}
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_news_headlines",\n    branch="api",\n    description="Récupère les dernières actualités via NewsAPI",\n    parameters={
    "properties": {
        "query": {
            "type": "string"
        },
        "language": {
            "type": "string"
        },
        "count": {
            "type": "integer"
        }
    }
},\n)\ndef get_news_headlines(query: str = "technology", language: str = "fr", count: int = 5) -> list:
    # --- P&P Checks ---
    if not os.getenv("NEWSAPI_KEY"):
        return "Erreur Plug & Play : clé API manquante (NEWSAPI_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        url = f"https://newsapi.org/v2/everything?q={query}&language={language}&pageSize={count}&apiKey={os.getenv('NEWSAPI_KEY')}"
        r = requests.get(url).json()
        return [{"title": a["title"], "url": a["url"], "source": a["source"]["name"]}
                for a in r.get("articles", [])]
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_wikipedia_summary",\n    branch="api",\n    description="Retourne le résumé Wikipedia d'un sujet",\n    parameters={
    "properties": {
        "topic": {
            "type": "string"
        },
        "lang": {
            "type": "string"
        }
    },
    "required": [
        "topic"
    ]
},\n)\ndef get_wikipedia_summary(topic: str, lang: str = "fr") -> str:
    # --- P&P Checks ---
    try:
        import wikipedia
        wikipedia.set_lang(lang)
        try:
            return wikipedia.summary(topic, sentences=5)
        except Exception as e:
            return f"Erreur : {e}"
    except ImportError as e:
        reqs_str = " ".join(['wikipedia']) if ['wikipedia'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_definition",\n    branch="api",\n    description="Retourne la définition d'un mot (anglais) via Free Dictionary API",\n    parameters={
    "properties": {
        "word": {
            "type": "string"
        }
    },
    "required": [
        "word"
    ]
},\n)\ndef get_definition(word: str) -> str:
    # --- P&P Checks ---
    try:
        import requests
        r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}").json()
        if isinstance(r, list):
            meanings = r[0].get("meanings", [])
            if meanings:
                defs = meanings[0].get("definitions", [])
                if defs:
                    return defs[0].get("definition", "Aucune définition trouvée")
        return "Aucune définition trouvée"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_movie_info",\n    branch="api",\n    description="Retourne les infos d'un film via OMDB API",\n    parameters={
    "properties": {
        "title": {
            "type": "string"
        }
    },
    "required": [
        "title"
    ]
},\n)\ndef get_movie_info(title: str) -> dict:
    # --- P&P Checks ---
    if not os.getenv("OMDB_API_KEY"):
        return "Erreur Plug & Play : clé API manquante (OMDB_API_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        r = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={os.getenv('OMDB_API_KEY')}").json()
        return {"title": r.get("Title"), "year": r.get("Year"), "plot": r.get("Plot"), "rating": r.get("imdbRating"), "genre": r.get("Genre")}
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_holidays",\n    branch="api",\n    description="Retourne les jours fériés d'un pays pour une année donnée",\n    parameters={
    "properties": {
        "country": {
            "type": "string"
        },
        "year": {
            "type": "integer"
        }
    }
},\n)\ndef get_holidays(country: str = "FR", year: int = 2025) -> list:
    # --- P&P Checks ---
    try:
        import requests
        r = requests.get(f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country}").json()
        return [{"date": h["date"], "name": h["name"]} for h in r]
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_iss_location",\n    branch="api",\n    description="Retourne la position actuelle de la Station Spatiale Internationale",\n    parameters={},\n)\ndef get_iss_location() -> dict:
    # --- P&P Checks ---
    try:
        import requests
        r = requests.get("http://api.open-notify.org/iss-now.json").json()
        pos = r["iss_position"]
        return {"latitude": pos["latitude"], "longitude": pos["longitude"], "timestamp": r["timestamp"]}
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="generate_barcode",\n    branch="api",\n    description="Génère un code-barres EAN13 ou Code128",\n    parameters={
    "properties": {
        "data": {
            "type": "string"
        },
        "barcode_type": {
            "type": "string"
        },
        "output": {
            "type": "string"
        }
    },
    "required": [
        "data"
    ]
},\n)\ndef generate_barcode(data: str, barcode_type: str = "code128", output: str = "barcode") -> str:
    # --- P&P Checks ---
    try:
        import barcode
        from barcode.writer import ImageWriter
        bc = barcode.get(barcode_type, data, writer=ImageWriter())
        path = bc.save(output)
        return f"Code-barres généré : {path}"
    except ImportError as e:
        reqs_str = " ".join(['python-barcode', 'pillow']) if ['python-barcode', 'pillow'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="ip_reputation_check",\n    branch="api",\n    description="Vérifie la réputation d'une adresse IP via AbuseIPDB",\n    parameters={
    "properties": {
        "ip": {
            "type": "string"
        }
    },
    "required": [
        "ip"
    ]
},\n)\ndef ip_reputation_check(ip: str) -> dict:
    # --- P&P Checks ---
    if not os.getenv("ABUSEIPDB_KEY"):
        return "Erreur Plug & Play : clé API manquante (ABUSEIPDB_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        r = requests.get("https://api.abuseipdb.com/api/v2/check",
            headers={"Key": os.getenv("ABUSEIPDB_KEY"), "Accept": "application/json"},
            params={"ipAddress": ip, "maxAgeInDays": 90})
        data = r.json().get("data", {})
        return {"ip": ip, "abuse_score": data.get("abuseConfidenceScore"), "country": data.get("countryCode"), "reports": data.get("totalReports")}
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="wolfram_alpha_query",\n    branch="api",\n    description="Envoie une question à Wolfram Alpha (calculs, sciences, etc.)",\n    parameters={
    "properties": {
        "query": {
            "type": "string"
        }
    },
    "required": [
        "query"
    ]
},\n)\ndef wolfram_alpha_query(query: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("WOLFRAM_APP_ID"):
        return "Erreur Plug & Play : clé API manquante (WOLFRAM_APP_ID). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import wolframalpha
        client = wolframalpha.Client(os.getenv("WOLFRAM_APP_ID"))
        res = client.query(query)
        pods = list(res.results)
        return str(next(iter(pods)).text) if pods else "Aucun résultat"
    except ImportError as e:
        reqs_str = " ".join(['wolframalpha']) if ['wolframalpha'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


