#!/bin/bash
# ======================================
#   UST Smart Installer - Linux         
#   Lancer = installation complete      
# ======================================

# Se placer dans le bon dossier
cd "$(dirname "$0")"

# -- Chercher Python -------------------------------
PYTHON=""

for cmd in python3.12 python3.11 python3.10 python3 python; do
    if command -v "$cmd" &>/dev/null; then
        # Check python version is >= 3.10
        VER=$($cmd -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)
        if [ ! -z "$VER" ]; then
            MAJOR=$(echo $VER | cut -d. -f1)
            MINOR=$(echo $VER | cut -d. -f2)
            if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
                PYTHON="$cmd"
                break
            fi
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo -e "\033[91m[ERREUR] Python 3.10+ est requis.\033[0m"
    echo "Veuillez l'installer via votre gestionnaire de paquets (ex: sudo apt install python3)"
    exit 1
fi

# -- Lancer l'installeur ---------------------------
$PYTHON ust_installer.py

read -p "  Appuie sur Entree pour fermer..."
