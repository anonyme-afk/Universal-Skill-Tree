""" ust.skills.dev """\nfrom __future__ import annotations\nimport os\nimport json\nfrom ust.core.registry import skill\n\n@skill(\n    name="lint_python_code",\n    branch="dev",\n    description="Analyse la qualité d'un fichier Python (pylint)",\n    parameters={
    "properties": {
        "file_path": {
            "type": "string"
        }
    },
    "required": [
        "file_path"
    ]
},\n)\ndef lint_python_code(file_path: str) -> str:
    # --- P&P Checks ---
    try:
        import subprocess
        r = subprocess.run(["pylint", file_path, "--output-format=text"], capture_output=True, text=True)
        return r.stdout or r.stderr
    except ImportError as e:
        reqs_str = " ".join(['pylint']) if ['pylint'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="format_python_code",\n    branch="dev",\n    description="Formate du code Python avec Black",\n    parameters={
    "properties": {
        "file_path": {
            "type": "string"
        }
    },
    "required": [
        "file_path"
    ]
},\n)\ndef format_python_code(file_path: str) -> str:
    # --- P&P Checks ---
    try:
        import subprocess
        r = subprocess.run(["black", file_path], capture_output=True, text=True)
        return r.stdout + r.stderr
    except ImportError as e:
        reqs_str = " ".join(['black']) if ['black'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="run_pytest",\n    branch="dev",\n    description="Lance les tests pytest d'un projet",\n    parameters={
    "properties": {
        "test_path": {
            "type": "string"
        },
        "verbose": {
            "type": "boolean"
        }
    }
},\n)\ndef run_pytest(test_path: str = ".", verbose: bool = True) -> str:
    # --- P&P Checks ---
    try:
        import subprocess
        args = ["pytest", test_path]
        if verbose:
            args.append("-v")
        r = subprocess.run(args, capture_output=True, text=True)
        return r.stdout + r.stderr
    except ImportError as e:
        reqs_str = " ".join(['pytest']) if ['pytest'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="git_commit_push",\n    branch="dev",\n    description="Stage, commit et push tous les changements Git",\n    parameters={
    "properties": {
        "message": {
            "type": "string"
        },
        "branch": {
            "type": "string"
        }
    }
},\n)\ndef git_commit_push(message: str = "UST auto-commit", branch: str = "main") -> str:
    # --- P&P Checks ---
    try:
        import subprocess
        results = []
        for cmd in [
            ["git", "add", "-A"],
            ["git", "commit", "-m", message],
            ["git", "push", "origin", branch]
        ]:
            r = subprocess.run(cmd, capture_output=True, text=True)
            results.append(r.stdout or r.stderr)
        return "
    ".join(results)
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="git_status",\n    branch="dev",\n    description="Retourne le statut Git du dossier courant",\n    parameters={
    "properties": {
        "path": {
            "type": "string"
        }
    }
},\n)\ndef git_status(path: str = ".") -> str:
    # --- P&P Checks ---
    try:
        import subprocess
        r = subprocess.run(["git", "-C", path, "status"], capture_output=True, text=True)
        return r.stdout
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="create_virtualenv",\n    branch="dev",\n    description="Crée un environnement virtuel Python",\n    parameters={
    "properties": {
        "name": {
            "type": "string"
        }
    }
},\n)\ndef create_virtualenv(name: str = "venv") -> str:
    # --- P&P Checks ---
    try:
        import subprocess
        r = subprocess.run(["python", "-m", "venv", name], capture_output=True, text=True)
        return f"Virtualenv '{name}' créé" if r.returncode == 0 else r.stderr
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="install_package",\n    branch="dev",\n    description="Installe un ou plusieurs packages pip",\n    parameters={
    "properties": {
        "packages": {
            "type": "array"
        }
    },
    "required": [
        "packages"
    ]
},\n)\ndef install_package(packages: list) -> str:
    # --- P&P Checks ---
    try:
        import subprocess
        r = subprocess.run(["pip", "install"] + packages, capture_output=True, text=True)
        return r.stdout or r.stderr
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="generate_requirements",\n    branch="dev",\n    description="Génère un fichier requirements.txt depuis pip freeze",\n    parameters={
    "properties": {
        "output": {
            "type": "string"
        }
    }
},\n)\ndef generate_requirements(output: str = "requirements.txt") -> str:
    # --- P&P Checks ---
    try:
        import subprocess
        r = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
        with open(output, "w") as f:
            f.write(r.stdout)
        return f"requirements.txt généré : {len(r.stdout.splitlines())} packages"
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="create_dockerfile",\n    branch="dev",\n    description="Génère un Dockerfile de base pour un projet Python",\n    parameters={
    "properties": {
        "app_file": {
            "type": "string"
        },
        "python_version": {
            "type": "string"
        }
    }
},\n)\ndef create_dockerfile(app_file: str = "main.py", python_version: str = "3.11") -> str:
    # --- P&P Checks ---
    try:
        content = f"FROM python:{python_version}-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD ["python", "{app_file}"]
    "
        with open("Dockerfile", "w") as f:
            f.write(content)
        return "Dockerfile créé"
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="docker_run",\n    branch="dev",\n    description="Lance un conteneur Docker",\n    parameters={
    "properties": {
        "image": {
            "type": "string"
        },
        "command": {
            "type": "string"
        },
        "ports": {
            "type": "string"
        }
    },
    "required": [
        "image"
    ]
},\n)\ndef docker_run(image: str, command: str = "", ports: str = "") -> str:
    # --- P&P Checks ---
    try:
        import subprocess
        args = ["docker", "run", "-d"]
        if ports:
            args += ["-p", ports]
        args.append(image)
        if command:
            args += command.split()
        r = subprocess.run(args, capture_output=True, text=True)
        return r.stdout.strip() or r.stderr
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="convert_code_language",\n    branch="dev",\n    description="Convertit du code d'un langage à un autre via IA (OpenAI)",\n    parameters={
    "properties": {
        "code": {
            "type": "string"
        },
        "from_lang": {
            "type": "string"
        },
        "to_lang": {
            "type": "string"
        }
    },
    "required": [
        "code",
        "from_lang",
        "to_lang"
    ]
},\n)\ndef convert_code_language(code: str, from_lang: str, to_lang: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("OPENAI_API_KEY"):
        return "Erreur Plug & Play : clé API manquante (OPENAI_API_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = f"Convertis ce code {from_lang} en {to_lang}. Retourne uniquement le code, sans explications.
    {code}"
        r = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
        return r.choices[0].message.content
    except ImportError as e:
        reqs_str = " ".join(['openai']) if ['openai'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="explain_code",\n    branch="dev",\n    description="Explique un bout de code en langage naturel (via IA)",\n    parameters={
    "properties": {
        "code": {
            "type": "string"
        },
        "language": {
            "type": "string"
        }
    },
    "required": [
        "code"
    ]
},\n)\ndef explain_code(code: str, language: str = "Python") -> str:
    # --- P&P Checks ---
    if not os.getenv("OPENAI_API_KEY"):
        return "Erreur Plug & Play : clé API manquante (OPENAI_API_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = f"Explique ce code {language} en français, simplement :
    {code}"
        r = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
        return r.choices[0].message.content
    except ImportError as e:
        reqs_str = " ".join(['openai']) if ['openai'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


