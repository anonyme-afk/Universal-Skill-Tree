""" ust.skills.productivity """\nfrom __future__ import annotations\nimport os\nimport json\nfrom ust.core.registry import skill\n\n@skill(\n    name="send_email_smtp",\n    branch="productivity",\n    description="Envoie un email via SMTP (Gmail, Outlook...)",\n    parameters={
    "properties": {
        "to": {
            "type": "string"
        },
        "subject": {
            "type": "string"
        },
        "body": {
            "type": "string"
        }
    },
    "required": [
        "to",
        "subject",
        "body"
    ]
},\n)\ndef send_email_smtp(to: str, subject: str, body: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("EMAIL_ADDRESS"):
        return "Erreur Plug & Play : clé API manquante (EMAIL_ADDRESS). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("EMAIL_PASSWORD"):
        return "Erreur Plug & Play : clé API manquante (EMAIL_PASSWORD). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("SMTP_HOST"):
        return "Erreur Plug & Play : clé API manquante (SMTP_HOST). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("SMTP_PORT"):
        return "Erreur Plug & Play : clé API manquante (SMTP_PORT). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import smtplib
        from email.mime.text import MIMEText
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = os.getenv("EMAIL_ADDRESS")
        msg["To"] = to
        with smtplib.SMTP(os.getenv("SMTP_HOST","smtp.gmail.com"), int(os.getenv("SMTP_PORT","587"))) as s:
            s.starttls()
            s.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            s.send_message(msg)
        return f"Email envoyé à {to}"
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="send_discord_message",\n    branch="productivity",\n    description="Envoie un message dans un canal Discord via webhook",\n    parameters={
    "properties": {
        "message": {
            "type": "string"
        },
        "username": {
            "type": "string"
        }
    },
    "required": [
        "message"
    ]
},\n)\ndef send_discord_message(message: str, username: str = "UST Bot") -> str:
    # --- P&P Checks ---
    if not os.getenv("DISCORD_WEBHOOK_URL"):
        return "Erreur Plug & Play : clé API manquante (DISCORD_WEBHOOK_URL). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        r = requests.post(os.getenv("DISCORD_WEBHOOK_URL"), json={"content": message, "username": username})
        return f"Status: {r.status_code}"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="send_telegram_message",\n    branch="productivity",\n    description="Envoie un message Telegram",\n    parameters={
    "properties": {
        "message": {
            "type": "string"
        }
    },
    "required": [
        "message"
    ]
},\n)\ndef send_telegram_message(message: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (TELEGRAM_BOT_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("TELEGRAM_CHAT_ID"):
        return "Erreur Plug & Play : clé API manquante (TELEGRAM_CHAT_ID). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": message})
        return "Message envoyé" if r.status_code == 200 else f"Erreur: {r.text}"
    except ImportError as e:
        reqs_str = " ".join(['python-telegram-bot']) if ['python-telegram-bot'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="send_slack_message",\n    branch="productivity",\n    description="Envoie un message dans Slack via webhook",\n    parameters={
    "properties": {
        "message": {
            "type": "string"
        }
    },
    "required": [
        "message"
    ]
},\n)\ndef send_slack_message(message: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("SLACK_WEBHOOK_URL"):
        return "Erreur Plug & Play : clé API manquante (SLACK_WEBHOOK_URL). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        r = requests.post(os.getenv("SLACK_WEBHOOK_URL"), json={"text": message})
        return f"Status: {r.status_code}"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="create_google_calendar_event",\n    branch="productivity",\n    description="Crée un événement Google Calendar",\n    parameters={
    "properties": {
        "title": {
            "type": "string"
        },
        "start": {
            "type": "string"
        },
        "end": {
            "type": "string"
        },
        "description": {
            "type": "string"
        }
    },
    "required": [
        "title",
        "start",
        "end"
    ]
},\n)\ndef create_google_calendar_event(title: str, start: str, end: str, description: str = "") -> str:
    # --- P&P Checks ---
    if not os.getenv("GOOGLE_CREDENTIALS_PATH"):
        return "Erreur Plug & Play : clé API manquante (GOOGLE_CREDENTIALS_PATH). Ajoutez-la dans .env.ust puis réessayez."
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file(os.getenv("GOOGLE_CREDENTIALS_PATH"))
        service = build("calendar", "v3", credentials=creds)
        event = {"summary": title, "description": description,
                 "start": {"dateTime": start, "timeZone": "Europe/Paris"},
                 "end": {"dateTime": end, "timeZone": "Europe/Paris"}}
        service.events().insert(calendarId="primary", body=event).execute()
        return f"Événement créé : {title}"
    except ImportError as e:
        reqs_str = " ".join(['google-api-python-client', 'google-auth-oauthlib']) if ['google-api-python-client', 'google-auth-oauthlib'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="create_notion_page",\n    branch="productivity",\n    description="Crée une page dans Notion",\n    parameters={
    "properties": {
        "title": {
            "type": "string"
        },
        "content": {
            "type": "string"
        }
    },
    "required": [
        "title",
        "content"
    ]
},\n)\ndef create_notion_page(title: str, content: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("NOTION_API_KEY"):
        return "Erreur Plug & Play : clé API manquante (NOTION_API_KEY). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("NOTION_DATABASE_ID"):
        return "Erreur Plug & Play : clé API manquante (NOTION_DATABASE_ID). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        headers = {"Authorization": f"Bearer {os.getenv('NOTION_API_KEY')}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}
        data = {"parent": {"database_id": os.getenv("NOTION_DATABASE_ID")},
                "properties": {"title": {"title": [{"text": {"content": title}}]}},
                "children": [{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}}]}
        r = requests.post("https://api.notion.com/v1/pages", json=data, headers=headers)
        return f"Page créée (status {r.status_code})"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="add_trello_card",\n    branch="productivity",\n    description="Ajoute une carte dans un tableau Trello",\n    parameters={
    "properties": {
        "list_id": {
            "type": "string"
        },
        "name": {
            "type": "string"
        },
        "description": {
            "type": "string"
        }
    },
    "required": [
        "list_id",
        "name"
    ]
},\n)\ndef add_trello_card(list_id: str, name: str, description: str = "") -> str:
    # --- P&P Checks ---
    if not os.getenv("TRELLO_API_KEY"):
        return "Erreur Plug & Play : clé API manquante (TRELLO_API_KEY). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("TRELLO_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (TRELLO_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        r = requests.post("https://api.trello.com/1/cards", params={
            "idList": list_id, "name": name, "desc": description,
            "key": os.getenv("TRELLO_API_KEY"), "token": os.getenv("TRELLO_TOKEN")
        })
        return f"Carte créée (status {r.status_code})"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="create_github_issue",\n    branch="productivity",\n    description="Crée une issue GitHub",\n    parameters={
    "properties": {
        "repo": {
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
        "repo",
        "title"
    ]
},\n)\ndef create_github_issue(repo: str, title: str, body: str = "") -> str:
    # --- P&P Checks ---
    if not os.getenv("GITHUB_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (GITHUB_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        r = requests.post(f"https://api.github.com/repos/{repo}/issues",
            json={"title": title, "body": body},
            headers={"Authorization": f"token {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github.v3+json"})
        return f"Issue créée : {r.json().get('html_url', r.text)}"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_github_repo_info",\n    branch="productivity",\n    description="Retourne les informations d'un repo GitHub",\n    parameters={
    "properties": {
        "repo": {
            "type": "string"
        }
    },
    "required": [
        "repo"
    ]
},\n)\ndef get_github_repo_info(repo: str) -> dict:
    # --- P&P Checks ---
    try:
        import requests
        r = requests.get(f"https://api.github.com/repos/{repo}").json()
        return {"name": r.get("name"), "stars": r.get("stargazers_count"), "forks": r.get("forks_count"), "description": r.get("description"), "language": r.get("language")}
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="summarize_text",\n    branch="productivity",\n    description="Résume un texte long (utilise OpenAI)",\n    parameters={
    "properties": {
        "text": {
            "type": "string"
        },
        "max_words": {
            "type": "integer"
        }
    },
    "required": [
        "text"
    ]
},\n)\ndef summarize_text(text: str, max_words: int = 100) -> str:
    # --- P&P Checks ---
    if not os.getenv("OPENAI_API_KEY"):
        return "Erreur Plug & Play : clé API manquante (OPENAI_API_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        r = client.chat.completions.create(model="gpt-4o-mini", messages=[
            {"role":"user","content":f"Résume ce texte en {max_words} mots max :\n\n{text}"}
        ])
        return r.choices[0].message.content
    except ImportError as e:
        reqs_str = " ".join(['openai']) if ['openai'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="set_timer",\n    branch="productivity",\n    description="Lance un timer et envoie une notification quand il expire",\n    parameters={
    "properties": {
        "seconds": {
            "type": "integer"
        },
        "label": {
            "type": "string"
        }
    },
    "required": [
        "seconds"
    ]
},\n)\ndef set_timer(seconds: int, label: str = "Timer") -> str:
    # --- P&P Checks ---
    try:
        import threading
        from plyer import notification
        def _notify():
            import time
            time.sleep(seconds)
            notification.notify(title="⏰ Timer", message=f"{label} — {seconds}s écoulées", timeout=10)
        t = threading.Thread(target=_notify, daemon=True)
        t.start()
        return f"Timer de {seconds}s lancé : {label}"
    except ImportError as e:
        reqs_str = " ".join(['plyer']) if ['plyer'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_current_time",\n    branch="productivity",\n    description="Retourne l'heure et la date actuelle",\n    parameters={
    "properties": {
        "timezone": {
            "type": "string"
        }
    }
},\n)\ndef get_current_time(timezone: str = "Europe/Paris") -> str:
    # --- P&P Checks ---
    try:
        try:
            import datetime
            from zoneinfo import ZoneInfo
            now = datetime.datetime.now(ZoneInfo(timezone))
            return now.strftime("%A %d %B %Y, %H:%M:%S")
        except:
            import datetime
            return str(datetime.datetime.now())
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


