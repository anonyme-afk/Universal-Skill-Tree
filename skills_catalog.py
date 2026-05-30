"""
╔══════════════════════════════════════════════════════════════════╗
║           UST — UNIVERSAL SKILL TREE                            ║
║           CATALOGUE COMPLET DE SKILLS                           ║
║           200+ skills, tous plug & play                         ║
╚══════════════════════════════════════════════════════════════════╝

FORMAT DE CHAQUE SKILL :
{
    "name": "nom_du_skill",
    "category": "catégorie",
    "description": "ce que ça fait",
    "requires": ["pip_package_1", "pip_package_2"],
    "env_vars": ["MA_CLE_API"],       # variables d'environnement nécessaires
    "function": callable,             # la vraie fonction Python
    "parameters": {...}               # schema JSON des paramètres
}
"""

import os
import json
import subprocess
import datetime
import platform
import importlib

# ══════════════════════════════════════════════════════════════════
# 🧠  CATÉGORIE 1 : IA & LLMs
# ══════════════════════════════════════════════════════════════════

AI_SKILLS = [
    {
        "name": "chat_openai",
        "category": "ai",
        "description": "Envoie un message à GPT-4o / GPT-3.5 via OpenAI",
        "requires": ["openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"prompt": "str", "model": "str = 'gpt-4o-mini'"},
        "code": """
def chat_openai(prompt: str, model: str = "gpt-4o-mini") -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = client.chat.completions.create(model=model, messages=[{"role":"user","content":prompt}])
    return r.choices[0].message.content
"""
    },
    {
        "name": "chat_gemini",
        "category": "ai",
        "description": "Envoie un message à Google Gemini",
        "requires": ["google-generativeai"],
        "env_vars": ["GEMINI_API_KEY"],
        "parameters": {"prompt": "str", "model": "str = 'gemini-pro'"},
        "code": """
def chat_gemini(prompt: str, model: str = "gemini-pro") -> str:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    m = genai.GenerativeModel(model)
    return m.generate_content(prompt).text
"""
    },
    {
        "name": "chat_ollama",
        "category": "ai",
        "description": "Parle à un LLM local via Ollama (llama3, mistral, etc.)",
        "requires": ["ollama"],
        "env_vars": [],
        "parameters": {"prompt": "str", "model": "str = 'llama3'"},
        "code": """
def chat_ollama(prompt: str, model: str = "llama3") -> str:
    import ollama
    r = ollama.chat(model=model, messages=[{"role":"user","content":prompt}])
    return r['message']['content']
"""
    },
    {
        "name": "chat_openrouter",
        "category": "ai",
        "description": "Accède à 200+ modèles via OpenRouter",
        "requires": ["openai"],
        "env_vars": ["OPENROUTER_API_KEY"],
        "parameters": {"prompt": "str", "model": "str = 'openai/gpt-4o-mini'"},
        "code": """
def chat_openrouter(prompt: str, model: str = "openai/gpt-4o-mini") -> str:
    from openai import OpenAI
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
    r = client.chat.completions.create(model=model, messages=[{"role":"user","content":prompt}])
    return r.choices[0].message.content
"""
    },
    {
        "name": "chat_anthropic",
        "category": "ai",
        "description": "Parle à Claude (Anthropic) via l'API officielle",
        "requires": ["anthropic"],
        "env_vars": ["ANTHROPIC_API_KEY"],
        "parameters": {"prompt": "str", "model": "str = 'claude-3-haiku-20240307'"},
        "code": """
def chat_anthropic(prompt: str, model: str = "claude-3-haiku-20240307") -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    msg = client.messages.create(model=model, max_tokens=1024, messages=[{"role":"user","content":prompt}])
    return msg.content[0].text
"""
    },
    {
        "name": "generate_image_dalle",
        "category": "ai",
        "description": "Génère une image via DALL-E 3",
        "requires": ["openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"prompt": "str", "size": "str = '1024x1024'"},
        "code": """
def generate_image_dalle(prompt: str, size: str = "1024x1024") -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = client.images.generate(model="dall-e-3", prompt=prompt, size=size, n=1)
    return r.data[0].url
"""
    },
    {
        "name": "transcribe_whisper",
        "category": "ai",
        "description": "Transcrit un fichier audio en texte via Whisper (OpenAI)",
        "requires": ["openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"audio_path": "str"},
        "code": """
def transcribe_whisper(audio_path: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    with open(audio_path, "rb") as f:
        r = client.audio.transcriptions.create(model="whisper-1", file=f)
    return r.text
"""
    },
    {
        "name": "transcribe_whisper_local",
        "category": "ai",
        "description": "Transcrit un fichier audio localement via faster-whisper (gratuit, offline)",
        "requires": ["faster-whisper"],
        "env_vars": [],
        "parameters": {"audio_path": "str", "model_size": "str = 'base'"},
        "code": """
def transcribe_whisper_local(audio_path: str, model_size: str = "base") -> str:
    from faster_whisper import WhisperModel
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path)
    return " ".join([s.text for s in segments])
"""
    },
    {
        "name": "embed_text",
        "category": "ai",
        "description": "Génère des embeddings vectoriels d'un texte (OpenAI)",
        "requires": ["openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"text": "str"},
        "code": """
def embed_text(text: str) -> list:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = client.embeddings.create(input=text, model="text-embedding-3-small")
    return r.data[0].embedding
"""
    },
    {
        "name": "analyze_image_vision",
        "category": "ai",
        "description": "Analyse une image avec GPT-4 Vision",
        "requires": ["openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"image_url": "str", "question": "str = 'Décris cette image'"},
        "code": """
def analyze_image_vision(image_url: str, question: str = "Décris cette image") -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user","content":[
            {"type":"text","text":question},
            {"type":"image_url","image_url":{"url":image_url}}
        ]}]
    )
    return r.choices[0].message.content
"""
    },
]

# ══════════════════════════════════════════════════════════════════
# 🖥️  CATÉGORIE 2 : SYSTÈME & OS
# ══════════════════════════════════════════════════════════════════

SYSTEM_SKILLS = [
    {
        "name": "get_cpu_usage",
        "category": "system",
        "description": "Retourne l'utilisation CPU en %",
        "requires": ["psutil"],
        "env_vars": [],
        "code": """
def get_cpu_usage() -> float:
    import psutil
    return psutil.cpu_percent(interval=1)
"""
    },
    {
        "name": "get_ram_usage",
        "category": "system",
        "description": "Retourne l'utilisation RAM",
        "requires": ["psutil"],
        "env_vars": [],
        "code": """
def get_ram_usage() -> dict:
    import psutil
    m = psutil.virtual_memory()
    return {"total_gb": round(m.total/1e9,2), "used_gb": round(m.used/1e9,2), "percent": m.percent}
"""
    },
    {
        "name": "get_disk_usage",
        "category": "system",
        "description": "Retourne l'espace disque disponible",
        "requires": ["psutil"],
        "env_vars": [],
        "parameters": {"path": "str = '/'"},
        "code": """
def get_disk_usage(path: str = "/") -> dict:
    import psutil
    d = psutil.disk_usage(path)
    return {"total_gb": round(d.total/1e9,2), "used_gb": round(d.used/1e9,2), "free_gb": round(d.free/1e9,2), "percent": d.percent}
"""
    },
    {
        "name": "run_command",
        "category": "system",
        "description": "Exécute une commande shell et retourne la sortie",
        "requires": [],
        "env_vars": [],
        "parameters": {"command": "str"},
        "requires_confirmation": True,
        "code": """
def run_command(command: str) -> str:
    import subprocess
    r = subprocess.run(command, shell=True, capture_output=True, text=True)
    return r.stdout or r.stderr
"""
    },
    {
        "name": "list_processes",
        "category": "system",
        "description": "Liste les processus actifs (top 20 par CPU)",
        "requires": ["psutil"],
        "env_vars": [],
        "code": """
def list_processes() -> list:
    import psutil
    procs = []
    for p in psutil.process_iter(['pid','name','cpu_percent','memory_percent']):
        try:
            procs.append(p.info)
        except:
            pass
    return sorted(procs, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:20]
"""
    },
    {
        "name": "kill_process",
        "category": "system",
        "description": "Tue un processus par son PID",
        "requires": ["psutil"],
        "env_vars": [],
        "parameters": {"pid": "int"},
        "requires_confirmation": True,
        "code": """
def kill_process(pid: int) -> str:
    import psutil
    try:
        p = psutil.Process(pid)
        p.kill()
        return f"Processus {pid} tué"
    except Exception as e:
        return f"Erreur: {e}"
"""
    },
    {
        "name": "get_os_info",
        "category": "system",
        "description": "Retourne les infos du système d'exploitation",
        "requires": [],
        "env_vars": [],
        "code": """
def get_os_info() -> dict:
    import platform
    return {
        "os": platform.system(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
        "python": platform.python_version()
    }
"""
    },
    {
        "name": "get_battery_status",
        "category": "system",
        "description": "Retourne l'état de la batterie",
        "requires": ["psutil"],
        "env_vars": [],
        "code": """
def get_battery_status() -> dict:
    import psutil
    b = psutil.sensors_battery()
    if not b:
        return {"error": "Pas de batterie détectée"}
    return {"percent": b.percent, "charging": b.power_plugged, "time_left_min": round(b.secsleft/60) if b.secsleft > 0 else "inconnu"}
"""
    },
    {
        "name": "screenshot",
        "category": "system",
        "description": "Prend une capture d'écran et la sauvegarde",
        "requires": ["pillow"],
        "env_vars": [],
        "parameters": {"save_path": "str = 'screenshot.png'"},
        "code": """
def screenshot(save_path: str = "screenshot.png") -> str:
    from PIL import ImageGrab
    img = ImageGrab.grab()
    img.save(save_path)
    return f"Screenshot sauvegardé : {save_path}"
"""
    },
    {
        "name": "set_clipboard",
        "category": "system",
        "description": "Met du texte dans le presse-papier",
        "requires": ["pyperclip"],
        "env_vars": [],
        "parameters": {"text": "str"},
        "code": """
def set_clipboard(text: str) -> str:
    import pyperclip
    pyperclip.copy(text)
    return "Texte copié dans le presse-papier"
"""
    },
    {
        "name": "get_clipboard",
        "category": "system",
        "description": "Lit le contenu du presse-papier",
        "requires": ["pyperclip"],
        "env_vars": [],
        "code": """
def get_clipboard() -> str:
    import pyperclip
    return pyperclip.paste()
"""
    },
    {
        "name": "open_url_browser",
        "category": "system",
        "description": "Ouvre une URL dans le navigateur par défaut",
        "requires": [],
        "env_vars": [],
        "parameters": {"url": "str"},
        "code": """
def open_url_browser(url: str) -> str:
    import webbrowser
    webbrowser.open(url)
    return f"URL ouverte : {url}"
"""
    },
    {
        "name": "send_notification_desktop",
        "category": "system",
        "description": "Envoie une notification desktop (Windows/Mac/Linux)",
        "requires": ["plyer"],
        "env_vars": [],
        "parameters": {"title": "str", "message": "str"},
        "code": """
def send_notification_desktop(title: str, message: str) -> str:
    from plyer import notification
    notification.notify(title=title, message=message, timeout=5)
    return f"Notification envoyée : {title}"
"""
    },
    {
        "name": "get_network_speed",
        "category": "system",
        "description": "Retourne les stats réseau (bytes envoyés/reçus)",
        "requires": ["psutil"],
        "env_vars": [],
        "code": """
def get_network_speed() -> dict:
    import psutil, time
    n1 = psutil.net_io_counters()
    time.sleep(1)
    n2 = psutil.net_io_counters()
    return {
        "download_kbps": round((n2.bytes_recv - n1.bytes_recv) / 1024, 2),
        "upload_kbps": round((n2.bytes_sent - n1.bytes_sent) / 1024, 2)
    }
"""
    },
    {
        "name": "lock_screen",
        "category": "system",
        "description": "Verrouille l'écran (Windows/Mac/Linux)",
        "requires": [],
        "env_vars": [],
        "code": """
def lock_screen() -> str:
    import platform, subprocess
    s = platform.system()
    if s == "Windows":
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
    elif s == "Darwin":
        subprocess.run(["pmset", "displaysleepnow"])
    else:
        subprocess.run(["xdg-screensaver", "lock"])
    return "Écran verrouillé"
"""
    },
]

# ══════════════════════════════════════════════════════════════════
# 🌐  CATÉGORIE 3 : WEB & RÉSEAU
# ══════════════════════════════════════════════════════════════════

WEB_SKILLS = [
    {
        "name": "web_search_ddg",
        "category": "web",
        "description": "Recherche sur DuckDuckGo (gratuit, sans API key)",
        "requires": ["duckduckgo-search"],
        "env_vars": [],
        "parameters": {"query": "str", "max_results": "int = 5"},
        "code": """
def web_search_ddg(query: str, max_results: int = 5) -> list:
    from duckduckgo_search import DDGS
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))
"""
    },
    {
        "name": "web_search_google",
        "category": "web",
        "description": "Recherche Google via SerpAPI",
        "requires": ["google-search-results"],
        "env_vars": ["SERPAPI_KEY"],
        "parameters": {"query": "str"},
        "code": """
def web_search_google(query: str) -> list:
    from serpapi import GoogleSearch
    s = GoogleSearch({"q": query, "api_key": os.getenv("SERPAPI_KEY")})
    return s.get_dict().get("organic_results", [])
"""
    },
    {
        "name": "scrape_webpage",
        "category": "web",
        "description": "Extrait le texte d'une page web",
        "requires": ["requests", "beautifulsoup4"],
        "env_vars": [],
        "parameters": {"url": "str"},
        "code": """
def scrape_webpage(url: str) -> str:
    import requests
    from bs4 import BeautifulSoup
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script","style","nav","footer"]):
        tag.decompose()
    return soup.get_text(separator="\\n", strip=True)[:5000]
"""
    },
    {
        "name": "download_file",
        "category": "web",
        "description": "Télécharge un fichier depuis une URL",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"url": "str", "save_path": "str"},
        "code": """
def download_file(url: str, save_path: str) -> str:
    import requests
    r = requests.get(url, stream=True)
    with open(save_path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    return f"Fichier téléchargé : {save_path}"
"""
    },
    {
        "name": "check_website_status",
        "category": "web",
        "description": "Vérifie si un site web est accessible",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"url": "str"},
        "code": """
def check_website_status(url: str) -> dict:
    import requests, time
    start = time.time()
    try:
        r = requests.get(url, timeout=5)
        return {"status": r.status_code, "online": True, "response_ms": round((time.time()-start)*1000)}
    except:
        return {"status": None, "online": False, "response_ms": None}
"""
    },
    {
        "name": "get_public_ip",
        "category": "web",
        "description": "Retourne l'IP publique de la machine",
        "requires": ["requests"],
        "env_vars": [],
        "code": """
def get_public_ip() -> str:
    import requests
    return requests.get("https://api.ipify.org").text
"""
    },
    {
        "name": "get_geolocation",
        "category": "web",
        "description": "Géolocalise une adresse IP",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"ip": "str = 'auto'"},
        "code": """
def get_geolocation(ip: str = "auto") -> dict:
    import requests
    url = f"https://ipapi.co/{ip}/json/" if ip != "auto" else "https://ipapi.co/json/"
    return requests.get(url).json()
"""
    },
    {
        "name": "send_webhook",
        "category": "web",
        "description": "Envoie une requête POST à un webhook",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"url": "str", "data": "dict"},
        "code": """
def send_webhook(url: str, data: dict) -> str:
    import requests
    r = requests.post(url, json=data)
    return f"Status: {r.status_code}"
"""
    },
    {
        "name": "get_weather",
        "category": "web",
        "description": "Météo d'une ville via Open-Meteo (gratuit, sans API key)",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"city": "str"},
        "code": """
def get_weather(city: str) -> dict:
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
"""
    },
    {
        "name": "get_crypto_price",
        "category": "web",
        "description": "Retourne le prix d'une crypto en temps réel",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"symbol": "str = 'bitcoin'"},
        "code": """
def get_crypto_price(symbol: str = "bitcoin") -> dict:
    import requests
    r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd,eur").json()
    return r.get(symbol, {"error": "Crypto non trouvée"})
"""
    },
    {
        "name": "get_stock_price",
        "category": "web",
        "description": "Prix d'une action en temps réel via Yahoo Finance",
        "requires": ["yfinance"],
        "env_vars": [],
        "parameters": {"ticker": "str"},
        "code": """
def get_stock_price(ticker: str) -> dict:
    import yfinance as yf
    t = yf.Ticker(ticker)
    info = t.fast_info
    return {"ticker": ticker, "price": info.last_price, "currency": info.currency}
"""
    },
    {
        "name": "translate_text",
        "category": "web",
        "description": "Traduit un texte via Google Translate (gratuit)",
        "requires": ["deep-translator"],
        "env_vars": [],
        "parameters": {"text": "str", "target_lang": "str = 'fr'"},
        "code": """
def translate_text(text: str, target_lang: str = "fr") -> str:
    from deep_translator import GoogleTranslator
    return GoogleTranslator(source="auto", target=target_lang).translate(text)
"""
    },
    {
        "name": "shorten_url",
        "category": "web",
        "description": "Raccourcit une URL via TinyURL",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"url": "str"},
        "code": """
def shorten_url(url: str) -> str:
    import requests
    r = requests.get(f"https://tinyurl.com/api-create.php?url={url}")
    return r.text
"""
    },
    {
        "name": "get_exchange_rate",
        "category": "web",
        "description": "Taux de change entre deux devises",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"from_currency": "str = 'USD'", "to_currency": "str = 'EUR'"},
        "code": """
def get_exchange_rate(from_currency: str = "USD", to_currency: str = "EUR") -> dict:
    import requests
    r = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}").json()
    rate = r["rates"].get(to_currency)
    return {"from": from_currency, "to": to_currency, "rate": rate}
"""
    },
]

