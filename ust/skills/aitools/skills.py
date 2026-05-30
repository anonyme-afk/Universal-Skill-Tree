"""
ust.skills.aitools
──────────────────
Branch: "aitools"
"""
from __future__ import annotations
import json
from ust.core.registry import skill

def _require(package: str):
    import importlib
    try:
        return importlib.import_module(package)
    except ImportError:
        raise ImportError(f"Package '{package}' required.")

@skill(
    name="search_awesome_ai_tools",
    branch="aitools",
    description="Search the awesome-ai-tools list for various AI tools (e.g., text, image, video, audio generation).",
    parameters={
        "properties": {
            "query": {"type": "string", "description": "Search keyword (e.g. 'video', 'image', 'code', 'audio')"}
        },
        "required": ["query"]
    }
)
def search_awesome_ai_tools(query: str) -> str:
    requests = _require("requests")
    url = "https://raw.githubusercontent.com/mahseema/awesome-ai-tools/main/README.md"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        return f"Failed to fetch awesome-ai-tools list: {e}"

    lines = content.splitlines()
    results = []
    
    query_lower = query.lower()
    for i, line in enumerate(lines):
        if line.startswith("- [") and query_lower in line.lower():
            result = line.strip()
            if i + 1 < len(lines) and not lines[i+1].startswith("-"):
                result += " " + lines[i+1].strip()
            results.append(result)
            
            if len(results) >= 15:
                break

    if not results:
        return f"No AI tools found matching '{query}'."
    
    return "Found these AI tools:\n" + "\n".join(results)
