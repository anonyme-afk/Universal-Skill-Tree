import re

with open("skills_catalog.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix truncation
if "def ha_set_light_color(en" in content:
    content = content[:content.find("def ha_set_light_color(en")]
    content += '..."\n    }\n]\n\n'

# Add missing variables that the user grouped in ALL_SKILLS
content += """
SECURITY_SKILLS = []
DATA_SKILLS = []
MISC_SKILLS = []
"""

# Append the new skills provided in the prompt
content += '''
# ══════════════════════════════════════════════════════════════════
# 🤖  CATÉGORIE 11 : AUTOMATISATION & NAVIGATION WEB (Selenium/Playwright)
# ══════════════════════════════════════════════════════════════════

AUTOMATION_SKILLS = [
    {
        "name": "browser_open_url",
        "category": "automation",
        "description": "Ouvre une URL avec Playwright (navigateur headless)",
        "requires": ["playwright"],
        "env_vars": [],
        "parameters": {"url": "str", "headless": "bool = True"},
        "code": """
def browser_open_url(url: str, headless: bool = True) -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url)
        title = page.title()
        browser.close()
    return f"Page ouverte : {title}"
"""
    },
    {
        "name": "browser_screenshot_url",
        "category": "automation",
        "description": "Prend un screenshot d'une page web avec Playwright",
        "requires": ["playwright"],
        "env_vars": [],
        "parameters": {"url": "str", "output": "str = 'page.png'"},
        "code": """
def browser_screenshot_url(url: str, output: str = "page.png") -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=output, full_page=True)
        browser.close()
    return f"Screenshot : {output}"
"""
    },
    {
        "name": "browser_fill_form",
        "category": "automation",
        "description": "Remplit et soumet un formulaire web avec Playwright",
        "requires": ["playwright"],
        "env_vars": [],
        "parameters": {"url": "str", "fields": "dict", "submit_selector": "str = 'button[type=submit]'"},
        "code": """
def browser_fill_form(url: str, fields: dict, submit_selector: str = "button[type=submit]") -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        for selector, value in fields.items():
            page.fill(selector, value)
        page.click(submit_selector)
        page.wait_for_load_state("networkidle")
        result = page.title()
        browser.close()
    return f"Formulaire soumis, nouvelle page : {result}"
"""
    },
    {
        "name": "browser_get_page_text",
        "category": "automation",
        "description": "Extrait tout le texte visible d'une page via Playwright (JS rendu)",
        "requires": ["playwright"],
        "env_vars": [],
        "parameters": {"url": "str"},
        "code": """
def browser_get_page_text(url: str) -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        text = page.inner_text("body")
        browser.close()
    return text[:5000]
"""
    },
    {
        "name": "browser_click_element",
        "category": "automation",
        "description": "Clique sur un élément d'une page web via sélecteur CSS",
        "requires": ["playwright"],
        "env_vars": [],
        "parameters": {"url": "str", "selector": "str"},
        "code": """
def browser_click_element(url: str, selector: str) -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.click(selector)
        page.wait_for_load_state("networkidle")
        result = page.title()
        browser.close()
    return f"Cliqué, nouvelle page : {result}"
"""
    },
    {
        "name": "schedule_task",
        "category": "automation",
        "description": "Planifie l'exécution répétée d'une fonction Python",
        "requires": ["schedule"],
        "env_vars": [],
        "parameters": {"interval_seconds": "int", "function_code": "str"},
        "code": """
def schedule_task(interval_seconds: int, function_code: str) -> str:
    import schedule, time, threading
    def job():
        exec(function_code)
    schedule.every(interval_seconds).seconds.do(job)
    def run():
        while True:
            schedule.run_pending()
            time.sleep(1)
    t = threading.Thread(target=run, daemon=True)
    t.start()
    return f"Tâche planifiée toutes les {interval_seconds}s"
"""
    },
    {
        "name": "watch_file_changes",
        "category": "automation",
        "description": "Surveille un dossier et déclenche une action à chaque modification",
        "requires": ["watchdog"],
        "env_vars": [],
        "parameters": {"folder": "str", "on_change_code": "str = 'print(event)'"},
        "code": """
def watch_file_changes(folder: str, on_change_code: str = "print(event)") -> str:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import threading
    class Handler(FileSystemEventHandler):
        def on_any_event(self, event):
            exec(on_change_code)
    observer = Observer()
    observer.schedule(Handler(), folder, recursive=True)
    t = threading.Thread(target=observer.start, daemon=True)
    t.start()
    return f"Surveillance de {folder} démarrée"
"""
    },
    {
        "name": "auto_click_gui",
        "category": "automation",
        "description": "Automatise des clics GUI via coordonnées (PyAutoGUI)",
        "requires": ["pyautogui"],
        "env_vars": [],
        "parameters": {"x": "int", "y": "int", "clicks": "int = 1", "interval": "float = 0.25"},
        "code": """
def auto_click_gui(x: int, y: int, clicks: int = 1, interval: float = 0.25) -> str:
    import pyautogui
    pyautogui.click(x, y, clicks=clicks, interval=interval)
    return f"Cliqué {clicks}x en ({x},{y})"
"""
    },
    {
        "name": "hotkey_press",
        "category": "automation",
        "description": "Presse une combinaison de touches clavier",
        "requires": ["pyautogui"],
        "env_vars": [],
        "parameters": {"keys": "list"},
        "code": """
def hotkey_press(keys: list) -> str:
    import pyautogui
    pyautogui.hotkey(*keys)
    return f"Touches pressées : {'+'.join(keys)}"
"""
    },
    {
        "name": "fill_pdf_form",
        "category": "automation",
        "description": "Remplit les champs d'un formulaire PDF",
        "requires": ["pymupdf"],
        "env_vars": [],
        "parameters": {"pdf_path": "str", "fields": "dict", "output": "str"},
        "code": """
def fill_pdf_form(pdf_path: str, fields: dict, output: str) -> str:
    import fitz
    doc = fitz.open(pdf_path)
    for page in doc:
        for widget in page.widgets():
            if widget.field_name in fields:
                widget.field_value = fields[widget.field_name]
                widget.update()
    doc.save(output)
    return f"PDF rempli : {output}"
"""
    },
]

# ══════════════════════════════════════════════════════════════════
# ☁️  CATÉGORIE 12 : CLOUD & STOCKAGE
# ══════════════════════════════════════════════════════════════════

CLOUD_SKILLS = [
    {
        "name": "upload_to_s3",
        "category": "cloud",
        "description": "Upload un fichier vers Amazon S3",
        "requires": ["boto3"],
        "env_vars": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"],
        "parameters": {"file_path": "str", "bucket": "str", "key": "str"},
        "code": """
def upload_to_s3(file_path: str, bucket: str, key: str) -> str:
    import boto3
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket, key)
    return f"Uploadé : s3://{bucket}/{key}"
"""
    },
    {
        "name": "download_from_s3",
        "category": "cloud",
        "description": "Télécharge un fichier depuis Amazon S3",
        "requires": ["boto3"],
        "env_vars": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"],
        "parameters": {"bucket": "str", "key": "str", "output": "str"},
        "code": """
def download_from_s3(bucket: str, key: str, output: str) -> str:
    import boto3
    s3 = boto3.client("s3")
    s3.download_file(bucket, key, output)
    return f"Téléchargé : {output}"
"""
    },
    {
        "name": "list_s3_files",
        "category": "cloud",
        "description": "Liste les fichiers d'un bucket S3",
        "requires": ["boto3"],
        "env_vars": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"],
        "parameters": {"bucket": "str", "prefix": "str = ''"},
        "code": """
def list_s3_files(bucket: str, prefix: str = "") -> list:
    import boto3
    s3 = boto3.client("s3")
    r = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [obj["Key"] for obj in r.get("Contents", [])]
"""
    },
    {
        "name": "upload_to_gdrive",
        "category": "cloud",
        "description": "Upload un fichier vers Google Drive",
        "requires": ["google-api-python-client", "google-auth-oauthlib"],
        "env_vars": ["GOOGLE_CREDENTIALS_PATH"],
        "parameters": {"file_path": "str", "folder_id": "str = None"},
        "code": """
def upload_to_gdrive(file_path: str, folder_id: str = None) -> str:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials
    import os
    creds = Credentials.from_authorized_user_file(os.getenv("GOOGLE_CREDENTIALS_PATH"))
    service = build("drive", "v3", credentials=creds)
    meta = {"name": os.path.basename(file_path)}
    if folder_id:
        meta["parents"] = [folder_id]
    media = MediaFileUpload(file_path, resumable=True)
    f = service.files().create(body=meta, media_body=media, fields="id").execute()
    return f"Fichier uploadé sur Drive, ID: {f.get('id')}"
"""
    },
    {
        "name": "upload_to_dropbox",
        "category": "cloud",
        "description": "Upload un fichier vers Dropbox",
        "requires": ["dropbox"],
        "env_vars": ["DROPBOX_TOKEN"],
        "parameters": {"file_path": "str", "dest_path": "str"},
        "code": """
def upload_to_dropbox(file_path: str, dest_path: str) -> str:
    import dropbox
    dbx = dropbox.Dropbox(os.getenv("DROPBOX_TOKEN"))
    with open(file_path, "rb") as f:
        dbx.files_upload(f.read(), dest_path, mute=True)
    return f"Uploadé sur Dropbox : {dest_path}"
"""
    },
    {
        "name": "create_cloudflare_kv",
        "category": "cloud",
        "description": "Stocke une valeur dans Cloudflare KV",
        "requires": ["requests"],
        "env_vars": ["CF_ACCOUNT_ID", "CF_API_TOKEN", "CF_KV_NAMESPACE_ID"],
        "parameters": {"key": "str", "value": "str"},
        "code": """
def create_cloudflare_kv(key: str, value: str) -> str:
    import requests
    url = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CF_ACCOUNT_ID')}/storage/kv/namespaces/{os.getenv('CF_KV_NAMESPACE_ID')}/values/{key}"
    r = requests.put(url, data=value, headers={"Authorization": f"Bearer {os.getenv('CF_API_TOKEN')}"})
    return f"KV créé (status {r.status_code})"
"""
    },
    {
        "name": "firebase_write",
        "category": "cloud",
        "description": "Écrit des données dans Firebase Realtime Database",
        "requires": ["requests"],
        "env_vars": ["FIREBASE_URL", "FIREBASE_SECRET"],
        "parameters": {"path": "str", "data": "dict"},
        "code": """
def firebase_write(path: str, data: dict) -> str:
    import requests
    url = f"{os.getenv('FIREBASE_URL')}/{path}.json?auth={os.getenv('FIREBASE_SECRET')}"
    r = requests.put(url, json=data)
    return f"Firebase écrit (status {r.status_code})"
"""
    },
    {
        "name": "firebase_read",
        "category": "cloud",
        "description": "Lit des données depuis Firebase Realtime Database",
        "requires": ["requests"],
        "env_vars": ["FIREBASE_URL", "FIREBASE_SECRET"],
        "parameters": {"path": "str"},
        "code": """
def firebase_read(path: str) -> dict:
    import requests
    url = f"{os.getenv('FIREBASE_URL')}/{path}.json?auth={os.getenv('FIREBASE_SECRET')}"
    return requests.get(url).json()
"""
    },
    {
        "name": "pinecone_upsert",
        "category": "cloud",
        "description": "Insère des vecteurs dans Pinecone (base de données vectorielle)",
        "requires": ["pinecone-client"],
        "env_vars": ["PINECONE_API_KEY", "PINECONE_INDEX"],
        "parameters": {"vectors": "list"},
        "code": """
def pinecone_upsert(vectors: list) -> str:
    import pinecone
    pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
    index = pinecone.Index(os.getenv("PINECONE_INDEX"))
    index.upsert(vectors=vectors)
    return f"{len(vectors)} vecteurs insérés"
"""
    },
    {
        "name": "supabase_insert",
        "category": "cloud",
        "description": "Insère une ligne dans une table Supabase",
        "requires": ["supabase"],
        "env_vars": ["SUPABASE_URL", "SUPABASE_KEY"],
        "parameters": {"table": "str", "data": "dict"},
        "code": """
def supabase_insert(table: str, data: dict) -> dict:
    from supabase import create_client
    sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    return sb.table(table).insert(data).execute().data
"""
    },
    {
        "name": "supabase_select",
        "category": "cloud",
        "description": "Lit des données depuis une table Supabase",
        "requires": ["supabase"],
        "env_vars": ["SUPABASE_URL", "SUPABASE_KEY"],
        "parameters": {"table": "str", "filters": "dict = {}"},
        "code": """
def supabase_select(table: str, filters: dict = {}) -> list:
    from supabase import create_client
    sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    query = sb.table(table).select("*")
    for k, v in filters.items():
        query = query.eq(k, v)
    return query.execute().data
"""
    },
]

# ══════════════════════════════════════════════════════════════════
# 💬  CATÉGORIE 13 : COMMUNICATION & RÉSEAUX SOCIAUX
# ══════════════════════════════════════════════════════════════════

SOCIAL_SKILLS = [
    {
        "name": "tweet_post",
        "category": "social",
        "description": "Poste un tweet via l'API Twitter/X",
        "requires": ["tweepy"],
        "env_vars": ["TWITTER_API_KEY", "TWITTER_API_SECRET", "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET"],
        "parameters": {"text": "str"},
        "code": """
def tweet_post(text: str) -> str:
    import tweepy
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
    )
    r = client.create_tweet(text=text)
    return f"Tweet posté, ID: {r.data['id']}"
"""
    },
    {
        "name": "tweet_search",
        "category": "social",
        "description": "Recherche des tweets récents sur un sujet",
        "requires": ["tweepy"],
        "env_vars": ["TWITTER_BEARER_TOKEN"],
        "parameters": {"query": "str", "max_results": "int = 10"},
        "code": """
def tweet_search(query: str, max_results: int = 10) -> list:
    import tweepy
    client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))
    r = client.search_recent_tweets(query=query, max_results=max_results)
    return [t.text for t in (r.data or [])]
"""
    },
    {
        "name": "reddit_post",
        "category": "social",
        "description": "Poste sur Reddit via PRAW",
        "requires": ["praw"],
        "env_vars": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD"],
        "parameters": {"subreddit": "str", "title": "str", "body": "str"},
        "code": """
def reddit_post(subreddit: str, title: str, body: str) -> str:
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
"""
    },
    {
        "name": "reddit_get_hot",
        "category": "social",
        "description": "Récupère les posts populaires d'un subreddit",
        "requires": ["praw"],
        "env_vars": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"],
        "parameters": {"subreddit": "str", "limit": "int = 10"},
        "code": """
def reddit_get_hot(subreddit: str, limit: int = 10) -> list:
    import praw
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="UST Bot"
    )
    return [{"title": p.title, "score": p.score, "url": p.url}
            for p in reddit.subreddit(subreddit).hot(limit=limit)]
"""
    },
    {
        "name": "github_create_repo",
        "category": "social",
        "description": "Crée un nouveau dépôt GitHub",
        "requires": ["requests"],
        "env_vars": ["GITHUB_TOKEN"],
        "parameters": {"name": "str", "description": "str = ''", "private": "bool = False"},
        "code": """
def github_create_repo(name: str, description: str = "", private: bool = False) -> str:
    import requests
    r = requests.post("https://api.github.com/user/repos",
        json={"name": name, "description": description, "private": private},
        headers={"Authorization": f"token {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github.v3+json"})
    return r.json().get("html_url", r.text)
"""
    },
    {
        "name": "github_push_file",
        "category": "social",
        "description": "Push un fichier sur un repo GitHub via l'API",
        "requires": ["requests"],
        "env_vars": ["GITHUB_TOKEN"],
        "parameters": {"repo": "str", "file_path": "str", "content": "str", "message": "str = 'UST commit'"},
        "code": """
def github_push_file(repo: str, file_path: str, content: str, message: str = "UST commit") -> str:
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
"""
    },
    {
        "name": "send_pushover_notification",
        "category": "social",
        "description": "Envoie une notification push via Pushover (mobile)",
        "requires": ["requests"],
        "env_vars": ["PUSHOVER_TOKEN", "PUSHOVER_USER"],
        "parameters": {"title": "str", "message": "str"},
        "code": """
def send_pushover_notification(title: str, message: str) -> str:
    import requests
    r = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": os.getenv("PUSHOVER_TOKEN"),
        "user": os.getenv("PUSHOVER_USER"),
        "title": title,
        "message": message
    })
    return f"Pushover (status {r.status_code})"
"""
    },
    {
        "name": "rss_feed_read",
        "category": "social",
        "description": "Lit un flux RSS et retourne les derniers articles",
        "requires": ["feedparser"],
        "env_vars": [],
        "parameters": {"url": "str", "limit": "int = 5"},
        "code": """
def rss_feed_read(url: str, limit: int = 5) -> list:
    import feedparser
    feed = feedparser.parse(url)
    return [{"title": e.title, "link": e.link, "published": e.get("published", "")}
            for e in feed.entries[:limit]]
"""
    },
]

# ══════════════════════════════════════════════════════════════════
# 🧬  CATÉGORIE 14 : CODE & DÉVELOPPEMENT
# ══════════════════════════════════════════════════════════════════

DEV_SKILLS = [
    {
        "name": "lint_python_code",
        "category": "dev",
        "description": "Analyse la qualité d'un fichier Python (pylint)",
        "requires": ["pylint"],
        "env_vars": [],
        "parameters": {"file_path": "str"},
        "code": """
def lint_python_code(file_path: str) -> str:
    import subprocess
    r = subprocess.run(["pylint", file_path, "--output-format=text"], capture_output=True, text=True)
    return r.stdout or r.stderr
"""
    },
    {
        "name": "format_python_code",
        "category": "dev",
        "description": "Formate du code Python avec Black",
        "requires": ["black"],
        "env_vars": [],
        "parameters": {"file_path": "str"},
        "code": """
def format_python_code(file_path: str) -> str:
    import subprocess
    r = subprocess.run(["black", file_path], capture_output=True, text=True)
    return r.stdout + r.stderr
"""
    },
    {
        "name": "run_pytest",
        "category": "dev",
        "description": "Lance les tests pytest d'un projet",
        "requires": ["pytest"],
        "env_vars": [],
        "parameters": {"test_path": "str = '.'", "verbose": "bool = True"},
        "code": """
def run_pytest(test_path: str = ".", verbose: bool = True) -> str:
    import subprocess
    args = ["pytest", test_path]
    if verbose:
        args.append("-v")
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout + r.stderr
"""
    },
    {
        "name": "git_commit_push",
        "category": "dev",
        "description": "Stage, commit et push tous les changements Git",
        "requires": [],
        "env_vars": [],
        "parameters": {"message": "str = 'UST auto-commit'", "branch": "str = 'main'"},
        "code": """
def git_commit_push(message: str = "UST auto-commit", branch: str = "main") -> str:
    import subprocess
    results = []
    for cmd in [
        ["git", "add", "-A"],
        ["git", "commit", "-m", message],
        ["git", "push", "origin", branch]
    ]:
        r = subprocess.run(cmd, capture_output=True, text=True)
        results.append(r.stdout or r.stderr)
    return "\\n".join(results)
"""
    },
    {
        "name": "git_status",
        "category": "dev",
        "description": "Retourne le statut Git du dossier courant",
        "requires": [],
        "env_vars": [],
        "parameters": {"path": "str = '.'"},
        "code": """
def git_status(path: str = ".") -> str:
    import subprocess
    r = subprocess.run(["git", "-C", path, "status"], capture_output=True, text=True)
    return r.stdout
"""
    },
    {
        "name": "create_virtualenv",
        "category": "dev",
        "description": "Crée un environnement virtuel Python",
        "requires": [],
        "env_vars": [],
        "parameters": {"name": "str = 'venv'"},
        "code": """
def create_virtualenv(name: str = "venv") -> str:
    import subprocess
    r = subprocess.run(["python", "-m", "venv", name], capture_output=True, text=True)
    return f"Virtualenv '{name}' créé" if r.returncode == 0 else r.stderr
"""
    },
    {
        "name": "install_package",
        "category": "dev",
        "description": "Installe un ou plusieurs packages pip",
        "requires": [],
        "env_vars": [],
        "parameters": {"packages": "list"},
        "code": """
def install_package(packages: list) -> str:
    import subprocess
    r = subprocess.run(["pip", "install"] + packages, capture_output=True, text=True)
    return r.stdout or r.stderr
"""
    },
    {
        "name": "generate_requirements",
        "category": "dev",
        "description": "Génère un fichier requirements.txt depuis pip freeze",
        "requires": [],
        "env_vars": [],
        "parameters": {"output": "str = 'requirements.txt'"},
        "code": """
def generate_requirements(output: str = "requirements.txt") -> str:
    import subprocess
    r = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
    with open(output, "w") as f:
        f.write(r.stdout)
    return f"requirements.txt généré : {len(r.stdout.splitlines())} packages"
"""
    },
    {
        "name": "create_dockerfile",
        "category": "dev",
        "description": "Génère un Dockerfile de base pour un projet Python",
        "requires": [],
        "env_vars": [],
        "parameters": {"app_file": "str = 'main.py'", "python_version": "str = '3.11'"},
        "code": """def create_dockerfile(app_file: str = "main.py", python_version: str = "3.11") -> str:
    content = f"FROM python:{python_version}-slim\\nWORKDIR /app\\nCOPY requirements.txt .\\nRUN pip install --no-cache-dir -r requirements.txt\\nCOPY . .\\nCMD [\\"python\\", \\"{app_file}\\"]\\n"
    with open("Dockerfile", "w") as f:
        f.write(content)
    return "Dockerfile créé"
"""
    },
    {
        "name": "docker_run",
        "category": "dev",
        "description": "Lance un conteneur Docker",
        "requires": [],
        "env_vars": [],
        "parameters": {"image": "str", "command": "str = ''", "ports": "str = ''"},
        "code": """
def docker_run(image: str, command: str = "", ports: str = "") -> str:
    import subprocess
    args = ["docker", "run", "-d"]
    if ports:
        args += ["-p", ports]
    args.append(image)
    if command:
        args += command.split()
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout.strip() or r.stderr
"""
    },
    {
        "name": "convert_code_language",
        "category": "dev",
        "description": "Convertit du code d'un langage à un autre via IA (OpenAI)",
        "requires": ["openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"code": "str", "from_lang": "str", "to_lang": "str"},
        "code": """
def convert_code_language(code: str, from_lang: str, to_lang: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Convertis ce code {from_lang} en {to_lang}. Retourne uniquement le code, sans explications.\\n\\n{code}"
    r = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
    return r.choices[0].message.content
"""
    },
    {
        "name": "explain_code",
        "category": "dev",
        "description": "Explique un bout de code en langage naturel (via IA)",
        "requires": ["openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"code": "str", "language": "str = 'Python'"},
        "code": """
def explain_code(code: str, language: str = "Python") -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Explique ce code {language} en français, simplement :\\n\\n{code}"
    r = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
    return r.choices[0].message.content
"""
    },
]

# ══════════════════════════════════════════════════════════════════
# 🧠  CATÉGORIE 15 : MÉMOIRE & BASE DE CONNAISSANCES (RAG)
# ══════════════════════════════════════════════════════════════════

MEMORY_SKILLS = [
    {
        "name": "memory_add",
        "category": "memory",
        "description": "Ajoute une information à la mémoire locale (JSON)",
        "requires": [],
        "env_vars": [],
        "parameters": {"key": "str", "value": "str", "db_path": "str = 'ust_memory.json'"},
        "code": """
def memory_add(key: str, value: str, db_path: str = "ust_memory.json") -> str:
    import json, os
    db = {}
    if os.path.exists(db_path):
        with open(db_path) as f:
            db = json.load(f)
    db[key] = value
    with open(db_path, "w") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    return f"Mémorisé : {key}"
"""
    },
    {
        "name": "memory_get",
        "category": "memory",
        "description": "Récupère une information mémorisée",
        "requires": [],
        "env_vars": [],
        "parameters": {"key": "str", "db_path": "str = 'ust_memory.json'"},
        "code": """
def memory_get(key: str, db_path: str = "ust_memory.json") -> str:
    import json, os
    if not os.path.exists(db_path):
        return f"Clé non trouvée : {key}"
    with open(db_path) as f:
        db = json.load(f)
    return db.get(key, f"Clé non trouvée : {key}")
"""
    },
    {
        "name": "memory_list",
        "category": "memory",
        "description": "Liste toutes les entrées mémorisées",
        "requires": [],
        "env_vars": [],
        "parameters": {"db_path": "str = 'ust_memory.json'"},
        "code": """
def memory_list(db_path: str = "ust_memory.json") -> dict:
    import json, os
    if not os.path.exists(db_path):
        return {}
    with open(db_path) as f:
        return json.load(f)
"""
    },
    {
        "name": "memory_delete",
        "category": "memory",
        "description": "Supprime une entrée mémorisée",
        "requires": [],
        "env_vars": [],
        "parameters": {"key": "str", "db_path": "str = 'ust_memory.json'"},
        "code": """
def memory_delete(key: str, db_path: str = "ust_memory.json") -> str:
    import json, os
    if not os.path.exists(db_path):
        return "Mémoire vide"
    with open(db_path) as f:
        db = json.load(f)
    db.pop(key, None)
    with open(db_path, "w") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    return f"Supprimé : {key}"
"""
    },
    {
        "name": "rag_index_folder",
        "category": "memory",
        "description": "Indexe tous les fichiers texte d'un dossier pour RAG (recherche sémantique locale)",
        "requires": ["chromadb", "openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"folder": "str", "collection_name": "str = 'ust_docs'"},
        "code": """
def rag_index_folder(folder: str, collection_name: str = "ust_docs") -> str:
    import os, chromadb
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    chroma = chromadb.PersistentClient(path=".ust_chroma")
    col = chroma.get_or_create_collection(collection_name)
    count = 0
    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()[:4000]
            emb = client.embeddings.create(input=content, model="text-embedding-3-small").data[0].embedding
            col.upsert(ids=[fname], documents=[content], embeddings=[emb])
            count += 1
        except:
            pass
    return f"{count} fichiers indexés dans '{collection_name}'"
"""
    },
    {
        "name": "rag_search",
        "category": "memory",
        "description": "Recherche sémantique dans les documents indexés (RAG local)",
        "requires": ["chromadb", "openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"query": "str", "collection_name": "str = 'ust_docs'", "n_results": "int = 3"},
        "code": """
def rag_search(query: str, collection_name: str = "ust_docs", n_results: int = 3) -> list:
    import chromadb
    from openai import OpenAI
    import os
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    chroma = chromadb.PersistentClient(path=".ust_chroma")
    col = chroma.get_or_create_collection(collection_name)
    emb = client.embeddings.create(input=query, model="text-embedding-3-small").data[0].embedding
    results = col.query(query_embeddings=[emb], n_results=n_results)
    return results["documents"][0]
"""
    },
    {
        "name": "rag_ask",
        "category": "memory",
        "description": "Pose une question à tes documents indexés (RAG complet)",
        "requires": ["chromadb", "openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"question": "str", "collection_name": "str = 'ust_docs'"},
        "code": """
def rag_ask(question: str, collection_name: str = "ust_docs") -> str:
    import chromadb
    from openai import OpenAI
    import os
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    chroma = chromadb.PersistentClient(path=".ust_chroma")
    col = chroma.get_or_create_collection(collection_name)
    emb = client.embeddings.create(input=question, model="text-embedding-3-small").data[0].embedding
    docs = col.query(query_embeddings=[emb], n_results=3)["documents"][0]
    context = "\\n\\n---\\n\\n".join(docs)
    prompt = f"Réponds à la question en te basant uniquement sur ces documents :\\n\\n{context}\\n\\nQuestion: {question}"
    r = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
    return r.choices[0].message.content
"""
    },
]

# ══════════════════════════════════════════════════════════════════
# 🔧  CATÉGORIE 16 : API & INTÉGRATIONS DIVERSES
# ══════════════════════════════════════════════════════════════════

API_SKILLS = [
    {
        "name": "call_rest_api",
        "category": "api",
        "description": "Appelle une API REST générique (GET/POST/PUT/DELETE)",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"url": "str", "method": "str = 'GET'", "headers": "dict = {}", "body": "dict = {}"},
        "code": """
def call_rest_api(url: str, method: str = "GET", headers: dict = {}, body: dict = {}) -> dict:
    import requests
    r = requests.request(method, url, headers=headers, json=body or None, timeout=10)
    try:
        return r.json()
    except:
        return {"status": r.status_code, "text": r.text}
"""
    },
    {
        "name": "get_news_headlines",
        "category": "api",
        "description": "Récupère les dernières actualités via NewsAPI",
        "requires": ["requests"],
        "env_vars": ["NEWSAPI_KEY"],
        "parameters": {"query": "str = 'technology'", "language": "str = 'fr'", "count": "int = 5"},
        "code": """
def get_news_headlines(query: str = "technology", language: str = "fr", count: int = 5) -> list:
    import requests
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&pageSize={count}&apiKey={os.getenv('NEWSAPI_KEY')}"
    r = requests.get(url).json()
    return [{"title": a["title"], "url": a["url"], "source": a["source"]["name"]}
            for a in r.get("articles", [])]
"""
    },
    {
        "name": "get_wikipedia_summary",
        "category": "api",
        "description": "Retourne le résumé Wikipedia d'un sujet",
        "requires": ["wikipedia"],
        "env_vars": [],
        "parameters": {"topic": "str", "lang": "str = 'fr'"},
        "code": """
def get_wikipedia_summary(topic: str, lang: str = "fr") -> str:
    import wikipedia
    wikipedia.set_lang(lang)
    try:
        return wikipedia.summary(topic, sentences=5)
    except Exception as e:
        return f"Erreur : {e}"
"""
    },
    {
        "name": "get_definition",
        "category": "api",
        "description": "Retourne la définition d'un mot (anglais) via Free Dictionary API",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"word": "str"},
        "code": """
def get_definition(word: str) -> str:
    import requests
    r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}").json()
    if isinstance(r, list):
        meanings = r[0].get("meanings", [])
        if meanings:
            defs = meanings[0].get("definitions", [])
            if defs:
                return defs[0].get("definition", "Aucune définition trouvée")
    return "Aucune définition trouvée"
"""
    },
    {
        "name": "get_movie_info",
        "category": "api",
        "description": "Retourne les infos d'un film via OMDB API",
        "requires": ["requests"],
        "env_vars": ["OMDB_API_KEY"],
        "parameters": {"title": "str"},
        "code": """
def get_movie_info(title: str) -> dict:
    import requests
    r = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={os.getenv('OMDB_API_KEY')}").json()
    return {"title": r.get("Title"), "year": r.get("Year"), "plot": r.get("Plot"), "rating": r.get("imdbRating"), "genre": r.get("Genre")}
"""
    },
    {
        "name": "get_holidays",
        "category": "api",
        "description": "Retourne les jours fériés d'un pays pour une année donnée",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"country": "str = 'FR'", "year": "int = 2025"},
        "code": """
def get_holidays(country: str = "FR", year: int = 2025) -> list:
    import requests
    r = requests.get(f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country}").json()
    return [{"date": h["date"], "name": h["name"]} for h in r]
"""
    },
    {
        "name": "get_iss_location",
        "category": "api",
        "description": "Retourne la position actuelle de la Station Spatiale Internationale",
        "requires": ["requests"],
        "env_vars": [],
        "code": """
def get_iss_location() -> dict:
    import requests
    r = requests.get("http://api.open-notify.org/iss-now.json").json()
    pos = r["iss_position"]
    return {"latitude": pos["latitude"], "longitude": pos["longitude"], "timestamp": r["timestamp"]}
"""
    },
    {
        "name": "generate_barcode",
        "category": "api",
        "description": "Génère un code-barres EAN13 ou Code128",
        "requires": ["python-barcode", "pillow"],
        "env_vars": [],
        "parameters": {"data": "str", "barcode_type": "str = 'code128'", "output": "str = 'barcode'"},
        "code": """
def generate_barcode(data: str, barcode_type: str = "code128", output: str = "barcode") -> str:
    import barcode
    from barcode.writer import ImageWriter
    bc = barcode.get(barcode_type, data, writer=ImageWriter())
    path = bc.save(output)
    return f"Code-barres généré : {path}"
"""
    },
    {
        "name": "ip_reputation_check",
        "category": "api",
        "description": "Vérifie la réputation d'une adresse IP via AbuseIPDB",
        "requires": ["requests"],
        "env_vars": ["ABUSEIPDB_KEY"],
        "parameters": {"ip": "str"},
        "code": """
def ip_reputation_check(ip: str) -> dict:
    import requests
    r = requests.get("https://api.abuseipdb.com/api/v2/check",
        headers={"Key": os.getenv("ABUSEIPDB_KEY"), "Accept": "application/json"},
        params={"ipAddress": ip, "maxAgeInDays": 90})
    data = r.json().get("data", {})
    return {"ip": ip, "abuse_score": data.get("abuseConfidenceScore"), "country": data.get("countryCode"), "reports": data.get("totalReports")}
"""
    },
    {
        "name": "wolfram_alpha_query",
        "category": "api",
        "description": "Envoie une question à Wolfram Alpha (calculs, sciences, etc.)",
        "requires": ["wolframalpha"],
        "env_vars": ["WOLFRAM_APP_ID"],
        "parameters": {"query": "str"},
        "code": """
def wolfram_alpha_query(query: str) -> str:
    import wolframalpha
    client = wolframalpha.Client(os.getenv("WOLFRAM_APP_ID"))
    res = client.query(query)
    pods = list(res.results)
    return str(next(iter(pods)).text) if pods else "Aucun résultat"
"""
    },
]

ALL_SKILLS = (
    AI_SKILLS + SYSTEM_SKILLS + WEB_SKILLS + FILE_SKILLS + PRODUCTIVITY_SKILLS + MEDIA_SKILLS + SMART_HOME_SKILLS + SECURITY_SKILLS + DATA_SKILLS + MISC_SKILLS + AUTOMATION_SKILLS + CLOUD_SKILLS + SOCIAL_SKILLS + DEV_SKILLS + MEMORY_SKILLS + API_SKILLS
)
'''

with open("skills_catalog.py", "w", encoding="utf-8") as f:
    f.write(content)