# ══════════════════════════════════════════════════════════════════
# 📁  CATÉGORIE 4 : FICHIERS & DOSSIERS
# ══════════════════════════════════════════════════════════════════

FILE_SKILLS = [
    {
        "name": "read_file",
        "category": "files",
        "description": "Lit le contenu d'un fichier texte",
        "requires": [],
        "env_vars": [],
        "parameters": {"path": "str"},
        "code": """
def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {e}"
"""
    },
    {
        "name": "write_file",
        "category": "files",
        "description": "Écrit du texte dans un fichier",
        "requires": [],
        "env_vars": [],
        "parameters": {"path": "str", "content": "str", "append": "bool = False"},
        "code": """
def write_file(path: str, content: str, append: bool = False) -> str:
    mode = "a" if append else "w"
    with open(path, mode, encoding="utf-8") as f:
        f.write(content)
    return f"Fichier écrit : {path}"
"""
    },
    {
        "name": "list_files",
        "category": "files",
        "description": "Liste les fichiers d'un dossier",
        "requires": [],
        "env_vars": [],
        "parameters": {"path": "str = '.'", "pattern": "str = '*'"},
        "code": """
def list_files(path: str = ".", pattern: str = "*") -> list:
    import glob
    return glob.glob(f"{path}/{pattern}")
"""
    },
    {
        "name": "search_in_files",
        "category": "files",
        "description": "Cherche un texte dans tous les fichiers d'un dossier",
        "requires": [],
        "env_vars": [],
        "parameters": {"folder": "str", "search_text": "str"},
        "code": """
def search_in_files(folder: str, search_text: str) -> list:
    import os
    results = []
    for root, _, files in os.walk(folder):
        for f in files:
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                    for i, line in enumerate(fp, 1):
                        if search_text.lower() in line.lower():
                            results.append({"file": path, "line": i, "content": line.strip()})
            except:
                pass
    return results
"""
    },
    {
        "name": "read_pdf",
        "category": "files",
        "description": "Extrait le texte d'un fichier PDF",
        "requires": ["pymupdf"],
        "env_vars": [],
        "parameters": {"path": "str"},
        "code": """
def read_pdf(path: str) -> str:
    import fitz
    doc = fitz.open(path)
    return "\\n".join([page.get_text() for page in doc])
"""
    },
    {
        "name": "read_excel",
        "category": "files",
        "description": "Lit un fichier Excel et retourne les données",
        "requires": ["openpyxl"],
        "env_vars": [],
        "parameters": {"path": "str", "sheet": "str = None"},
        "code": """
def read_excel(path: str, sheet: str = None) -> list:
    import openpyxl
    wb = openpyxl.load_workbook(path)
    ws = wb[sheet] if sheet else wb.active
    return [[cell.value for cell in row] for row in ws.iter_rows()]
"""
    },
    {
        "name": "read_csv",
        "category": "files",
        "description": "Lit un fichier CSV et retourne les données",
        "requires": [],
        "env_vars": [],
        "parameters": {"path": "str"},
        "code": """
def read_csv(path: str) -> list:
    import csv
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))
"""
    },
    {
        "name": "write_csv",
        "category": "files",
        "description": "Écrit des données dans un fichier CSV",
        "requires": [],
        "env_vars": [],
        "parameters": {"path": "str", "data": "list", "headers": "list"},
        "code": """
def write_csv(path: str, data: list, headers: list) -> str:
    import csv
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(data)
    return f"CSV écrit : {path}"
"""
    },
    {
        "name": "compress_folder",
        "category": "files",
        "description": "Compresse un dossier en ZIP",
        "requires": [],
        "env_vars": [],
        "parameters": {"folder_path": "str", "output_path": "str"},
        "code": """
def compress_folder(folder_path: str, output_path: str) -> str:
    import shutil
    shutil.make_archive(output_path.replace(".zip",""), "zip", folder_path)
    return f"Archive créée : {output_path}"
"""
    },
    {
        "name": "extract_zip",
        "category": "files",
        "description": "Extrait un fichier ZIP",
        "requires": [],
        "env_vars": [],
        "parameters": {"zip_path": "str", "extract_to": "str = '.'"},
        "code": """
def extract_zip(zip_path: str, extract_to: str = ".") -> str:
    import zipfile
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_to)
    return f"Extrait dans : {extract_to}"
"""
    },
    {
        "name": "convert_image",
        "category": "files",
        "description": "Convertit une image vers un autre format (PNG, JPEG, WEBP...)",
        "requires": ["pillow"],
        "env_vars": [],
        "parameters": {"input_path": "str", "output_path": "str"},
        "code": """
def convert_image(input_path: str, output_path: str) -> str:
    from PIL import Image
    img = Image.open(input_path)
    img.save(output_path)
    return f"Image convertie : {output_path}"
"""
    },
    {
        "name": "resize_image",
        "category": "files",
        "description": "Redimensionne une image",
        "requires": ["pillow"],
        "env_vars": [],
        "parameters": {"path": "str", "width": "int", "height": "int", "output": "str"},
        "code": """
def resize_image(path: str, width: int, height: int, output: str) -> str:
    from PIL import Image
    img = Image.open(path).resize((width, height))
    img.save(output)
    return f"Image redimensionnée : {output}"
"""
    },
    {
        "name": "pdf_to_images",
        "category": "files",
        "description": "Convertit chaque page d'un PDF en image",
        "requires": ["pymupdf", "pillow"],
        "env_vars": [],
        "parameters": {"pdf_path": "str", "output_folder": "str = 'pdf_pages'"},
        "code": """
def pdf_to_images(pdf_path: str, output_folder: str = "pdf_pages") -> str:
    import fitz, os
    from PIL import Image
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        pix.save(f"{output_folder}/page_{i+1}.png")
    return f"{len(doc)} pages extraites dans {output_folder}"
"""
    },
    {
        "name": "get_file_info",
        "category": "files",
        "description": "Retourne les métadonnées d'un fichier",
        "requires": [],
        "env_vars": [],
        "parameters": {"path": "str"},
        "code": """
def get_file_info(path: str) -> dict:
    import os, datetime
    s = os.stat(path)
    return {
        "name": os.path.basename(path),
        "size_kb": round(s.st_size / 1024, 2),
        "created": str(datetime.datetime.fromtimestamp(s.st_ctime)),
        "modified": str(datetime.datetime.fromtimestamp(s.st_mtime)),
        "extension": os.path.splitext(path)[1]
    }
"""
    },
]

