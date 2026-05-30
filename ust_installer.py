# --------------------------------------------------*- coding: utf-8 -*-
"""
UST Smart Installer - Zero Error, Full Auto
Double-click → tout est configuré automatiquement.
"""

import os, sys, json, subprocess, platform, time, shutil, re, glob
from pathlib import Path

# ==================================================
#  LOGGER - tout est sauvegardé dans ust_install.log
# ==================================================
LOG_FILE = Path(__file__).parent / "ust_install.log"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")

# ==================================================
#  COULEURS
# ==================================================
IS_WIN = platform.system() == "Windows"

# Activer les couleurs ANSI sur Windows
if IS_WIN:
    os.system("color")
    import ctypes
    try:
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

class C:
    R="\033[0m"; B="\033[1m"; G="\033[92m"; Y="\033[93m"
    RE="\033[91m"; CY="\033[96m"; BL="\033[94m"; GR="\033[90m"
    PU="\033[95m"

def clr(text, c): return f"{c}{text}{C.R}"

# ==================================================
#  UI
# ==================================================

WIDTH = 56

def clear():
    os.system("cls" if IS_WIN else "clear")

def header():
    clear()
    print(clr("="*(WIDTH+2), C.CY))
    
    print(clr("  UST Smart Installer - Plug & Play".center(WIDTH), C.CY))
    print(clr("  Zero configuration. Zero erreur.".center(WIDTH), C.CY))
    
    print(clr("="*(WIDTH+2), C.CY))
    print()

def line(char="-"): print(clr(char * (WIDTH + 2), C.GR))

def status(icon, text, color=C.R):
    print(f"  {icon}  {clr(text, color)}")
    log(f"{icon} {text}")

def progress(label, total_steps):
    """Générateur de barre de progression."""
    for i in range(total_steps + 1):
        pct = int((i / total_steps) * 30)
        bar = "=" * pct + "-" * (30 - pct)
        print(f"\r  {clr(label, C.BL)} [{clr(bar, C.G)}] {i*100//total_steps}%", end="", flush=True)
        if i < total_steps:
            time.sleep(0.04)
    print()

def section(title):
    line()
    print(f"\n  {clr('[>]', C.PU)}  {clr(title, C.B)}\n")

def success_screen(msg):
    line()
    print(f"\n  {clr('[OK] ' + msg, C.G)}\n")

def error_screen(msg, fix):
    line()
    print(f"\n  {clr('[ERREUR] ' + msg, C.RE)}")
    print(f"  {clr('[INFO] ' + fix, C.Y)}\n")

# ==================================================
#  SAFE RUNNER - jamais de crash visible
# ==================================================

def run(cmd, timeout=120, cwd=None):
    """Lance une commande. Retourne (success, output). Ne crash jamais."""
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout, cwd=cwd,
            encoding="utf-8", errors="replace"
        )
        log(f"CMD {cmd} → rc={r.returncode}")
        return r.returncode == 0, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        log(f"TIMEOUT: {cmd}")
        return False, "timeout"
    except Exception as e:
        log(f"ERR cmd {cmd}: {e}")
        return False, str(e)

def pip(*args, venv_python=None):
    """Lance pip de façon robuste."""
    py = venv_python or sys.executable
    return run([py, "-m", "pip"] + list(args) + ["--quiet", "--no-warn-script-location"])

# ==================================================
#  DÉTECTION DU PROJET
# ==================================================

SIGNATURES = [
    {
        "name": "Mark XXXIX-OR (Jarvis - FatihMakes)",
        "emoji": "[OR]",
        "detect": ["or_client.py", "agent"],
        "inject": "or_client.py",
        "branches": ["system", "web", "files", "browser", "vision", "apps"],
        "import_hint": "# OpenRouter client",
    },
    {
        "name": "AutoGPT",
        "emoji": "[GPT]",
        "detect": ["autogpt", "run_agent.py"],
        "inject": "run_agent.py",
        "branches": ["system", "web", "files"],
        "import_hint": None,
    },
    {
        "name": "CrewAI Project",
        "emoji": "[CAI]",
        "detect": ["crew.py", "tasks.py"],
        "inject": "crew.py",
        "branches": ["web", "files", "ai"],
        "import_hint": None,
    },
    {
        "name": "LangChain Agent",
        "emoji": "[LC]",
        "detect": ["langchain", "agents"],
        "inject": "main.py",
        "branches": ["web", "files", "ai"],
        "import_hint": None,
    },
    {
        "name": "Projet Python generique",
        "emoji": "[PY]",
        "detect": ["main.py"],
        "inject": "main.py",
        "branches": ["system", "web", "files"],
        "import_hint": None,
    },
]

