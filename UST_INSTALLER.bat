@echo off
:: ======================================
::   UST Smart Installer - Windows       
::   Double-click = installation complete
:: ======================================

title UST Smart Installer
chcp 65001 > nul 2>&1

:: -- Activer les couleurs ANSI ---------------------
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f > nul 2>&1

:: -- Chercher Python -------------------------------
set PYTHON_CMD=

:: Test python3 d'abord
python3 --version > nul 2>&1
if %errorlevel% == 0 (set PYTHON_CMD=python3 & goto :found_python)

:: Test python
python --version > nul 2>&1
if %errorlevel% == 0 (set PYTHON_CMD=python & goto :found_python)

:: Test py (launcher Windows)
py --version > nul 2>&1
if %errorlevel% == 0 (set PYTHON_CMD=py & goto :found_python)

:: -- Python non trouve -----------------------------
echo.
echo  [UST] Python n'est pas installe sur ce PC.
echo.
echo  Solution :
echo  1. Va sur https://python.org/downloads
echo  2. Telecharge Python 3.12
echo  3. COCHE "Add Python to PATH" lors de l'installation
echo  4. Relance ce fichier
echo.

:: Essayer d'ouvrir la page de téléchargement automatiquement
start https://python.org/downloads
pause
exit /b 1

:found_python
:: -- Verifier la version ---------------------------
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PY_VER=%%i
echo.
echo  Python detecte : %PY_VER%

:: -- Lancer l'installeur ---------------------------
%PYTHON_CMD% "%~dp0ust_installer.py"

:: -- Garder la fenetre ouverte si erreur ---------
if %errorlevel% neq 0 (
    echo.
    echo  [ERREUR] L'installeur s'est arrete.
    echo  Consulte ust_install.log pour les details.
    pause
)