# ══════════════════════════════════════════════════════════════════
# 📅  CATÉGORIE 5 : PRODUCTIVITÉ
# ══════════════════════════════════════════════════════════════════

PRODUCTIVITY_SKILLS = [
    {
        "name": "send_email_smtp",
        "category": "productivity",
        "description": "Envoie un email via SMTP (Gmail, Outlook...)",
        "requires": [],
        "env_vars": ["EMAIL_ADDRESS", "EMAIL_PASSWORD", "SMTP_HOST", "SMTP_PORT"],
        "parameters": {"to": "str", "subject": "str", "body": "str"},
        "code": """
def send_email_smtp(to: str, subject: str, body: str) -> str:
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
"""
    },
    {
        "name": "send_discord_message",
        "category": "productivity",
        "description": "Envoie un message dans un canal Discord via webhook",
        "requires": ["requests"],
        "env_vars": ["DISCORD_WEBHOOK_URL"],
        "parameters": {"message": "str", "username": "str = 'UST Bot'"},
        "code": """
def send_discord_message(message: str, username: str = "UST Bot") -> str:
    import requests
    r = requests.post(os.getenv("DISCORD_WEBHOOK_URL"), json={"content": message, "username": username})
    return f"Status: {r.status_code}"
"""
    },
    {
        "name": "send_telegram_message",
        "category": "productivity",
        "description": "Envoie un message Telegram",
        "requires": ["python-telegram-bot"],
        "env_vars": ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"],
        "parameters": {"message": "str"},
        "code": """
def send_telegram_message(message: str) -> str:
    import requests
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": message})
    return "Message envoyé" if r.status_code == 200 else f"Erreur: {r.text}"
"""
    },
    {
        "name": "send_slack_message",
        "category": "productivity",
        "description": "Envoie un message dans Slack via webhook",
        "requires": ["requests"],
        "env_vars": ["SLACK_WEBHOOK_URL"],
        "parameters": {"message": "str"},
        "code": """
def send_slack_message(message: str) -> str:
    import requests
    r = requests.post(os.getenv("SLACK_WEBHOOK_URL"), json={"text": message})
    return f"Status: {r.status_code}"
"""
    },
    {
        "name": "create_google_calendar_event",
        "category": "productivity",
        "description": "Crée un événement Google Calendar",
        "requires": ["google-api-python-client", "google-auth-oauthlib"],
        "env_vars": ["GOOGLE_CREDENTIALS_PATH"],
        "parameters": {"title": "str", "start": "str", "end": "str", "description": "str = ''"},
        "code": """
def create_google_calendar_event(title: str, start: str, end: str, description: str = "") -> str:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    creds = Credentials.from_authorized_user_file(os.getenv("GOOGLE_CREDENTIALS_PATH"))
    service = build("calendar", "v3", credentials=creds)
    event = {"summary": title, "description": description,
             "start": {"dateTime": start, "timeZone": "Europe/Paris"},
             "end": {"dateTime": end, "timeZone": "Europe/Paris"}}
    service.events().insert(calendarId="primary", body=event).execute()
    return f"Événement créé : {title}"
"""
    },
    {
        "name": "create_notion_page",
        "category": "productivity",
        "description": "Crée une page dans Notion",
        "requires": ["requests"],
        "env_vars": ["NOTION_API_KEY", "NOTION_DATABASE_ID"],
        "parameters": {"title": "str", "content": "str"},
        "code": """
def create_notion_page(title: str, content: str) -> str:
    import requests
    headers = {"Authorization": f"Bearer {os.getenv('NOTION_API_KEY')}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}
    data = {"parent": {"database_id": os.getenv("NOTION_DATABASE_ID")},
            "properties": {"title": {"title": [{"text": {"content": title}}]}},
            "children": [{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}}]}
    r = requests.post("https://api.notion.com/v1/pages", json=data, headers=headers)
    return f"Page créée (status {r.status_code})"
"""
    },
    {
        "name": "add_trello_card",
        "category": "productivity",
        "description": "Ajoute une carte dans un tableau Trello",
        "requires": ["requests"],
        "env_vars": ["TRELLO_API_KEY", "TRELLO_TOKEN"],
        "parameters": {"list_id": "str", "name": "str", "description": "str = ''"},
        "code": """
def add_trello_card(list_id: str, name: str, description: str = "") -> str:
    import requests
    r = requests.post("https://api.trello.com/1/cards", params={
        "idList": list_id, "name": name, "desc": description,
        "key": os.getenv("TRELLO_API_KEY"), "token": os.getenv("TRELLO_TOKEN")
    })
    return f"Carte créée (status {r.status_code})"
"""
    },
    {
        "name": "create_github_issue",
        "category": "productivity",
        "description": "Crée une issue GitHub",
        "requires": ["requests"],
        "env_vars": ["GITHUB_TOKEN"],
        "parameters": {"repo": "str", "title": "str", "body": "str = ''"},
        "code": """
def create_github_issue(repo: str, title: str, body: str = "") -> str:
    import requests
    r = requests.post(f"https://api.github.com/repos/{repo}/issues",
        json={"title": title, "body": body},
        headers={"Authorization": f"token {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github.v3+json"})
    return f"Issue créée : {r.json().get('html_url', r.text)}"
"""
    },
    {
        "name": "get_github_repo_info",
        "category": "productivity",
        "description": "Retourne les informations d'un repo GitHub",
        "requires": ["requests"],
        "env_vars": [],
        "parameters": {"repo": "str"},
        "code": """
def get_github_repo_info(repo: str) -> dict:
    import requests
    r = requests.get(f"https://api.github.com/repos/{repo}").json()
    return {"name": r.get("name"), "stars": r.get("stargazers_count"), "forks": r.get("forks_count"), "description": r.get("description"), "language": r.get("language")}
"""
    },
    {
        "name": "summarize_text",
        "category": "productivity",
        "description": "Résume un texte long (utilise OpenAI)",
        "requires": ["openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"text": "str", "max_words": "int = 100"},
        "code": """
def summarize_text(text: str, max_words: int = 100) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = client.chat.completions.create(model="gpt-4o-mini", messages=[
        {"role":"user","content":f"Résume ce texte en {max_words} mots max :\\n\\n{text}"}
    ])
    return r.choices[0].message.content
"""
    },
    {
        "name": "set_timer",
        "category": "productivity",
        "description": "Lance un timer et envoie une notification quand il expire",
        "requires": ["plyer"],
        "env_vars": [],
        "parameters": {"seconds": "int", "label": "str = 'Timer'"},
        "code": """
def set_timer(seconds: int, label: str = "Timer") -> str:
    import threading
    from plyer import notification
    def _notify():
        import time
        time.sleep(seconds)
        notification.notify(title="⏰ Timer", message=f"{label} — {seconds}s écoulées", timeout=10)
    t = threading.Thread(target=_notify, daemon=True)
    t.start()
    return f"Timer de {seconds}s lancé : {label}"
"""
    },
    {
        "name": "get_current_time",
        "category": "productivity",
        "description": "Retourne l'heure et la date actuelle",
        "requires": [],
        "env_vars": [],
        "parameters": {"timezone": "str = 'Europe/Paris'"},
        "code": """
def get_current_time(timezone: str = "Europe/Paris") -> str:
    try:
        import datetime
        from zoneinfo import ZoneInfo
        now = datetime.datetime.now(ZoneInfo(timezone))
        return now.strftime("%A %d %B %Y, %H:%M:%S")
    except:
        import datetime
        return str(datetime.datetime.now())
"""
    },
]

# ══════════════════════════════════════════════════════════════════
# 🎵  CATÉGORIE 6 : MÉDIA & AUDIO
# ══════════════════════════════════════════════════════════════════

MEDIA_SKILLS = [
    {
        "name": "text_to_speech",
        "category": "media",
        "description": "Convertit du texte en fichier audio MP3 (gTTS, gratuit)",
        "requires": ["gtts", "playsound"],
        "env_vars": [],
        "parameters": {"text": "str", "lang": "str = 'fr'", "output": "str = 'output.mp3'"},
        "code": """
def text_to_speech(text: str, lang: str = "fr", output: str = "output.mp3") -> str:
    from gtts import gTTS
    tts = gTTS(text=text, lang=lang)
    tts.save(output)
    return f"Audio généré : {output}"
"""
    },
    {
        "name": "text_to_speech_openai",
        "category": "media",
        "description": "TTS haute qualité via OpenAI (voix nova, alloy, echo...)",
        "requires": ["openai"],
        "env_vars": ["OPENAI_API_KEY"],
        "parameters": {"text": "str", "voice": "str = 'nova'", "output": "str = 'speech.mp3'"},
        "code": """
def text_to_speech_openai(text: str, voice: str = "nova", output: str = "speech.mp3") -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = client.audio.speech.create(model="tts-1", voice=voice, input=text)
    r.stream_to_file(output)
    return f"Audio OpenAI : {output}"
"""
    },
    {
        "name": "play_audio",
        "category": "media",
        "description": "Joue un fichier audio",
        "requires": ["pygame"],
        "env_vars": [],
        "parameters": {"path": "str"},
        "code": """
def play_audio(path: str) -> str:
    import pygame, time
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    return f"Audio joué : {path}"
"""
    },
    {
        "name": "record_audio",
        "category": "media",
        "description": "Enregistre l'audio du microphone",
        "requires": ["sounddevice", "scipy"],
        "env_vars": [],
        "parameters": {"duration": "int = 5", "output": "str = 'recording.wav'", "sample_rate": "int = 44100"},
        "code": """
def record_audio(duration: int = 5, output: str = "recording.wav", sample_rate: int = 44100) -> str:
    import sounddevice as sd
    from scipy.io.wavfile import write
    print(f"Enregistrement pendant {duration}s...")
    data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    write(output, sample_rate, data)
    return f"Audio enregistré : {output}"
"""
    },
    {
        "name": "download_youtube_audio",
        "category": "media",
        "description": "Télécharge l'audio d'une vidéo YouTube en MP3",
        "requires": ["yt-dlp"],
        "env_vars": [],
        "parameters": {"url": "str", "output_folder": "str = '.'"},
        "code": """
def download_youtube_audio(url: str, output_folder: str = ".") -> str:
    import yt_dlp
    opts = {"format": "bestaudio/best", "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]}
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    return f"Audio téléchargé dans {output_folder}"
"""
    },
    {
        "name": "download_youtube_video",
        "category": "media",
        "description": "Télécharge une vidéo YouTube",
        "requires": ["yt-dlp"],
        "env_vars": [],
        "parameters": {"url": "str", "output_folder": "str = '.'", "quality": "str = 'best'"},
        "code": """
def download_youtube_video(url: str, output_folder: str = ".", quality: str = "best") -> str:
    import yt_dlp
    opts = {"format": quality, "outtmpl": f"{output_folder}/%(title)s.%(ext)s"}
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    return f"Vidéo téléchargée dans {output_folder}"
"""
    },
    {
        "name": "get_youtube_info",
        "category": "media",
        "description": "Retourne les infos d'une vidéo YouTube (titre, durée, vues...)",
        "requires": ["yt-dlp"],
        "env_vars": [],
        "parameters": {"url": "str"},
        "code": """
def get_youtube_info(url: str) -> dict:
    import yt_dlp
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)
    return {"title": info.get("title"), "duration": info.get("duration"), "views": info.get("view_count"), "channel": info.get("channel"), "description": (info.get("description") or "")[:500]}
"""
    },
    {
        "name": "play_spotify",
        "category": "media",
        "description": "Contrôle Spotify (play, pause, next) via l'API Spotipy",
        "requires": ["spotipy"],
        "env_vars": ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "SPOTIFY_REDIRECT_URI"],
        "parameters": {"action": "str = 'pause'"},
        "code": """
def play_spotify(action: str = "pause") -> str:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-modify-playback-state"
    ))
    if action == "play": sp.start_playback()
    elif action == "pause": sp.pause_playback()
    elif action == "next": sp.next_track()
    elif action == "previous": sp.previous_track()
    return f"Spotify: {action}"
"""
    },
    {
        "name": "get_spotify_current_track",
        "category": "media",
        "description": "Retourne la chanson en cours sur Spotify",
        "requires": ["spotipy"],
        "env_vars": ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "SPOTIFY_REDIRECT_URI"],
        "code": """
def get_spotify_current_track() -> dict:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-read-currently-playing"
    ))
    t = sp.current_user_playing_track()
    if not t: return {"playing": False}
    return {"title": t["item"]["name"], "artist": t["item"]["artists"][0]["name"], "playing": t["is_playing"]}
"""
    },
    {
        "name": "generate_qr_code",
        "category": "media",
        "description": "Génère un QR code et le sauvegarde en image",
        "requires": ["qrcode", "pillow"],
        "env_vars": [],
        "parameters": {"data": "str", "output": "str = 'qrcode.png'"},
        "code": """
def generate_qr_code(data: str, output: str = "qrcode.png") -> str:
    import qrcode
    img = qrcode.make(data)
    img.save(output)
    return f"QR code sauvegardé : {output}"
"""
    },
]