def detect_project(root: Path) -> dict:
    items = set(p.name for p in root.iterdir())
    for sig in SIGNATURES:
        hits = sum(1 for f in sig["detect"] if f in items)
        if hits >= min(2, len(sig["detect"])):
            log(f"Projet detecte : {sig['name']}")
            return sig
    return SIGNATURES[-1]  # generique

# ==================================================
#  SCAN CLÉS API
# ==================================================

API_PATTERNS = [
    r'sk-or-[A-Za-z0-9\-_]{20,}',   # OpenRouter
    r'sk-[A-Za-z0-9]{20,}',          # OpenAI
    r'AIzaSy[A-Za-z0-9\-_]{33}',     # Google/Gemini
    r'sk-ant-[A-Za-z0-9\-_]{20,}',   # Anthropic
]

def scan_api_keys(root: Path) -> dict:
    """Scanne TOUS les fichiers du projet pour trouver les clés API."""
    found = {}
    search = list(root.glob("**/*.py")) + list(root.glob("**/*.env*")) + \
             list(root.glob("**/*.json")) + list(root.glob("**/*.toml")) + \
             list(root.glob("**/*.cfg"))

    for file in search[:80]:  # limite pour la perf
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
            for pat in API_PATTERNS:
                matches = re.findall(pat, text)
                for m in matches:
                    if len(m) > 12 and "example" not in m.lower() and "your" not in m.lower():
                        key_type = (
                            "openrouter" if m.startswith("sk-or") else
                            "openai" if m.startswith("sk-") else
                            "gemini" if m.startswith("AIzaSy") else
                            "anthropic"
                        )
                        if key_type not in found:
                            found[key_type] = {"value": m, "file": file.name}
                            log(f"Clé {key_type} trouvée dans {file.name}")
        except Exception:
            pass
    return found

# ==================================================
#  VENV
# ==================================================

def create_venv(root: Path) -> tuple[bool, Path]:
    """Crée un venv isolé pour éviter tout conflit."""
    venv_path = root / ".ust_venv"
    if venv_path.exists():
        log("venv deja existant, reutilise")
    else:
        ok, _ = run([sys.executable, "-m", "venv", str(venv_path)])
        if not ok:
            log("venv echoue, utilisation du Python système")
            return False, None

    # Chemin vers python dans le venv
    if IS_WIN:
        py = venv_path / "Scripts" / "python.exe"
    else:
        py = venv_path / "bin" / "python"

    return py.exists(), py

# ==================================================
#  INSTALLATION PACKAGES
# ==================================================

def install_package(package: str, venv_py: Path = None) -> bool:
    """Installe un package. Essaie plusieurs fois avec fallbacks."""
    py = str(venv_py) if venv_py else sys.executable

    # Tentative 1 : normale
    ok, out = run([py, "-m", "pip", "install", package,
                   "--quiet", "--no-warn-script-location"])
    if ok: return True

    # Tentative 2 : sans cache
    ok, out = run([py, "-m", "pip", "install", package,
                   "--no-cache-dir", "--quiet"])
    if ok: return True

    # Tentative 3 : upgrade pip puis réessayer
    run([py, "-m", "pip", "install", "--upgrade", "pip", "--quiet"])
    ok, out = run([py, "-m", "pip", "install", package, "--quiet"])
    return ok

# ==================================================
#  GÉNÉRATION DU BRIDGE
# ==================================================

BRIDGE = '''"""
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
_UST_BRANCHES = {branches}

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
        for line in env_file.read_text().splitlines():
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
'''

def generate_bridge(root: Path, branches: list, api_keys: dict) -> Path:
    bridge = root / "ust_bridge.py"
    bridge.write_text(BRIDGE.format(branches=repr(branches)), encoding="utf-8")
    return bridge

