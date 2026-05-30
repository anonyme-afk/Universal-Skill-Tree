"""
Universal Skill Tree (UST)
──────────────────────────
Plug & Play skill framework for AI agents.

Quick start:
    from ust import enable_branch, USTAdapter

    enable_branch("system")
    agent = USTAdapter(api_key="sk-or-...", model="openai/gpt-4o-mini")
    reply = agent.chat_sync("Open Chrome and go to github.com")
    print(reply)

Or enable everything:
    from ust import enable_all, USTAdapter
    enable_all()
"""
from __future__ import annotations

from .core.registry import get_registry, SkillRegistry
from .core.executor import Executor
from .core.adapter  import USTAdapter
from .core.gemini_adapter import GeminiAdapter
from .core.litellm_adapter import LiteLLMAdapter
from .core.ollama_adapter import OllamaAdapter

# ─── Branch loader map ────────────────────────────────────────────────────────

_BRANCH_MODULES: dict[str, str] = {
    "api": "ust.skills.api.skills",
    "memory": "ust.skills.memory.skills",
    "dev": "ust.skills.dev.skills",
    "social": "ust.skills.social.skills",
    "cloud": "ust.skills.cloud.skills",
    "automation": "ust.skills.automation.skills",
    "misc": "ust.skills.misc.skills",
    "data": "ust.skills.data.skills",
    "security": "ust.skills.security.skills",
    "smarthome": "ust.skills.smarthome.skills",
    "productivity": "ust.skills.productivity.skills",
    "system": "ust.skills.system.skills",
    "files":  "ust.skills.files.skills",
    "web":    "ust.skills.web.skills",
    "media":  "ust.skills.media.skills",
    "apps":   "ust.skills.apps.skills",
    "vision": "ust.skills.vision.skills",
    "osint":  "ust.skills.osint.skills",
    "cyber":  "ust.skills.cyber.skills",
    "crypto": "ust.skills.crypto.skills",
    "ai":     "ust.skills.ai.skills",
    "browser":"ust.skills.browser.skills",
    "selfhosted":"ust.skills.selfhosted.skills",
    "aitools":"ust.skills.aitools.skills",
    "agent_skills":"ust.skills.agent_skills.skills",
    "mcp":"ust.skills.mcp.skills",
}

_loaded_branches: set[str] = set()


def enable_branch(branch: str) -> None:
    """
    Load and activate a skill branch.

    Args:
        branch: One of 'system', 'files', 'web', 'media', 'apps', 'vision'

    Example:
        enable_branch("system")   # Loads all PC control skills
        enable_branch("web")      # Loads web search + scraping skills
    """
    if branch in _loaded_branches:
        return  # Already loaded

    module_path = _BRANCH_MODULES.get(branch)
    if not module_path:
        available = ", ".join(_BRANCH_MODULES.keys())
        raise ValueError(f"Unknown branch '{branch}'. Available: {available}")

    import importlib
    try:
        importlib.import_module(module_path)
        _loaded_branches.add(branch)
        registry = get_registry()
        skill_count = len(registry.branch(branch))
        print(f"[UST] ✅ Branch '{branch}' loaded — {skill_count} skills active")
    except ImportError as e:
        print(f"[UST] ⚠️  Branch '{branch}' partially loaded (missing optional deps): {e}")
        _loaded_branches.add(branch)


def enable_all() -> None:
    """Load all available skill branches."""
    for branch in _BRANCH_MODULES:
        enable_branch(branch)


def status() -> None:
    """Print a summary of all loaded skills."""
    print(get_registry().summary())


# ─── Public API ───────────────────────────────────────────────────────────────

__all__ = [
    "enable_branch",
    "enable_all",
    "status",
    "USTAdapter",
    "GeminiAdapter",
    "LiteLLMAdapter",
    "OllamaAdapter",
    "get_registry",
    "Executor",
]

__version__ = "0.1.0"
