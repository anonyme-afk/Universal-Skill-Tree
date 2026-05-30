""" ust.skills.misc """
from __future__ import annotations
import os
import json
from ust.core.registry import skill

@skill(
    name="get_random_joke",
    branch="misc",
    description="Retourne une blague aléatoire (en anglais)",
    parameters={},
)
def get_random_joke() -> str:
    import requests
    r = requests.get("https://official-joke-api.appspot.com/random_joke").json()
    return f"{r['setup']} — {r['punchline']}"


@skill(
    name="get_random_quote",
    branch="misc",
    description="Retourne une citation aléatoire",
    parameters={},
)
def get_random_quote() -> dict:
    import requests
    r = requests.get("https://api.quotable.io/random").json()
    return {"quote": r.get("content"), "author": r.get("author")}


@skill(
    name="detect_language",
    branch="misc",
    description="Détecte la langue d'un texte",
    parameters={
    "properties": {
        "text": {
            "type": "string"
        }
    },
    "required": [
        "text"
    ]
},
)
def detect_language(text: str) -> str:
    from langdetect import detect
    return detect(text)


@skill(
    name="parse_date",
    branch="misc",
    description="Parse une date en texte naturel (ex: 'tomorrow', 'next Monday')",
    parameters={
    "properties": {
        "date_string": {
            "type": "string"
        }
    },
    "required": [
        "date_string"
    ]
},
)
def parse_date(date_string: str) -> str:
    import dateparser
    d = dateparser.parse(date_string)
    return str(d) if d else "Date non reconnue"


@skill(
    name="format_json",
    branch="misc",
    description="Formate et indente du JSON",
    parameters={
    "properties": {
        "data": {
            "type": "string"
        }
    },
    "required": [
        "data"
    ]
},
)
def format_json(data: str) -> str:
    import json
    return json.dumps(json.loads(data), indent=2, ensure_ascii=False)


@skill(
    name="run_python_code",
    branch="misc",
    description="Exécute du code Python dynamiquement et retourne le résultat",
    parameters={
    "properties": {
        "code": {
            "type": "string"
        }
    },
    "required": [
        "code"
    ]
},
)
def run_python_code(code: str) -> str:
    import io, sys
    output = io.StringIO()
    sys.stdout = output
    try:
        exec(code)
    except Exception as e:
        sys.stdout = sys.__stdout__
        return f"Erreur: {e}"
    sys.stdout = sys.__stdout__
    return output.getvalue()


@skill(
    name="send_sms_twilio",
    branch="misc",
    description="Envoie un SMS via Twilio",
    parameters={
    "properties": {
        "to": {
            "type": "string"
        },
        "message": {
            "type": "string"
        }
    },
    "required": [
        "to",
        "message"
    ]
},
)
def send_sms_twilio(to: str, message: str) -> str:
    from twilio.rest import Client
    client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
    msg = client.messages.create(body=message, from_=os.getenv("TWILIO_FROM"), to=to)
    return f"SMS envoyé : {msg.sid}"


@skill(
    name="whatsapp_send",
    branch="misc",
    description="Envoie un message WhatsApp via Twilio",
    parameters={
    "properties": {
        "to": {
            "type": "string"
        },
        "message": {
            "type": "string"
        }
    },
    "required": [
        "to",
        "message"
    ]
},
)
def whatsapp_send(to: str, message: str) -> str:
    from twilio.rest import Client
    client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
    msg = client.messages.create(body=message,
        from_=f"whatsapp:{os.getenv('TWILIO_WHATSAPP_FROM')}",
        to=f"whatsapp:{to}")
    return f"WhatsApp envoyé : {msg.sid}"


@skill(
    name="control_mouse",
    branch="misc",
    description="Contrôle la souris (déplace, clique)",
    parameters={
    "properties": {
        "action": {
            "type": "string"
        },
        "x": {
            "type": "integer"
        },
        "y": {
            "type": "integer"
        }
    }
},
)
def control_mouse(action: str = "move", x: int = 0, y: int = 0) -> str:
    import pyautogui
    if action == "move": pyautogui.moveTo(x, y)
    elif action == "click": pyautogui.click(x, y)
    elif action == "double_click": pyautogui.doubleClick(x, y)
    elif action == "right_click": pyautogui.rightClick(x, y)
    return f"Souris: {action} ({x},{y})"


@skill(
    name="type_text",
    branch="misc",
    description="Tape du texte au clavier automatiquement",
    parameters={
    "properties": {
        "text": {
            "type": "string"
        },
        "interval": {
            "type": "number"
        }
    },
    "required": [
        "text"
    ]
},
)
def type_text(text: str, interval: float = 0.05) -> str:
    import pyautogui
    pyautogui.typewrite(text, interval=interval)
    return f"Texte tapé : {text}"