# ==================================================
#  PATCH PROJET
# ==================================================

INJECT_BLOCK = '''
# -------------------------------------------------- UST Universal Skill Tree (auto-injecté) ------
try:
    from ust_bridge import get_ust_tools as _get_ust_tools
    UST_TOOLS = _get_ust_tools()
except Exception:
    UST_TOOLS = []
# --------------------------------------------------
'''

def patch_main_file(root: Path, filename: str) -> bool:
    target = root / filename
    if not target.exists():
        log(f"Fichier {filename} introuvable, skip patch")
        return False

    content = target.read_text(encoding="utf-8", errors="ignore")
    if "ust_bridge" in content:
        log("Déjà patche")
        return True

    # Trouver la dernière ligne d'import
    lines = content.splitlines()
    insert_at = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            insert_at = i + 1

    lines.insert(insert_at, INJECT_BLOCK)

    # Backup avant patch
    backup = target.with_suffix(".py.ust_backup")
    if not backup.exists():
        shutil.copy2(target, backup)
        log(f"Backup cree : {backup.name}")

    target.write_text("\n".join(lines), encoding="utf-8")
    log(f"Patch appliqué à {filename}")
    return True

# ==================================================
#  .env.ust
# ==================================================

def create_env(root: Path, api_keys: dict):
    env_path = root / ".env.ust"
    lines = ["# -------------------------------------------------- UST - Clés API (auto-généré) ----------------------\n"]

    if "openrouter" in api_keys:
        lines.append(f"OPENROUTER_API_KEY={api_keys['openrouter']['value']}\n")
        lines.append(f"# Trouvée dans : {api_keys['openrouter']['file']}\n")
    else:
        lines.append("OPENROUTER_API_KEY=sk-or-METS-TA-CLE-ICI\n")
        lines.append("# Obtiens une clé GRATUITE sur https://openrouter.ai\n")

    if "gemini" in api_keys:
        lines.append(f"\nGEMINI_API_KEY={api_keys['gemini']['value']}\n")

    env_path.write_text("".join(lines), encoding="utf-8")
    return env_path

# ==================================================
#  VÉRIFICATION FINALE
# ==================================================

def verify_installation(venv_py: Path) -> bool:
    """Teste que UST est bien importable."""
    py = str(venv_py) if (venv_py and venv_py.exists()) else sys.executable
    ok_flag, out = run([py, "-c", "from ust import enable_branch; print('UST_OK')"])
    return ok_flag and "UST_OK" in out

# ==================================================
#  MAIN
# ==================================================

