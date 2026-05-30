"""
ust.skills.osint
────────────────
Branch: "osint"
"""
from __future__ import annotations
import subprocess
from ust.core.registry import skill

def _require(package: str):
    import importlib
    try:
        return importlib.import_module(package)
    except ImportError:
        raise ImportError(f"Package '{package}' required.")

@skill(
    name="osint_sherlock",
    branch="osint",
    description="Hunt down social media accounts by username across social networks using Sherlock.",
    parameters={
        "properties": {
            "username": {"type": "string", "description": "The target username"}
        },
        "required": ["username"]
    }
)
def osint_sherlock(username: str) -> str:
    try:
        result = subprocess.run(["sherlock", username, "--timeout", "5", "--print-found"], capture_output=True, text=True)
        return result.stdout or "No accounts found."
    except Exception as e:
        return f"Error: {e}"

@skill(
    name="osint_network_scan",
    branch="osint",
    description="Basic OSINT network scan (whois, dns, geoip)",
    parameters={
        "properties": {
            "target": {"type": "string"},
            "action": {"type": "string", "enum": ["whois", "dns", "geoip"]}
        },
        "required": ["target", "action"]
    }
)
def osint_network_scan(target: str, action: str) -> str:
    if action == "whois":
        res = subprocess.run(["whois", target], capture_output=True, text=True)
        return res.stdout
    elif action == "dns":
        import socket
        return f"IP: {socket.gethostbyname(target)}"
    elif action == "geoip":
        g = _require("geocoder")
        req = g.ip(target)
        return f"City: {req.city}, Country: {req.country}"
    return "Unknown action"

@skill(
    name="osint_osintgram",
    branch="osint",
    description="Run Osintgram (Instagram OSINT tool) commands. (Requires Osintgram to be installed and cloned).",
    parameters={
        "properties": {
            "target_username": {"type": "string", "description": "The target Instagram username"},
            "command": {"type": "string", "description": "The command to run (e.g. info, followers, followings, photos, etc.)"}
        },
        "required": ["target_username", "command"]
    }
)
def osint_osintgram(target_username: str, command: str) -> str:
    try:
        # Assuming osintgram is a known setup on the system or wrapped by a script `osintgram`
        # Alternatively, docker-compose run osintgram <target> -c <command>
        result = subprocess.run(["python3", "main.py", target_username, "-c", command], capture_output=True, text=True, cwd="./Osintgram")
        if result.returncode != 0 and result.stderr:
             # Try Docker approach if python main.py fails
             res_docker = subprocess.run(["docker", "run", "--rm", "osintgram", target_username, "-c", command], capture_output=True, text=True)
             return res_docker.stdout or res_docker.stderr
        return result.stdout or "Command executed successfully (no output)."
    except Exception as e:
        return f"Error executing Osintgram: {e}"
