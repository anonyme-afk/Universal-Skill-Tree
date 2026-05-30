""" ust.skills.web """\nfrom __future__ import annotations\nimport os\nimport json\nfrom ust.core.registry import skill\n\n@skill(\n    name="web_search_ddg",\n    branch="web",\n    description="Recherche sur DuckDuckGo (gratuit, sans API key)",\n    parameters={
    "properties": {
        "query": {
            "type": "string"
        },
        "max_results": {
            "type": "integer"
        }
    },
    "required": [
        "query"
    ]
},\n)\ndef web_search_ddg(query: str, max_results: int = 5) -> list:
    # --- P&P Checks ---
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=max_results))
    except ImportError as e:
        reqs_str = " ".join(['duckduckgo-search']) if ['duckduckgo-search'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="web_search_google",\n    branch="web",\n    description="Recherche Google via SerpAPI",\n    parameters={
    "properties": {
        "query": {
            "type": "string"
        }
    },
    "required": [
        "query"
    ]
},\n)\ndef web_search_google(query: str) -> list:
    # --- P&P Checks ---
    if not os.getenv("SERPAPI_KEY"):
        return "Erreur Plug & Play : clé API manquante (SERPAPI_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        from serpapi import GoogleSearch
        s = GoogleSearch({"q": query, "api_key": os.getenv("SERPAPI_KEY")})
        return s.get_dict().get("organic_results", [])
    except ImportError as e:
        reqs_str = " ".join(['google-search-results']) if ['google-search-results'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="scrape_webpage",\n    branch="web",\n    description="Extrait le texte d'une page web",\n    parameters={
    "properties": {
        "url": {
            "type": "string"
        }
    },
    "required": [
        "url"
    ]
},\n)\ndef scrape_webpage(url: str) -> str:
    # --- P&P Checks ---
    try:
        import requests
        from bs4 import BeautifulSoup
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)[:5000]
    except ImportError as e:
        reqs_str = " ".join(['requests', 'beautifulsoup4']) if ['requests', 'beautifulsoup4'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="download_file",\n    branch="web",\n    description="Télécharge un fichier depuis une URL",\n    parameters={
    "properties": {
        "url": {
            "type": "string"
        },
        "save_path": {
            "type": "string"
        }
    },
    "required": [
        "url",
        "save_path"
    ]
},\n)\ndef download_file(url: str, save_path: str) -> str:
    # --- P&P Checks ---
    try:
        import requests
        r = requests.get(url, stream=True)
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return f"Fichier téléchargé : {save_path}"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="check_website_status",\n    branch="web",\n    description="Vérifie si un site web est accessible",\n    parameters={
    "properties": {
        "url": {
            "type": "string"
        }
    },
    "required": [
        "url"
    ]
},\n)\ndef check_website_status(url: str) -> dict:
    # --- P&P Checks ---
    try:
        import requests, time
        start = time.time()
        try:
            r = requests.get(url, timeout=5)
            return {"status": r.status_code, "online": True, "response_ms": round((time.time()-start)*1000)}
        except:
            return {"status": None, "online": False, "response_ms": None}
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_public_ip",\n    branch="web",\n    description="Retourne l'IP publique de la machine",\n    parameters={},\n)\ndef get_public_ip() -> str:
    # --- P&P Checks ---
    try:
        import requests
        return requests.get("https://api.ipify.org").text
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_geolocation",\n    branch="web",\n    description="Géolocalise une adresse IP",\n    parameters={
    "properties": {
        "ip": {
            "type": "string"
        }
    }
},\n)\ndef get_geolocation(ip: str = "auto") -> dict:
    # --- P&P Checks ---
    try:
        import requests
        url = f"https://ipapi.co/{ip}/json/" if ip != "auto" else "https://ipapi.co/json/"
        return requests.get(url).json()
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="send_webhook",\n    branch="web",\n    description="Envoie une requête POST à un webhook",\n    parameters={
    "properties": {
        "url": {
            "type": "string"
        },
        "data": {
            "type": "object"
        }
    },
    "required": [
        "url",
        "data"
    ]
},\n)\ndef send_webhook(url: str, data: dict) -> str:
    # --- P&P Checks ---
    try:
        import requests
        r = requests.post(url, json=data)
        return f"Status: {r.status_code}"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_weather",\n    branch="web",\n    description="Météo d'une ville via Open-Meteo (gratuit, sans API key)",\n    parameters={
    "properties": {
        "city": {
            "type": "string"
        }
    },
    "required": [
        "city"
    ]
},\n)\ndef get_weather(city: str) -> dict:
    # --- P&P Checks ---
    try:
        import requests
        # Géocode d'abord
        geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1").json()
        if not geo.get("results"):
            return {"error": f"Ville non trouvée : {city}"}
        r = geo["results"][0]
        lat, lon = r["latitude"], r["longitude"]
        w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()
        cw = w["current_weather"]
        return {"city": city, "temp_c": cw["temperature"], "wind_kmh": cw["windspeed"], "code": cw["weathercode"]}
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_crypto_price",\n    branch="web",\n    description="Retourne le prix d'une crypto en temps réel",\n    parameters={
    "properties": {
        "symbol": {
            "type": "string"
        }
    }
},\n)\ndef get_crypto_price(symbol: str = "bitcoin") -> dict:
    # --- P&P Checks ---
    try:
        import requests
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd,eur").json()
        return r.get(symbol, {"error": "Crypto non trouvée"})
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_stock_price",\n    branch="web",\n    description="Prix d'une action en temps réel via Yahoo Finance",\n    parameters={
    "properties": {
        "ticker": {
            "type": "string"
        }
    },
    "required": [
        "ticker"
    ]
},\n)\ndef get_stock_price(ticker: str) -> dict:
    # --- P&P Checks ---
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        info = t.fast_info
        return {"ticker": ticker, "price": info.last_price, "currency": info.currency}
    except ImportError as e:
        reqs_str = " ".join(['yfinance']) if ['yfinance'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="translate_text",\n    branch="web",\n    description="Traduit un texte via Google Translate (gratuit)",\n    parameters={
    "properties": {
        "text": {
            "type": "string"
        },
        "target_lang": {
            "type": "string"
        }
    },
    "required": [
        "text"
    ]
},\n)\ndef translate_text(text: str, target_lang: str = "fr") -> str:
    # --- P&P Checks ---
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except ImportError as e:
        reqs_str = " ".join(['deep-translator']) if ['deep-translator'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="shorten_url",\n    branch="web",\n    description="Raccourcit une URL via TinyURL",\n    parameters={
    "properties": {
        "url": {
            "type": "string"
        }
    },
    "required": [
        "url"
    ]
},\n)\ndef shorten_url(url: str) -> str:
    # --- P&P Checks ---
    try:
        import requests
        r = requests.get(f"https://tinyurl.com/api-create.php?url={url}")
        return r.text
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_exchange_rate",\n    branch="web",\n    description="Taux de change entre deux devises",\n    parameters={
    "properties": {
        "from_currency": {
            "type": "string"
        },
        "to_currency": {
            "type": "string"
        }
    }
},\n)\ndef get_exchange_rate(from_currency: str = "USD", to_currency: str = "EUR") -> dict:
    # --- P&P Checks ---
    try:
        import requests
        r = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}").json()
        rate = r["rates"].get(to_currency)
        return {"from": from_currency, "to": to_currency, "rate": rate}
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


