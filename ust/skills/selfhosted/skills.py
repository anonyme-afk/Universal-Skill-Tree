"""
ust.skills.selfhosted
─────────────────────
Branch: "selfhosted"
"""
from __future__ import annotations
import subprocess
import json
from ust.core.registry import skill

def _require(package: str):
    import importlib
    try:
        return importlib.import_module(package)
    except ImportError:
        raise ImportError(f"Package '{package}' required.")

@skill(
    name="search_awesome_selfhosted",
    branch="selfhosted",
    description="Search the awesome-selfhosted list for open-source self-hosted alternatives to popular SaaS software.",
    parameters={
        "properties": {
            "query": {"type": "string", "description": "Search keyword (e.g. 'Google Drive', 'Notes', 'Dashboard', 'Password Manager')"}
        },
        "required": ["query"]
    }
)
def search_awesome_selfhosted(query: str) -> str:
    requests = _require("requests")
    # Fetch the awesome-selfhosted README
    url = "https://raw.githubusercontent.com/awesome-selfhosted/awesome-selfhosted/master/README.md"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        return f"Failed to fetch awesome-selfhosted list: {e}"

    lines = content.splitlines()
    results = []
    
    # Simple line-by-line fuzzy search for the query
    query_lower = query.lower()
    for i, line in enumerate(lines):
        if line.startswith("- [") and query_lower in line.lower():
            # Grab the item line, and maybe the next line if it continues the description
            result = line.strip()
            if i + 1 < len(lines) and not lines[i+1].startswith("-"):
                result += " " + lines[i+1].strip()
            results.append(result)
            
            if len(results) >= 15: # Cap to 15 results to not overload the context
                break

    if not results:
        return f"No self-hosted applications found matching '{query}'."
    
    return "Found these self-hosted alternatives:\n" + "\n".join(results)

@skill(
    name="docker_ps",
    branch="selfhosted",
    description="List currently active docker containers.",
    parameters={"properties": {}}
)
def docker_ps() -> str:
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return f"Error running docker ps: {result.stderr}"
        if not result.stdout.strip():
            return "No docker containers are currently running."
        return result.stdout.strip()
    except FileNotFoundError:
        return "Docker is not installed or not in PATH."
    except Exception as e:
        return f"Docker ps failed: {e}"

@skill(
    name="docker_deploy_simple",
    branch="selfhosted",
    description="Deploy a simple docker container (e.g. for a self-hosted app).",
    parameters={
        "properties": {
            "image": {"type": "string", "description": "Docker image to run (e.g. 'nginx:latest', 'lscr.io/linuxserver/jellyfin')"},
            "name": {"type": "string", "description": "Name for the container"},
            "port_mapping": {"type": "string", "description": "Port mapping (e.g. '8080:80', '3000:3000'). Leave empty for none"},
        },
        "required": ["image", "name"]
    }
)
def docker_deploy_simple(image: str, name: str, port_mapping: str = "") -> str:
    try:
        cmd = ["docker", "run", "-d", "--name", name]
        if port_mapping:
            cmd.extend(["-p", port_mapping])
        cmd.append(image)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return f"Failed to deploy container {name}: {result.stderr}"
        
        return f"Successfully deployed container '{name}' from image '{image}'. Container ID: {result.stdout.strip()}"
    except FileNotFoundError:
        return "Docker is not installed or not in PATH."
    except Exception as e:
        return f"Deployment failed: {e}"