# ══════════════════════════════════════════════════════════════════
# 🏠  CATÉGORIE 7 : DOMOTIQUE & IOT
# ══════════════════════════════════════════════════════════════════

SMART_HOME_SKILLS = [
    {
        "name": "ha_get_states",
        "category": "smarthome",
        "description": "Récupère les états de tous les appareils Home Assistant",
        "requires": ["requests"],
        "env_vars": ["HA_URL", "HA_TOKEN"],
        "code": """
def ha_get_states() -> list:
    import requests
    r = requests.get(f"{os.getenv('HA_URL')}/api/states",
        headers={"Authorization": f"Bearer {os.getenv('HA_TOKEN')}"})
    return r.json()
"""
    },
    {
        "name": "ha_turn_on",
        "category": "smarthome",
        "description": "Allume un appareil Home Assistant (lumière, switch...)",
        "requires": ["requests"],
        "env_vars": ["HA_URL", "HA_TOKEN"],
        "parameters": {"entity_id": "str"},
        "code": """
def ha_turn_on(entity_id: str) -> str:
    import requests
    domain = entity_id.split(".")[0]
    r = requests.post(f"{os.getenv('HA_URL')}/api/services/{domain}/turn_on",
        headers={"Authorization": f"Bearer {os.getenv('HA_TOKEN')}"},
        json={"entity_id": entity_id})
    return f"Allumé : {entity_id} (status {r.status_code})"
"""
    },
    {
        "name": "ha_turn_off",
        "category": "smarthome",
        "description": "Éteint un appareil Home Assistant",
        "requires": ["requests"],
        "env_vars": ["HA_URL", "HA_TOKEN"],
        "parameters": {"entity_id": "str"},
        "code": """
def ha_turn_off(entity_id: str) -> str:
    import requests
    domain = entity_id.split(".")[0]
    r = requests.post(f"{os.getenv('HA_URL')}/api/services/{domain}/turn_off",
        headers={"Authorization": f"Bearer {os.getenv('HA_TOKEN')}"},
        json={"entity_id": entity_id})
    return f"Éteint : {entity_id} (status {r.status_code})"
"""
    },
    {
        "name": "ha_set_light_color",
        "category": "smarthome",
        "description": "Change la couleur d'une lumière Home Assistant",
        "requires": ["requests"],
        "env_vars": ["HA_URL", "HA_TOKEN"],
        "parameters": {"entity_id": "str", "rgb": "list", "brightness": "int = 255"},
        "code": """def ha_set_light_color(entity_id: str, rgb: list, brightness: int = 255) -> str:
    import requests, os
    domain = entity_id.split(".")[0]
    r = requests.post(f"{os.getenv('HA_URL')}/api/services/{domain}/turn_on",
        headers={"Authorization": f"Bearer {os.getenv('HA_TOKEN')}"},
        json={"entity_id": entity_id, "rgb_color": rgb, "brightness": brightness})
    return f"Couleur changée : {entity_id} (status {r.status_code})"
"""
    }
]