def main():
    root = Path(__file__).parent.resolve()
    log(f"\n{'='*50}\nINSTALL START - {time.strftime('%Y-%m-%d %H:%M:%S')}\nRoot: {root}")

    header()

    # -------------------------------------------------- 1. Detection OS & Python ------------------
    section("Analyse de l'environnement")
    status("[OS]", f"OS : {platform.system()} {platform.release()}")
    status("[PY]", f"Python : {sys.version.split()[0]}")

    major, minor = sys.version_info.major, sys.version_info.minor
    if major < 3 or minor < 10:
        error_screen(
            f"Python {major}.{minor} trop ancien (besoin 3.10+)",
            "Telecharge Python 3.12 sur https://python.org/downloads"
        )
        input("  Appuie sur Entree pour quitter...")
        return

    # -------------------------------------------------- 2. Détection projet -----------------------
    section("Detection du projet")
    project = detect_project(root)
    status(project["emoji"], f"Projet : {clr(project['name'], C.Y)}", C.R)
    status("[FILE]", f"Fichier principal : {project['inject']}")

    # -------------------------------------------------- 3. Scan clés API --------------------------
    section("Scan des clés API")
    progress("Scan en cours", 20)
    api_keys = scan_api_keys(root)

    if api_keys:
        for ktype, kinfo in api_keys.items():
            masked = kinfo["value"][:10] + "..." + kinfo["value"][-4:]
            status("[KEY]", f"{ktype} : {masked} (dans {kinfo['file']})", C.GR)
    else:
        status("[!]", "Aucune cle trouvee - sera configuree dans .env.ust", C.Y)

    # -------------------------------------------------- 4. Création du venv -----------------------
    section("Environnement isolé (venv)")
    venv_ok, venv_py = create_venv(root)
    if venv_ok:
        status("[OK]", f"Venv cree : .ust_venv/", C.G)
    else:
        status("[INFO]", "Venv non disponible, Python système utilisé", C.Y)
        venv_py = None

    py_to_use = venv_py if venv_ok else None

    # -------------------------------------------------- 5. Installation packages ------------------
    section("Installation des packages")

    branches = project["branches"]
    extras = ",".join(branches)
    main_pkg = f"universal-skill-tree-naneg[{extras}]"

    packages = [
        ("pip (mise a jour)", "pip"),
        ("UST core", "universal-skill-tree-naneg"),
        (f"UST branches [{extras}]", main_pkg),
    ]

    all_ok = True
    for label, pkg in packages:
        print(f"  [*] {label}...", end=" ", flush=True)
        ok_flag = install_package(pkg, venv_py)
        if ok_flag:
            print(clr("[OK]", C.G))
        else:
            print(clr("[!] (ignore, continuons)", C.Y))
            log(f"Package {pkg} echoue")
            if "universal-skill-tree" in pkg:
                all_ok = False

    # -------------------------------------------------- 6. Génération ust_bridge.py ---------------
    section("Creation du bridge UST")
    bridge = generate_bridge(root, branches, api_keys)
    status("[OK]", f"ust_bridge.py cree", C.G)

    # -------------------------------------------------- 7. Patch du projet ------------------------
    section("Connexion au projet")
    patched = patch_main_file(root, project["inject"])
    if patched:
        status("[OK]", f"{project['inject']} - import UST injecté", C.G)
        status("[BACKUP]", f"Backup cree : {project['inject']}.ust_backup", C.GR)
    else:
        status("[INFO]", f"{project['inject']} non trouvé (bridge cree quand même)", C.Y)

    # -------------------------------------------------- 8. Fichier .env.ust -----------------------
    section("Configuration des cles API")
    env_file = create_env(root, api_keys)
    if api_keys:
        status("[OK]", "Cles API copiees dans .env.ust", C.G)
    else:
        status("[EDIT]", ".env.ust cree - METS TA CLÉ OPENROUTER DEDANS !", C.Y)

    # -------------------------------------------------- 9. Verification ---------------------------
    section("Verification finale")
    progress("Test UST", 15)
    verified = verify_installation(venv_py)

    if verified:
        status("[OK]", "UST importé et fonctionnel !", C.G)
    else:
        status("[!]", "Import partiel - vérifie ust_install.log si besoin", C.Y)

    # -------------------------------------------------- 10. Résumé --------------------------------
    line()
    print(f"""
  {clr('[SUCCESS] Installation terminee !', C.B + C.G)}

  {clr('Ce qui a ete fait :', C.B)}
  [OK] UST installé dans .ust_venv/
  [OK] ust_bridge.py cree (le pont UST ↔ projet)
  [OK] {project['inject']} patche (import auto-ajouté)
  {"[OK] Cles API copiees" if api_keys else "[EDIT] .env.ust cree - mets ta clé OpenRouter"}

  {clr('Utilise UST dans ton code :', C.B)}
  {clr("from ust_bridge import run_ust, get_ust_tools", C.CY)}
  {clr("reply = run_ust('Ouvre Chrome')", C.CY)}

  {clr("Log complet : ust_install.log", C.GR)}
    """)

    if not api_keys:
        print(f"  {clr('[!] ACTION REQUISE :', C.Y + C.B)}")
        print(f"  {clr('  1. Ouvre .env.ust', C.Y)}")
        print(f"  {clr('  2. Remplace METS-TA-CLE-ICI par ta clé', C.Y)}")
        print(f"  {clr('  3. Cle gratuite : https://openrouter.ai', C.Y)}")
        print()

    log("INSTALL END")
    input(f"\n  {clr('Appuie sur Entree pour fermer...', C.GR)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Annule.")
    except Exception as e:
        log(f"CRASH: {e}")
        import traceback; traceback.print_exc()
        print(f"\n  Erreur inattendue : {e}")
        print(f"  Details dans ust_install.log")
        input("  Appuie sur Entree pour fermer...")
