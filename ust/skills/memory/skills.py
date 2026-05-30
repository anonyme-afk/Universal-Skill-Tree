""" ust.skills.memory """\nfrom __future__ import annotations\nimport os\nimport json\nfrom ust.core.registry import skill\n\n@skill(\n    name="memory_add",\n    branch="memory",\n    description="Ajoute une information à la mémoire locale (JSON)",\n    parameters={
    "properties": {
        "key": {
            "type": "string"
        },
        "value": {
            "type": "string"
        },
        "db_path": {
            "type": "string"
        }
    },
    "required": [
        "key",
        "value"
    ]
},\n)\ndef memory_add(key: str, value: str, db_path: str = "ust_memory.json") -> str:
    # --- P&P Checks ---
    try:
        import json, os
        db = {}
        if os.path.exists(db_path):
            with open(db_path) as f:
                db = json.load(f)
        db[key] = value
        with open(db_path, "w") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        return f"Mémorisé : {key}"
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="memory_get",\n    branch="memory",\n    description="Récupère une information mémorisée",\n    parameters={
    "properties": {
        "key": {
            "type": "string"
        },
        "db_path": {
            "type": "string"
        }
    },
    "required": [
        "key"
    ]
},\n)\ndef memory_get(key: str, db_path: str = "ust_memory.json") -> str:
    # --- P&P Checks ---
    try:
        import json, os
        if not os.path.exists(db_path):
            return f"Clé non trouvée : {key}"
        with open(db_path) as f:
            db = json.load(f)
        return db.get(key, f"Clé non trouvée : {key}")
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="memory_list",\n    branch="memory",\n    description="Liste toutes les entrées mémorisées",\n    parameters={
    "properties": {
        "db_path": {
            "type": "string"
        }
    }
},\n)\ndef memory_list(db_path: str = "ust_memory.json") -> dict:
    # --- P&P Checks ---
    try:
        import json, os
        if not os.path.exists(db_path):
            return {}
        with open(db_path) as f:
            return json.load(f)
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="memory_delete",\n    branch="memory",\n    description="Supprime une entrée mémorisée",\n    parameters={
    "properties": {
        "key": {
            "type": "string"
        },
        "db_path": {
            "type": "string"
        }
    },
    "required": [
        "key"
    ]
},\n)\ndef memory_delete(key: str, db_path: str = "ust_memory.json") -> str:
    # --- P&P Checks ---
    try:
        import json, os
        if not os.path.exists(db_path):
            return "Mémoire vide"
        with open(db_path) as f:
            db = json.load(f)
        db.pop(key, None)
        with open(db_path, "w") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        return f"Supprimé : {key}"
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="rag_index_folder",\n    branch="memory",\n    description="Indexe tous les fichiers texte d'un dossier pour RAG (recherche sémantique locale)",\n    parameters={
    "properties": {
        "folder": {
            "type": "string"
        },
        "collection_name": {
            "type": "string"
        }
    },
    "required": [
        "folder"
    ]
},\n)\ndef rag_index_folder(folder: str, collection_name: str = "ust_docs") -> str:
    # --- P&P Checks ---
    if not os.getenv("OPENAI_API_KEY"):
        return "Erreur Plug & Play : clé API manquante (OPENAI_API_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import os, chromadb
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        chroma = chromadb.PersistentClient(path=".ust_chroma")
        col = chroma.get_or_create_collection(collection_name)
        count = 0
        for fname in os.listdir(folder):
            path = os.path.join(folder, fname)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()[:4000]
                emb = client.embeddings.create(input=content, model="text-embedding-3-small").data[0].embedding
                col.upsert(ids=[fname], documents=[content], embeddings=[emb])
                count += 1
            except:
                pass
        return f"{count} fichiers indexés dans '{collection_name}'"
    except ImportError as e:
        reqs_str = " ".join(['chromadb', 'openai']) if ['chromadb', 'openai'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="rag_search",\n    branch="memory",\n    description="Recherche sémantique dans les documents indexés (RAG local)",\n    parameters={
    "properties": {
        "query": {
            "type": "string"
        },
        "collection_name": {
            "type": "string"
        },
        "n_results": {
            "type": "integer"
        }
    },
    "required": [
        "query"
    ]
},\n)\ndef rag_search(query: str, collection_name: str = "ust_docs", n_results: int = 3) -> list:
    # --- P&P Checks ---
    if not os.getenv("OPENAI_API_KEY"):
        return "Erreur Plug & Play : clé API manquante (OPENAI_API_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import chromadb
        from openai import OpenAI
        import os
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        chroma = chromadb.PersistentClient(path=".ust_chroma")
        col = chroma.get_or_create_collection(collection_name)
        emb = client.embeddings.create(input=query, model="text-embedding-3-small").data[0].embedding
        results = col.query(query_embeddings=[emb], n_results=n_results)
        return results["documents"][0]
    except ImportError as e:
        reqs_str = " ".join(['chromadb', 'openai']) if ['chromadb', 'openai'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="rag_ask",\n    branch="memory",\n    description="Pose une question à tes documents indexés (RAG complet)",\n    parameters={
    "properties": {
        "question": {
            "type": "string"
        },
        "collection_name": {
            "type": "string"
        }
    },
    "required": [
        "question"
    ]
},\n)\ndef rag_ask(question: str, collection_name: str = "ust_docs") -> str:
    # --- P&P Checks ---
    if not os.getenv("OPENAI_API_KEY"):
        return "Erreur Plug & Play : clé API manquante (OPENAI_API_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import chromadb
        from openai import OpenAI
        import os
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        chroma = chromadb.PersistentClient(path=".ust_chroma")
        col = chroma.get_or_create_collection(collection_name)
        emb = client.embeddings.create(input=question, model="text-embedding-3-small").data[0].embedding
        docs = col.query(query_embeddings=[emb], n_results=3)["documents"][0]
        context = "
    ---
    ".join(docs)
        prompt = f"Réponds à la question en te basant uniquement sur ces documents :
    {context}
    Question: {question}"
        r = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
        return r.choices[0].message.content
    except ImportError as e:
        reqs_str = " ".join(['chromadb', 'openai']) if ['chromadb', 'openai'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


