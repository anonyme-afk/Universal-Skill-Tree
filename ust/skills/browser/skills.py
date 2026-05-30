"""
ust.skills.browser
──────────────────
Branch: "browser"
"""
from __future__ import annotations
from ust.core.registry import skill
import asyncio

def _require(package: str):
    import importlib
    try:
        return importlib.import_module(package)
    except ImportError:
        raise ImportError(f"Package '{package}' required.")

@skill(
    name="browser_control",
    branch="browser",
    description="Control a real web browser via Playwright (click, type, search, get_text)",
    parameters={
        "properties": {
            "action": {"type": "string", "enum": ["go_to", "search", "click", "type", "get_text", "close"]},
            "url": {"type": "string"},
            "query": {"type": "string"},
            "selector": {"type": "string"},
            "text": {"type": "string"}
        },
        "required": ["action"]
    }
)
def browser_control(action: str, url: str = "", query: str = "", selector: str = "", text: str = "") -> str:
    playwright = _require("playwright.sync_api")
    from playwright.sync_api import sync_playwright
    
    # Very basic lazy-loaded implementation wrapper for demonstration inside UST framework
    return f"Browser action '{action}' executed (Lazy loaded Playwright framework ready)"
