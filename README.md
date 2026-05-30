# 🌳 Universal Skill Tree (UST)

![PyPI](https://img.shields.io/pypi/v/universal-skill-tree-naneg)
🔗 **Lien PyPI :** [universal-skill-tree-naneg sur PyPI](https://pypi.org/project/universal-skill-tree-naneg/)

**Le framework de skills Plug & Play pour connecter tout à votre agent IA en 3 lignes de code.**

---

#  Guide d'Intégration Complet : Connecter UST à votre IA (De A à Z)

Ce guide explique les étapes indispensables pour fusionner, de bout en bout, **Universal Skill Tree (UST)** avec votre projet d'IA existant (comme *Mark-XXXIX-OR*, AutoGPT, LangChain, etc.). 

Suivez ce manuel industriel, détaillé de fond en comble, pour un déploiement sans erreurs.

---

##  Étape 1 : Préparation et Récupération des Fichiers

Avant toute chose, vous devez avoir les fichiers sur votre ordinateur.

1. **Votre projet IA** : Assurez-vous d'avoir téléchargé et extrait le dossier contenant votre IA (qui comporte un fichier d'entrée comme `main.py` ou `app.py`).
2. **Le Universal Skill Tree** : Téléchargez et extrayez le dossier de `Universal-Skill-Tree`.

---

##  Étape 2 : Le Déplacement Manuel des Fichiers (Crucial)

Pour que votre IA puisse apprendre les compétences, les fichiers d'importation de UST doivent se trouver au même endroit que le cœur de votre IA. C'est l'erreur la plus commune (qui cause les plantages de type "File Not Found").

Ouvrez le dossier de **Universal-Skill-Tree**, copiez les fichiers suivants, et collez-les **directement à la racine du dossier de votre IA** :

* `skills_catalog.py` *(Contient la base de données brute des 200+ compétences)*
* `import_skills_catalog.py` *(Le moteur de compilation des compétences)*
* *Optionnel (Smart Installer)* : Vous pouvez aussi copier `UST_INSTALLER.bat`, `UST_INSTALLER.command`, `UST_INSTALLER.sh`, et `ust_installer.py` si vous souhaitez utiliser l'interface d'installation automatisée (qui repère les fichiers et s'occupe de tout).

>  **À quoi doit ressembler l'arborescence de votre dossier d'IA maintenant ?**
> À la racine de votre projet d'IA, vous devez voir cohabiter :
> - `main.py` (ou le cœur de votre IA)
> - `skills_catalog.py`
> - `import_skills_catalog.py`

---

##  Étape 3 : Installation et Compilation via le Terminal

Maintenant que les fichiers sont placés au bon endroit, vous devez installer le framework et générer l'architecture des compétences ("compiler" le catalogue) pour qu'elles soient comprises par votre programme.

1. **Ouvrez votre Terminal (Mac/Linux) ou Invite de commandes / PowerShell (Windows)**.
2. **Naviguez** dans le dossier exact de votre IA via la commande `cd chemin/vers/votre/dossier/ia`.

3. **Installez le cœur du framework (via PIP) :**
```bash
pip install --upgrade universal-skill-tree-naneg
```
*(Cela configure les fondations de l'outil et télécharge les dépendances requises globalement sur votre système).*

4. **Injectez et compilez le catalogue de compétences :**
Exécutez le script d'importation pour générer toute l'arborescence `ust/skills/...` en local :
```bash
python import_skills_catalog.py
```
*(Note : Sous Windows, utilisez la commande `python` ou `py`. Sous Mac/Linux, utilisez `python3`).*

---

##  Étape 4 : Connecter UST dans le Code de l'IA (Le "Câblage")

Pour que votre IA puisse utiliser ces super-pouvoirs de façon native, vous devez la relier via le bridge (le pont de connexion) dans son fichier de départ (ex: `main.py`).

1. **Ajouter la liaison (Tout en haut du fichier `main.py`) :**
Le bridge UST exporte deux fonctions essentielles. Exigez-les en haut de votre script :
```python
from ust_bridge import run_ust, get_ust_tools
```
*(Note : Si vous ne possédez pas de fichier `ust_bridge.py`, pas de panique, la bibliothèque pip possède les siens, ou vous pouvez exécuter un des installateurs (comme `UST_INSTALLER.bat`) pour le générer automatiquement).*

2. **Donner les outils (Tools) à votre IA :**
Dans la configuration du prompt, du client OpenAI, ou des paramètres de votre LLM, pointez vers la fonction qui liste les outils afin que l'IA connaisse ses nouvelles capacités.
```python
# Renseigne l'IA sur toutes les compétences de l'ordinateur
outils_ia = get_ust_tools()

# Lors de l'appel au modèle d'IA (exemple fictif type OpenAI) :
# response = client.chat.completions.create(
#     model="gpt-4o",
#     messages=historique,
#     tools=outils_ia
# )
```

3. **Intercepter et Exécuter les Actions :**
Dès que l'IA renvoie un "Tool Call" ou détecte qu'elle doit utiliser une compétence matérielle/logicielle (par exemple, "Je lance Spotify"), envoyez la requête directement à UST.
```python
# Laissez UST trouver, exécuter et vérifier le module appelé automatiquement :
reponse_outil = run_ust("L'ordre textuel de l'IA ici ou la requête structurée")
print(reponse_outil)
```

---

##  Étape 5 : Configuration des Clés API et Sécurité

Avoir les compétences c'est bien, avoir les droits d'accès c'est indispensable. UST utilise un standard industriel de gestion sécurisée via variables d'environnement.

Lors de l'installation, un fichier d'environnement masqué a été créé.

1. Cherchez un fichier nommé `.env.ust` (ou simplement `.env`) à la racine de votre dossier d'IA. S'il n'existe pas, créez-le.
2. Ouvrez ce fichier avec un éditeur de texte classique (Bloc-notes, VS Code, etc.).
3. Renseignez-y vos clés secrètes en remplaçant la valeur par défaut (`METS-TA-CLE-ICI`). Par exemple :

```env
# Clé requise pour le LLM principal (Gratuite sur https://openrouter.ai)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxx

# Pour la compétence Météo
OPENWEATHERMAP_API_KEY=TaCleIci

# Pour les compétences Spotify
SPOTIPY_CLIENT_ID=TonID
SPOTIPY_CLIENT_SECRET=TonSecret
SPOTIPY_REDIRECT_URI=http://localhost:8080

# etc.
```

** RÈGLES DE SÉCURITÉ INDUSTRIELLES :**
- Ne partagez **jamais** votre fichier `.env.ust`.
- Si vous utilisez Git ou GitHub, assurez-vous d'avoir ajouté `.env.ust` et `.env` dans votre fichier `.gitignore` afin de ne jamais divulguer vos identifiants publiquement sur internet.

---

##  Architecture Finale Attendue (Vérification)

Afin d'être sûr(e) d'avoir réussi l'intégration sans faille, vérifiez l'arborescence de votre projet. Après avoir exécuté les commandes, elle devrait ressembler très exactement à ceci :

```text
📁 Ton-Dossier-IA/
 ├── 📄 main.py (Ton programme IA modifié avec les 3 lignes de connexion)
 ├── 📄 skills_catalog.py (Le dictionnaire brut des compétences fourni)
 ├── 📄 import_skills_catalog.py (Le script compilateur fourni)
 ├── 📄 ust_bridge.py (Le pont de communication, généré automatiquement)
 ├── 📄 .env.ust (Fichier caché contenant tes mots de passe et clés API)
 └── 📁 ust/ (Dossier généré automatiquement)
      └── 📁 skills/ (Toutes les compétences compilées et classées prêt à l'emploi)
           ├── 📁 ai/
           ├── 📁 web/
           ├── 📁 productivity/
           └── ... (Les 200+ modules)
```

##  Vous êtes prêt(e) !
Votre agent d'intelligence artificielle est maintenant connecté au reste de votre ordinateur et du web, propulsé de manière propre et industrielle par l'architecture Plug & Play de **Universal Skill Tree**.