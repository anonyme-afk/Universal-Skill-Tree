# 🌳 Universal Skill Tree (UST)

![PyPI](https://img.shields.io/pypi/v/universal-skill-tree-naneg)
🔗 **Lien PyPI :** [universal-skill-tree-naneg sur PyPI](https://pypi.org/project/universal-skill-tree-naneg/)

**Le framework de compétences Plug & Play pour connecter n'importe quel LLM à votre PC et au web en 3 lignes de code.**

---

##  Guide d'Intégration Complet

Ce document présente l'intégralité du module **Universal Skill Tree (UST)**. Suivez ce manuel pour un déploiement sécurisé, performant et sans friction.

---

##  Étape 1 : Préparation et Placement des Fichiers

Pour intégrer les compétences à votre agent IA, assurez-vous de placer ces fichiers clés **à la racine de votre projet d'IA** (à côté de votre script principal comme `main.py`) :

*   `skills_catalog.py` *(Le catalogue brut contenant les signatures et configurations des compétences)*
*   `import_skills_catalog.py` *(Le moteur de compilation local responsable de générer l'arborescence des modules)*
*   `ust_installer.py` & Scripts `.bat` / `.sh` / `.command` *(L'installateur intelligent à un clic)*

### 📁 Structure Attendue de votre Projet d'IA :
```text
📁 Ton-Projet-IA/
 ├── 📄 main.py (Script de démarrage de ton IA)
 ├── 📄 skills_catalog.py (Fourni)
 ├── 📄 import_skills_catalog.py (Fourni)
 ├── 📄 ust_installer.py (Fourni)
 └── 📄 .env.ust (Fichier de configuration de tes clés)
```

---

##  Étape 2 : Installation & Compilation

Vous pouvez installer et configurer UST de deux manières : automatique ou manuelle.

### Option A : L'Installateur Intelligent (Recommandé)
Lancez simplement le script adapté à votre système depuis la racine de votre projet :
* **Windows** : Double-cliquez sur `UST_INSTALLER.bat`
* **Mac** : Exécutez `UST_INSTALLER.command`
* **Linux** : Exécutez `./UST_INSTALLER.sh`

L'installateur va automatiquement créer un environnement virtuel `.ust_venv`, y installer le paquet `universal-skill-tree-naneg`, compiler vos compétences, et générer un fichier de pont prêt à l'emploi nommé `ust_bridge.py`.

### Option B : Installation Manuelle (Ligne de Commande)
1. Installez le cœur du framework :
   ```bash
   pip install --upgrade universal-skill-tree-naneg
   ```
2. Compilez le catalogue d'importation de compétences au sein de votre environnement pour générer l'arborescence `ust/skills/` locale :
   ```bash
   python3 import_skills_catalog.py
   ```

---

##  Étape 3 : Chargement des Branches et API Publique

UST est construit de manière modulaire. Vous n'activez et n'installez que les compétences (les "branches") dont vous avez besoin pour garder votre application légère.

```python
from ust import enable_branch, enable_all, status, get_registry

# Charger uniquement les modules nécessaires
enable_branch("system")  # 15 compétences système actives (CPU, RAM, Processus, etc.)
enable_branch("web")     # 14 compétences web actives (Recherche, Scraping, etc.)
enable_branch("files")   # 14 compétences de gestion de fichiers actives (Lecture, Écriture, etc.)

# Ou activer absolument toutes les branches disponibles
# enable_all()

# Afficher un résumé des compétences prêtes à l'emploi
status()
```

---

## 🔌 Étape 4 : Connexion des LLM via nos Adapteurs Natifs

UST intègre des adaptateurs asynchrones ultra-rapides pour acheminer tout l'historique et les appels d'outils automatiques.

### 1. USTAdapter (Pour serveurs compatibles OpenAI / OpenRouter)
```python
import asyncio
from ust import USTAdapter, enable_branch

async def main():
    enable_branch("system")
    
    # Initialiser l'adaptateur avec votre clé et modèle de choix
    agent = USTAdapter(api_key="ta-cle-api", model="openai/gpt-4o-mini")
    
    # Envoyer un ordre en langage naturel
    reply = await agent.chat("Donne-moi l'état actuel de mon processeur et de ma mémoire vive.")
    print("Réponse de l'IA :", reply)

asyncio.run(main())
```

### 2. GeminiAdapter (Google GenAI natif)
Se connecte à l'API Gemini de Google via le SDK moderne `@google/genai` :
```python
from ust import GeminiAdapter
# agent = GeminiAdapter(api_key="GEMINI_API_KEY")
# reply = await agent.chat("Fais une capture d'écran et sauvegarde-la.")
```

### 3. LiteLLMAdapter (Multi-fournisseurs universel)
```python
from ust import LiteLLMAdapter
# agent = LiteLLMAdapter(model="anthropic/claude-3-5-sonnet")
```

### 4. OllamaAdapter (Pour vos modèles locaux)
```python
from ust import OllamaAdapter
# agent = OllamaAdapter(model="llama3")
```

---

##  Gestion de la Sécurité et des Autorisations

###  Middleware de Secrets (`require_secrets`)
Vous pouvez blinder la sécurité de votre application en exigeant que certaines clés d'API soient configurées de manière étanche avant l'interaction de votre agent :

```python
from ust import require_secrets

with require_secrets("OPENAI_API_KEY", "OPENWEATHERMAP_API_KEY"):
    # Vos appels d'agents s'exécutent en toute confiance
    pass
```

###  Gestion des Outils Dangereux
Certaines compétences (comme l'exécution de commandes shell `run_command` ou la neutralisation de processus `kill_process`) sont marquées comme **hautement sensibles**.
* UST intègre un avertissement interne automatique si un de ces outils est invoqué sans gestionnaire de confirmation explicite configuré.

###  Contrôle dynamique du Registre
Il est facile d'activer ou de désactiver des compétences individuellement au runtime pour affiner les autorisations :

```python
registry = get_registry()

# Désactiver temporairement l'exécution de ligne de commande
registry.disable("run_command")

# Réactiver à la volée une compétence
registry.enable("run_command")
```

---

##  Répertoire des 20+ Branches Disponibles

Le framework supporte un large éventail de spécialisations à travers des bibliothèques légères activables par dépendances optionnelles (PIP Extras) :

| Branche | Description | PIP Extras à installer |
|:---|:---|:---|
| **`system`** | Contrôle matériel de la machine, presse-papier, processus, volume. | `universal-skill-tree-naneg[system]` |
| **`files`** | Analyse de documents, lecture/écriture, métadonnées, CSV/Excel/Word. | `universal-skill-tree-naneg[files]` |
| **`web`** | Moteur de recherche DuckDuckGo, scraping HTTPX et parseur HTML. | `universal-skill-tree-naneg[web]` |
| **`vision`** | Captures d'écran multi-écrans, gestion des images et formats. | `universal-skill-tree-naneg[vision]` |
| **`browser`** | Web scraping dynamique et screenshots complets. | `universal-skill-tree-naneg[browser]` |
| **`smarthome`**| Intégration Home Assistant & objets connectés. | `universal-skill-tree-naneg[selfhosted]` |
| **`media`** | Gestion audio de l'ordinateur. | `universal-skill-tree-naneg[media]` |
| **`ai`** | Orchestration de sous-agents (CrewAI, LiteLLM). | `universal-skill-tree-naneg[ai]` |

Pour tout installer d'un coup, configurez simplement :
```bash
pip install universal-skill-tree-naneg[all]
```

---

##  Lancement des Tests Locaux

Pour s'assurer que votre implémentation est irréprochable et tester le comportement de la logique des outils en local sans consommer de crédit d'API payant :

```bash
python3 tests/test_ust.py

python tests/test_ust.py
```

*Les 32 tests de bout en bout valideront le chargement, l'idempotence, le câblage de l'exécuteur de tâches, les middlewares de sécurité, ainsi que les mocks d'adaptateurs IA.*

---

##  Prêt à propulser votre IA !
Grâce à l'architecture Plug & Play industrielle de **Universal Skill Tree**, votre agent dispose dorénavant d'un pont transparent pour interagir en toute sécurité avec le système d'exploitation et l'internet moderne.
