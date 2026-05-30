""" ust.skills.security """
from __future__ import annotations
import os
import json
from ust.core.registry import skill

@skill(
    name="generate_password",
    branch="security",
    description="Génère un mot de passe fort aléatoire",
    parameters={
    "properties": {
        "length": {
            "type": "integer"
        },
        "special_chars": {
            "type": "boolean"
        }
    }
},
)
def generate_password(length: int = 20, special_chars: bool = True) -> str:
    import random, string
    chars = string.ascii_letters + string.digits
    if special_chars:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return "".join(random.SystemRandom().choice(chars) for _ in range(length))


@skill(
    name="hash_text",
    branch="security",
    description="Hash un texte (SHA256, MD5, bcrypt...)",
    parameters={
    "properties": {
        "text": {
            "type": "string"
        },
        "algorithm": {
            "type": "string"
        }
    },
    "required": [
        "text"
    ]
},
)
def hash_text(text: str, algorithm: str = "sha256") -> str:
    import hashlib
    return hashlib.new(algorithm, text.encode()).hexdigest()


@skill(
    name="encrypt_file",
    branch="security",
    description="Chiffre un fichier avec une clé symétrique (Fernet)",
    parameters={
    "properties": {
        "path": {
            "type": "string"
        },
        "key": {
            "type": "string"
        }
    },
    "required": [
        "path"
    ]
},
)
def encrypt_file(path: str, key: str = None) -> dict:
    from cryptography.fernet import Fernet
    if not key:
        key = Fernet.generate_key().decode()
    f = Fernet(key.encode())
    with open(path, "rb") as fp:
        encrypted = f.encrypt(fp.read())
    with open(path + ".enc", "wb") as fp:
        fp.write(encrypted)
    return {"encrypted_path": path + ".enc", "key": key}


@skill(
    name="decrypt_file",
    branch="security",
    description="Déchiffre un fichier chiffré avec Fernet",
    parameters={
    "properties": {
        "path": {
            "type": "string"
        },
        "key": {
            "type": "string"
        },
        "output": {
            "type": "string"
        }
    },
    "required": [
        "path",
        "key",
        "output"
    ]
},
)
def decrypt_file(path: str, key: str, output: str) -> str:
    from cryptography.fernet import Fernet
    f = Fernet(key.encode())
    with open(path, "rb") as fp:
        data = f.decrypt(fp.read())
    with open(output, "wb") as fp:
        fp.write(data)
    return f"Fichier déchiffré : {output}"


@skill(
    name="scan_ports",
    branch="security",
    description="Scanne les ports ouverts d'un hôte",
    parameters={
    "properties": {
        "host": {
            "type": "string"
        },
        "ports": {
            "type": "array"
        }
    },
    "required": [
        "host"
    ]
},
)
def scan_ports(host: str, ports: list = [22,80,443,3306,8080]) -> dict:
    import socket
    results = {}
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        results[port] = s.connect_ex((host, port)) == 0
        s.close()
    return results


@skill(
    name="check_dns",
    branch="security",
    description="Résout un nom de domaine en adresse IP",
    parameters={
    "properties": {
        "domain": {
            "type": "string"
        }
    },
    "required": [
        "domain"
    ]
},
)
def check_dns(domain: str) -> list:
    import socket
    return list(set([r[4][0] for r in socket.getaddrinfo(domain, None)]))


@skill(
    name="generate_uuid",
    branch="security",
    description="Génère un UUID unique",
    parameters={},
)
def generate_uuid() -> str:
    import uuid
    return str(uuid.uuid4())


@skill(
    name="encode_base64",
    branch="security",
    description="Encode une chaîne en Base64",
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
def encode_base64(text: str) -> str:
    import base64
    return base64.b64encode(text.encode()).decode()


@skill(
    name="decode_base64",
    branch="security",
    description="Décode une chaîne Base64",
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
def decode_base64(text: str) -> str:
    import base64
    return base64.b64decode(text.encode()).decode()


