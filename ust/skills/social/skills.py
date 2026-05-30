""" ust.skills.social """\nfrom __future__ import annotations\nimport os\nimport json\nfrom ust.core.registry import skill\n\n@skill(\n    name="tweet_post",\n    branch="social",\n    description="Poste un tweet via l'API Twitter/X",\n    parameters={
    "properties": {
        "text": {
            "type": "string"
        }
    },
    "required": [
        "text"
    ]
},\n)\ndef tweet_post(text: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("TWITTER_API_KEY"):
        return "Erreur Plug & Play : clé API manquante (TWITTER_API_KEY). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("TWITTER_API_SECRET"):
        return "Erreur Plug & Play : clé API manquante (TWITTER_API_SECRET). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("TWITTER_ACCESS_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (TWITTER_ACCESS_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("TWITTER_ACCESS_SECRET"):
        return "Erreur Plug & Play : clé API manquante (TWITTER_ACCESS_SECRET). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import tweepy
        client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        r = client.create_tweet(text=text)
        return f"Tweet posté, ID: {r.data['id']}"
    except ImportError as e:
        reqs_str = " ".join(['tweepy']) if ['tweepy'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="tweet_search",\n    branch="social",\n    description="Recherche des tweets récents sur un sujet",\n    parameters={
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
},\n)\ndef tweet_search(query: str, max_results: int = 10) -> list:
    # --- P&P Checks ---
    if not os.getenv("TWITTER_BEARER_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (TWITTER_BEARER_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import tweepy
        client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))
        r = client.search_recent_tweets(query=query, max_results=max_results)
        return [t.text for t in (r.data or [])]
    except ImportError as e:
        reqs_str = " ".join(['tweepy']) if ['tweepy'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="reddit_post",\n    branch="social",\n    description="Poste sur Reddit via PRAW",\n    parameters={
    "properties": {
        "subreddit": {
            "type": "string"
        },
        "title": {
            "type": "string"
        },
        "body": {
            "type": "string"
        }
    },
    "required": [
        "subreddit",
        "title",
        "body"
    ]
},\n)\ndef reddit_post(subreddit: str, title: str, body: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("REDDIT_CLIENT_ID"):
        return "Erreur Plug & Play : clé API manquante (REDDIT_CLIENT_ID). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("REDDIT_CLIENT_SECRET"):
        return "Erreur Plug & Play : clé API manquante (REDDIT_CLIENT_SECRET). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("REDDIT_USERNAME"):
        return "Erreur Plug & Play : clé API manquante (REDDIT_USERNAME). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("REDDIT_PASSWORD"):
        return "Erreur Plug & Play : clé API manquante (REDDIT_PASSWORD). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import praw
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            user_agent="UST Bot"
        )
        post = reddit.subreddit(subreddit).submit(title, selftext=body)
        return f"Posté sur r/{subreddit} : {post.url}"
    except ImportError as e:
        reqs_str = " ".join(['praw']) if ['praw'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="reddit_get_hot",\n    branch="social",\n    description="Récupère les posts populaires d'un subreddit",\n    parameters={
    "properties": {
        "subreddit": {
            "type": "string"
        },
        "limit": {
            "type": "integer"
        }
    },
    "required": [
        "subreddit"
    ]
},\n)\ndef reddit_get_hot(subreddit: str, limit: int = 10) -> list:
    # --- P&P Checks ---
    if not os.getenv("REDDIT_CLIENT_ID"):
        return "Erreur Plug & Play : clé API manquante (REDDIT_CLIENT_ID). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("REDDIT_CLIENT_SECRET"):
        return "Erreur Plug & Play : clé API manquante (REDDIT_CLIENT_SECRET). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import praw
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent="UST Bot"
        )
        return [{"title": p.title, "score": p.score, "url": p.url}
                for p in reddit.subreddit(subreddit).hot(limit=limit)]
    except ImportError as e:
        reqs_str = " ".join(['praw']) if ['praw'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="github_create_repo",\n    branch="social",\n    description="Crée un nouveau dépôt GitHub",\n    parameters={
    "properties": {
        "name": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "private": {
            "type": "boolean"
        }
    },
    "required": [
        "name"
    ]
},\n)\ndef github_create_repo(name: str, description: str = "", private: bool = False) -> str:
    # --- P&P Checks ---
    if not os.getenv("GITHUB_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (GITHUB_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        r = requests.post("https://api.github.com/user/repos",
            json={"name": name, "description": description, "private": private},
            headers={"Authorization": f"token {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github.v3+json"})
        return r.json().get("html_url", r.text)
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="github_push_file",\n    branch="social",\n    description="Push un fichier sur un repo GitHub via l'API",\n    parameters={
    "properties": {
        "repo": {
            "type": "string"
        },
        "file_path": {
            "type": "string"
        },
        "content": {
            "type": "string"
        },
        "message": {
            "type": "string"
        }
    },
    "required": [
        "repo",
        "file_path",
        "content"
    ]
},\n)\ndef github_push_file(repo: str, file_path: str, content: str, message: str = "UST commit") -> str:
    # --- P&P Checks ---
    if not os.getenv("GITHUB_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (GITHUB_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests, base64
        url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
        headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github.v3+json"}
        existing = requests.get(url, headers=headers).json()
        sha = existing.get("sha")
        data = {"message": message, "content": base64.b64encode(content.encode()).decode()}
        if sha:
            data["sha"] = sha
        r = requests.put(url, json=data, headers=headers)
        return f"Fichier pushé (status {r.status_code})"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="send_pushover_notification",\n    branch="social",\n    description="Envoie une notification push via Pushover (mobile)",\n    parameters={
    "properties": {
        "title": {
            "type": "string"
        },
        "message": {
            "type": "string"
        }
    },
    "required": [
        "title",
        "message"
    ]
},\n)\ndef send_pushover_notification(title: str, message: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("PUSHOVER_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (PUSHOVER_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("PUSHOVER_USER"):
        return "Erreur Plug & Play : clé API manquante (PUSHOVER_USER). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        r = requests.post("https://api.pushover.net/1/messages.json", data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "title": title,
            "message": message
        })
        return f"Pushover (status {r.status_code})"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="rss_feed_read",\n    branch="social",\n    description="Lit un flux RSS et retourne les derniers articles",\n    parameters={
    "properties": {
        "url": {
            "type": "string"
        },
        "limit": {
            "type": "integer"
        }
    },
    "required": [
        "url"
    ]
},\n)\ndef rss_feed_read(url: str, limit: int = 5) -> list:
    # --- P&P Checks ---
    try:
        import feedparser
        feed = feedparser.parse(url)
        return [{"title": e.title, "link": e.link, "published": e.get("published", "")}
                for e in feed.entries[:limit]]
    except ImportError as e:
        reqs_str = " ".join(['feedparser']) if ['feedparser'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


