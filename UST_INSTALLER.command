#!/bin/bash
# ======================================
#   UST Smart Installer - macOS         
#   Double-click = installation complete
# ======================================

# Se placer dans le bon dossier
cd "$(dirname "$0")"

# S'auto-rendre exécutable
chmod +x "$0"

# -- Chercher Python -------------------------------
PYTHON=""

for cmd in python3.12 python3.11 python3.10 python3 python; do
    if command -v "$cmd" &>/dev/null; then
        VER=$($cmd --version 2>&1 | grep -oP '\d+\.\d+')
        MAJOR=$(echo $VER | cut -d. -f1)
        MINOR=$(echo $VER | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    # Python non trouve - ouvrir la page de telechargement
    osascript -e 'display alert "Python 3.10+ requis" message "La page de telechargement va s'\''ouvrir dans votre navigateur." buttons {"OK"} default button "OK"'
    open "https://python.org/downloads"
    exit 1
fi

# -- Lancer l'installeur ---------------------------
$PYTHON ust_installer.py

# Garder le terminal ouvert
read -p "  Appuie sur Entree pour fermer..."