SECURITY_SKILLS = [
    {
        "name": "generate_password",
        "category": "security",
        "description": "Génère un mot de passe sécurisé",
        "requires": [],
        "env_vars": [],
        "parameters": {"length": "int = 16"},
        "code": """def generate_password(length: int = 16) -> str:
    import secrets, string
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))
"""
    }
]

DATA_SKILLS = [
    {
        "name": "parse_json",
        "category": "data",
        "description": "Parse un string JSON",
        "requires": [],
        "env_vars": [],
        "parameters": {"json_str": "str"},
        "code": """def parse_json(json_str: str) -> dict:
    import json
    return json.loads(json_str)
"""
    }
]

MISC_SKILLS = [
    {
        "name": "echo",
        "category": "misc",
        "description": "Echo le texte",
        "requires": [],
        "env_vars": [],
        "parameters": {"text": "str"},
        "code": """def echo(text: str) -> str:
    return text
"""
    }
]

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
    return "\n".join(results)
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
    content = f"FROM python:{python_version}-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nCMD [\"python\", \"{app_file}\"]\n"
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
    prompt = f"Convertis ce code {from_lang} en {to_lang}. Retourne uniquement le code, sans explications.\n\n{code}"
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
    prompt = f"Explique ce code {language} en français, simplement :\n\n{code}"
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
    context = "\n\n---\n\n".join(docs)
    prompt = f"Réponds à la question en te basant uniquement sur ces documents :\n\n{context}\n\nQuestion: {question}"
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
