"""
ust.skills.agent_skills
───────────────────────
Branch: "agent_skills"
"""
from __future__ import annotations
from ust.core.registry import skill

def _require(package: str):
    import importlib
    try:
        return importlib.import_module(package)
    except ImportError:
        raise ImportError(f"Package '{package}' required.")

@skill(
    name="search_awesome_agent_skills",
    branch="agent_skills",
    description="Search the awesome-agent-skills list for community-built agent skills.",
    parameters={
        "properties": {
            "query": {"type": "string", "description": "Search keyword (e.g. 'Stripe', 'Google', 'Database')"}
        },
        "required": ["query"]
    }
)
def search_awesome_agent_skills(query: str) -> str:
    requests = _require("requests")
    url = "https://raw.githubusercontent.com/VoltAgent/awesome-agent-skills/main/README.md"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        return f"Failed to fetch awesome-agent-skills list: {e}"

    lines = content.splitlines()
    results = []
    
    query_lower = query.lower()
    for i, line in enumerate(lines):
        if line.startswith("- [") and query_lower in line.lower() or query_lower in line.lower():
            if line.strip():
                results.append(line.strip())
            
            if len(results) >= 20:
                break

    if not results:
        return f"No agent skills found matching '{query}'."
    
    return "Found these Awesome Agent Skills:\n" + "\n".join(results)
