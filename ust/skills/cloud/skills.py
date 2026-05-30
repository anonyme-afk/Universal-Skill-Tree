""" ust.skills.cloud """\nfrom __future__ import annotations\nimport os\nimport json\nfrom ust.core.registry import skill\n\n@skill(\n    name="upload_to_s3",\n    branch="cloud",\n    description="Upload un fichier vers Amazon S3",\n    parameters={
    "properties": {
        "file_path": {
            "type": "string"
        },
        "bucket": {
            "type": "string"
        },
        "key": {
            "type": "string"
        }
    },
    "required": [
        "file_path",
        "bucket",
        "key"
    ]
},\n)\ndef upload_to_s3(file_path: str, bucket: str, key: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        return "Erreur Plug & Play : clé API manquante (AWS_ACCESS_KEY_ID). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("AWS_SECRET_ACCESS_KEY"):
        return "Erreur Plug & Play : clé API manquante (AWS_SECRET_ACCESS_KEY). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("AWS_DEFAULT_REGION"):
        return "Erreur Plug & Play : clé API manquante (AWS_DEFAULT_REGION). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import boto3
        s3 = boto3.client("s3")
        s3.upload_file(file_path, bucket, key)
        return f"Uploadé : s3://{bucket}/{key}"
    except ImportError as e:
        reqs_str = " ".join(['boto3']) if ['boto3'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="download_from_s3",\n    branch="cloud",\n    description="Télécharge un fichier depuis Amazon S3",\n    parameters={
    "properties": {
        "bucket": {
            "type": "string"
        },
        "key": {
            "type": "string"
        },
        "output": {
            "type": "string"
        }
    },
    "required": [
        "bucket",
        "key",
        "output"
    ]
},\n)\ndef download_from_s3(bucket: str, key: str, output: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        return "Erreur Plug & Play : clé API manquante (AWS_ACCESS_KEY_ID). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("AWS_SECRET_ACCESS_KEY"):
        return "Erreur Plug & Play : clé API manquante (AWS_SECRET_ACCESS_KEY). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("AWS_DEFAULT_REGION"):
        return "Erreur Plug & Play : clé API manquante (AWS_DEFAULT_REGION). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import boto3
        s3 = boto3.client("s3")
        s3.download_file(bucket, key, output)
        return f"Téléchargé : {output}"
    except ImportError as e:
        reqs_str = " ".join(['boto3']) if ['boto3'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="list_s3_files",\n    branch="cloud",\n    description="Liste les fichiers d'un bucket S3",\n    parameters={
    "properties": {
        "bucket": {
            "type": "string"
        },
        "prefix": {
            "type": "string"
        }
    },
    "required": [
        "bucket"
    ]
},\n)\ndef list_s3_files(bucket: str, prefix: str = "") -> list:
    # --- P&P Checks ---
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        return "Erreur Plug & Play : clé API manquante (AWS_ACCESS_KEY_ID). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("AWS_SECRET_ACCESS_KEY"):
        return "Erreur Plug & Play : clé API manquante (AWS_SECRET_ACCESS_KEY). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("AWS_DEFAULT_REGION"):
        return "Erreur Plug & Play : clé API manquante (AWS_DEFAULT_REGION). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import boto3
        s3 = boto3.client("s3")
        r = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return [obj["Key"] for obj in r.get("Contents", [])]
    except ImportError as e:
        reqs_str = " ".join(['boto3']) if ['boto3'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="upload_to_gdrive",\n    branch="cloud",\n    description="Upload un fichier vers Google Drive",\n    parameters={
    "properties": {
        "file_path": {
            "type": "string"
        },
        "folder_id": {
            "type": "string"
        }
    },
    "required": [
        "file_path"
    ]
},\n)\ndef upload_to_gdrive(file_path: str, folder_id: str = None) -> str:
    # --- P&P Checks ---
    if not os.getenv("GOOGLE_CREDENTIALS_PATH"):
        return "Erreur Plug & Play : clé API manquante (GOOGLE_CREDENTIALS_PATH). Ajoutez-la dans .env.ust puis réessayez."
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials
        import os
        creds = Credentials.from_authorized_user_file(os.getenv("GOOGLE_CREDENTIALS_PATH"))
        service = build("drive", "v3", credentials=creds)
        meta = {"name": os.path.basename(file_path)}
        if folder_id:
            meta["parents"] = [folder_id]
        media = MediaFileUpload(file_path, resumable=True)
        f = service.files().create(body=meta, media_body=media, fields="id").execute()
        return f"Fichier uploadé sur Drive, ID: {f.get('id')}"
    except ImportError as e:
        reqs_str = " ".join(['google-api-python-client', 'google-auth-oauthlib']) if ['google-api-python-client', 'google-auth-oauthlib'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="upload_to_dropbox",\n    branch="cloud",\n    description="Upload un fichier vers Dropbox",\n    parameters={
    "properties": {
        "file_path": {
            "type": "string"
        },
        "dest_path": {
            "type": "string"
        }
    },
    "required": [
        "file_path",
        "dest_path"
    ]
},\n)\ndef upload_to_dropbox(file_path: str, dest_path: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("DROPBOX_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (DROPBOX_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import dropbox
        dbx = dropbox.Dropbox(os.getenv("DROPBOX_TOKEN"))
        with open(file_path, "rb") as f:
            dbx.files_upload(f.read(), dest_path, mute=True)
        return f"Uploadé sur Dropbox : {dest_path}"
    except ImportError as e:
        reqs_str = " ".join(['dropbox']) if ['dropbox'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="create_cloudflare_kv",\n    branch="cloud",\n    description="Stocke une valeur dans Cloudflare KV",\n    parameters={
    "properties": {
        "key": {
            "type": "string"
        },
        "value": {
            "type": "string"
        }
    },
    "required": [
        "key",
        "value"
    ]
},\n)\ndef create_cloudflare_kv(key: str, value: str) -> str:
    # --- P&P Checks ---
    if not os.getenv("CF_ACCOUNT_ID"):
        return "Erreur Plug & Play : clé API manquante (CF_ACCOUNT_ID). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("CF_API_TOKEN"):
        return "Erreur Plug & Play : clé API manquante (CF_API_TOKEN). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("CF_KV_NAMESPACE_ID"):
        return "Erreur Plug & Play : clé API manquante (CF_KV_NAMESPACE_ID). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        url = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CF_ACCOUNT_ID')}/storage/kv/namespaces/{os.getenv('CF_KV_NAMESPACE_ID')}/values/{key}"
        r = requests.put(url, data=value, headers={"Authorization": f"Bearer {os.getenv('CF_API_TOKEN')}"})
        return f"KV créé (status {r.status_code})"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="firebase_write",\n    branch="cloud",\n    description="Écrit des données dans Firebase Realtime Database",\n    parameters={
    "properties": {
        "path": {
            "type": "string"
        },
        "data": {
            "type": "object"
        }
    },
    "required": [
        "path",
        "data"
    ]
},\n)\ndef firebase_write(path: str, data: dict) -> str:
    # --- P&P Checks ---
    if not os.getenv("FIREBASE_URL"):
        return "Erreur Plug & Play : clé API manquante (FIREBASE_URL). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("FIREBASE_SECRET"):
        return "Erreur Plug & Play : clé API manquante (FIREBASE_SECRET). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        url = f"{os.getenv('FIREBASE_URL')}/{path}.json?auth={os.getenv('FIREBASE_SECRET')}"
        r = requests.put(url, json=data)
        return f"Firebase écrit (status {r.status_code})"
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="firebase_read",\n    branch="cloud",\n    description="Lit des données depuis Firebase Realtime Database",\n    parameters={
    "properties": {
        "path": {
            "type": "string"
        }
    },
    "required": [
        "path"
    ]
},\n)\ndef firebase_read(path: str) -> dict:
    # --- P&P Checks ---
    if not os.getenv("FIREBASE_URL"):
        return "Erreur Plug & Play : clé API manquante (FIREBASE_URL). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("FIREBASE_SECRET"):
        return "Erreur Plug & Play : clé API manquante (FIREBASE_SECRET). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import requests
        url = f"{os.getenv('FIREBASE_URL')}/{path}.json?auth={os.getenv('FIREBASE_SECRET')}"
        return requests.get(url).json()
    except ImportError as e:
        reqs_str = " ".join(['requests']) if ['requests'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="pinecone_upsert",\n    branch="cloud",\n    description="Insère des vecteurs dans Pinecone (base de données vectorielle)",\n    parameters={
    "properties": {
        "vectors": {
            "type": "array"
        }
    },
    "required": [
        "vectors"
    ]
},\n)\ndef pinecone_upsert(vectors: list) -> str:
    # --- P&P Checks ---
    if not os.getenv("PINECONE_API_KEY"):
        return "Erreur Plug & Play : clé API manquante (PINECONE_API_KEY). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("PINECONE_INDEX"):
        return "Erreur Plug & Play : clé API manquante (PINECONE_INDEX). Ajoutez-la dans .env.ust puis réessayez."
    try:
        import pinecone
        pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
        index = pinecone.Index(os.getenv("PINECONE_INDEX"))
        index.upsert(vectors=vectors)
        return f"{len(vectors)} vecteurs insérés"
    except ImportError as e:
        reqs_str = " ".join(['pinecone-client']) if ['pinecone-client'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="supabase_insert",\n    branch="cloud",\n    description="Insère une ligne dans une table Supabase",\n    parameters={
    "properties": {
        "table": {
            "type": "string"
        },
        "data": {
            "type": "object"
        }
    },
    "required": [
        "table",
        "data"
    ]
},\n)\ndef supabase_insert(table: str, data: dict) -> dict:
    # --- P&P Checks ---
    if not os.getenv("SUPABASE_URL"):
        return "Erreur Plug & Play : clé API manquante (SUPABASE_URL). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("SUPABASE_KEY"):
        return "Erreur Plug & Play : clé API manquante (SUPABASE_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        from supabase import create_client
        sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        return sb.table(table).insert(data).execute().data
    except ImportError as e:
        reqs_str = " ".join(['supabase']) if ['supabase'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="supabase_select",\n    branch="cloud",\n    description="Lit des données depuis une table Supabase",\n    parameters={
    "properties": {
        "table": {
            "type": "string"
        },
        "filters": {
            "type": "object"
        }
    },
    "required": [
        "table"
    ]
},\n)\ndef supabase_select(table: str, filters: dict = {}) -> list:
    # --- P&P Checks ---
    if not os.getenv("SUPABASE_URL"):
        return "Erreur Plug & Play : clé API manquante (SUPABASE_URL). Ajoutez-la dans .env.ust puis réessayez."
    if not os.getenv("SUPABASE_KEY"):
        return "Erreur Plug & Play : clé API manquante (SUPABASE_KEY). Ajoutez-la dans .env.ust puis réessayez."
    try:
        from supabase import create_client
        sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        query = sb.table(table).select("*")
        for k, v in filters.items():
            query = query.eq(k, v)
        return query.execute().data
    except ImportError as e:
        reqs_str = " ".join(['supabase']) if ['supabase'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


