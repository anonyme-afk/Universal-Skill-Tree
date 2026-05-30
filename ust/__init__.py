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

# ─── Secrets Middleware ────────────────────────────────────────────────────────

from contextlib import contextmanager
import os

@contextmanager
def require_secrets(*var_names: str):
    """
    Context manager to ensure required environment variables are set.
    Looks for them in the environment or an optional .env.ust file.
    
    Example:
        with require_secrets("OPENAI_API_KEY", "SPOTIFY_CLIENT_ID"):
            agent.chat_sync(...)
    """
    try:
        import dotenv
        dotenv.load_dotenv(".env.ust")
    except ImportError:
        pass # python-dotenv not available, relying on pure os.environ
        
    missing = []
    for var in var_names:
        if not os.getenv(var):
            missing.append(var)
            
    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(f"UST_ConfigurationError: Missing environment variables: {missing_str}. Please set them in .env.ust or your environment.")
        
    yield

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

import logging

logger = logging.getLogger("ust")

def set_log_level(level: int):
    """Set the logging level for UST."""
    logger.setLevel(level)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[UST] %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

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

    import importlib.util
    try:
        if not importlib.util.find_spec(module_path):
            logger.warning(f"⚠️ Branch '{branch}' is not yet compiled. Please run `python import_skills_catalog.py`")
            return
        importlib.import_module(module_path)
        _loaded_branches.add(branch)
        registry = get_registry()
        skill_count = len(registry.branch(branch))
        logger.info(f"✅ Branch '{branch}' loaded — {skill_count} skills active")
    except ImportError as e:
        logger.warning(f"⚠️  Branch '{branch}' partially loaded (missing optional deps) or not compiled: {e}")
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
    "require_secrets"
]

try:
    import importlib.metadata
    __version__ = importlib.metadata.version("universal-skill-tree-naneg")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.2.0"
