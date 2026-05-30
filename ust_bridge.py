"""
|==========================================|
|  UST Bridge - Auto-généré par l'installeur |
|  Universal Skill Tree × Ton projet        |
|==========================================|
"""
import os, sys
from pathlib import Path

# -------------------------------------------------- Activation du venv UST si présent ------------
_VENV = Path(__file__).parent / ".ust_venv"
if _VENV.exists():
    _site = _VENV / ("Lib/site-packages" if sys.platform == "win32"
                     else f"lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages")
    if str(_site) not in sys.path:
        sys.path.insert(0, str(_site))

# -------------------------------------------------- Chargement UST --------------------------------
_UST_LOADED = False
_UST_TOOLS  = []
_UST_BRANCHES = ['system', 'web', 'files']

try:
    from ust import enable_branch, USTAdapter
    from ust.core.registry import get_registered_tools

    for _b in _UST_BRANCHES:
        try:
            enable_branch(_b)
        except Exception as _e:
            pass  # branch optionnelle

    _UST_TOOLS  = get_registered_tools()
    _UST_LOADED = True
except ImportError:
    pass  # UST pas encore installé - silencieux

# -------------------------------------------------- Clé API auto-detectee -------------------------
def _find_key():
    for var in ["OPENROUTER_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"]:
        v = os.environ.get(var, "")
        if v: return v
    env_file = Path(__file__).parent / ".env.ust"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                if v.strip() not in ("", "METS-TA-CLE-ICI"):
                    os.environ[k.strip()] = v.strip()
                    return v.strip()
    return ""

# -------------------------------------------------- API Publique ----------------------------------

def get_ust_tools() -> list:
    """Retourne les tools UST au format OpenAI/OpenRouter."""
    return _UST_TOOLS

def get_ust_status() -> dict:
    return {{"loaded": _UST_LOADED, "tools": len(_UST_TOOLS), "branches": _UST_BRANCHES}}

def run_ust(prompt: str, history: list = None, model: str = "openai/gpt-4o-mini") -> str:
    """Envoie un prompt à l'agent UST et retourne la réponse."""
    if not _UST_LOADED:
        return "[UST non chargé - vérifie ust_install.log]"
    key = _find_key()
    agent = USTAdapter(api_key=key, model=model)
    return agent.chat_sync(prompt, history=history or [])

def ust_tools_for_api() -> list:
    """Alias propre pour injection dans un appel API."""
    return get_ust_tools()

# -------------------------------------------------- Auto-print au chargement ----------------------
if __name__ != "__main__":
    if _UST_LOADED:
        print(f"[UST] ✅ {{len(_UST_TOOLS)}} tools actifs - branches: {{', '.join(_UST_BRANCHES)}}")
    else:
        print("[UST] [!] Bridge chargé mais UST non installé")

if __name__ == "__main__":
    print(get_ust_status())
    if _UST_LOADED:
        print(run_ust("Quel est mon usage CPU ?"))
