""" ust.skills.system """\nfrom __future__ import annotations\nimport os\nimport json\nfrom ust.core.registry import skill\n\n@skill(\n    name="get_cpu_usage",\n    branch="system",\n    description="Retourne l'utilisation CPU en %",\n    parameters={},\n)\ndef get_cpu_usage() -> float:
    # --- P&P Checks ---
    try:
        import psutil
        return psutil.cpu_percent(interval=1)
    except ImportError as e:
        reqs_str = " ".join(['psutil']) if ['psutil'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_ram_usage",\n    branch="system",\n    description="Retourne l'utilisation RAM",\n    parameters={},\n)\ndef get_ram_usage() -> dict:
    # --- P&P Checks ---
    try:
        import psutil
        m = psutil.virtual_memory()
        return {"total_gb": round(m.total/1e9,2), "used_gb": round(m.used/1e9,2), "percent": m.percent}
    except ImportError as e:
        reqs_str = " ".join(['psutil']) if ['psutil'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_disk_usage",\n    branch="system",\n    description="Retourne l'espace disque disponible",\n    parameters={
    "properties": {
        "path": {
            "type": "string"
        }
    }
},\n)\ndef get_disk_usage(path: str = "/") -> dict:
    # --- P&P Checks ---
    try:
        import psutil
        d = psutil.disk_usage(path)
        return {"total_gb": round(d.total/1e9,2), "used_gb": round(d.used/1e9,2), "free_gb": round(d.free/1e9,2), "percent": d.percent}
    except ImportError as e:
        reqs_str = " ".join(['psutil']) if ['psutil'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="run_command",\n    branch="system",\n    description="Exécute une commande shell et retourne la sortie",\n    parameters={
    "properties": {
        "command": {
            "type": "string"
        }
    },
    "required": [
        "command"
    ]
},\n)\ndef run_command(command: str) -> str:
    # --- P&P Checks ---
    try:
        import subprocess
        r = subprocess.run(command, shell=True, capture_output=True, text=True)
        return r.stdout or r.stderr
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="list_processes",\n    branch="system",\n    description="Liste les processus actifs (top 20 par CPU)",\n    parameters={},\n)\ndef list_processes() -> list:
    # --- P&P Checks ---
    try:
        import psutil
        procs = []
        for p in psutil.process_iter(['pid','name','cpu_percent','memory_percent']):
            try:
                procs.append(p.info)
            except:
                pass
        return sorted(procs, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:20]
    except ImportError as e:
        reqs_str = " ".join(['psutil']) if ['psutil'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="kill_process",\n    branch="system",\n    description="Tue un processus par son PID",\n    parameters={
    "properties": {
        "pid": {
            "type": "integer"
        }
    },
    "required": [
        "pid"
    ]
},\n)\ndef kill_process(pid: int) -> str:
    # --- P&P Checks ---
    try:
        import psutil
        try:
            p = psutil.Process(pid)
            p.kill()
            return f"Processus {pid} tué"
        except Exception as e:
            return f"Erreur: {e}"
    except ImportError as e:
        reqs_str = " ".join(['psutil']) if ['psutil'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_os_info",\n    branch="system",\n    description="Retourne les infos du système d'exploitation",\n    parameters={},\n)\ndef get_os_info() -> dict:
    # --- P&P Checks ---
    try:
        import platform
        return {
            "os": platform.system(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node(),
            "python": platform.python_version()
        }
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_battery_status",\n    branch="system",\n    description="Retourne l'état de la batterie",\n    parameters={},\n)\ndef get_battery_status() -> dict:
    # --- P&P Checks ---
    try:
        import psutil
        b = psutil.sensors_battery()
        if not b:
            return {"error": "Pas de batterie détectée"}
        return {"percent": b.percent, "charging": b.power_plugged, "time_left_min": round(b.secsleft/60) if b.secsleft > 0 else "inconnu"}
    except ImportError as e:
        reqs_str = " ".join(['psutil']) if ['psutil'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="screenshot",\n    branch="system",\n    description="Prend une capture d'écran et la sauvegarde",\n    parameters={
    "properties": {
        "save_path": {
            "type": "string"
        }
    }
},\n)\ndef screenshot(save_path: str = "screenshot.png") -> str:
    # --- P&P Checks ---
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab()
        img.save(save_path)
        return f"Screenshot sauvegardé : {save_path}"
    except ImportError as e:
        reqs_str = " ".join(['pillow']) if ['pillow'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="set_clipboard",\n    branch="system",\n    description="Met du texte dans le presse-papier",\n    parameters={
    "properties": {
        "text": {
            "type": "string"
        }
    },
    "required": [
        "text"
    ]
},\n)\ndef set_clipboard(text: str) -> str:
    # --- P&P Checks ---
    try:
        import pyperclip
        pyperclip.copy(text)
        return "Texte copié dans le presse-papier"
    except ImportError as e:
        reqs_str = " ".join(['pyperclip']) if ['pyperclip'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_clipboard",\n    branch="system",\n    description="Lit le contenu du presse-papier",\n    parameters={},\n)\ndef get_clipboard() -> str:
    # --- P&P Checks ---
    try:
        import pyperclip
        return pyperclip.paste()
    except ImportError as e:
        reqs_str = " ".join(['pyperclip']) if ['pyperclip'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="open_url_browser",\n    branch="system",\n    description="Ouvre une URL dans le navigateur par défaut",\n    parameters={
    "properties": {
        "url": {
            "type": "string"
        }
    },
    "required": [
        "url"
    ]
},\n)\ndef open_url_browser(url: str) -> str:
    # --- P&P Checks ---
    try:
        import webbrowser
        webbrowser.open(url)
        return f"URL ouverte : {url}"
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="send_notification_desktop",\n    branch="system",\n    description="Envoie une notification desktop (Windows/Mac/Linux)",\n    parameters={
    "properties": {
        "title": {
            "type": "string"
        },
        "message": {
            "type": "string"
        }
    },
    "required": [
        "title",
        "message"
    ]
},\n)\ndef send_notification_desktop(title: str, message: str) -> str:
    # --- P&P Checks ---
    try:
        from plyer import notification
        notification.notify(title=title, message=message, timeout=5)
        return f"Notification envoyée : {title}"
    except ImportError as e:
        reqs_str = " ".join(['plyer']) if ['plyer'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="get_network_speed",\n    branch="system",\n    description="Retourne les stats réseau (bytes envoyés/reçus)",\n    parameters={},\n)\ndef get_network_speed() -> dict:
    # --- P&P Checks ---
    try:
        import psutil, time
        n1 = psutil.net_io_counters()
        time.sleep(1)
        n2 = psutil.net_io_counters()
        return {
            "download_kbps": round((n2.bytes_recv - n1.bytes_recv) / 1024, 2),
            "upload_kbps": round((n2.bytes_sent - n1.bytes_sent) / 1024, 2)
        }
    except ImportError as e:
        reqs_str = " ".join(['psutil']) if ['psutil'] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


@skill(\n    name="lock_screen",\n    branch="system",\n    description="Verrouille l'écran (Windows/Mac/Linux)",\n    parameters={},\n)\ndef lock_screen() -> str:
    # --- P&P Checks ---
    try:
        import platform, subprocess
        s = platform.system()
        if s == "Windows":
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
        elif s == "Darwin":
            subprocess.run(["pmset", "displaysleepnow"])
        else:
            subprocess.run(["xdg-screensaver", "lock"])
        return "Écran verrouillé"
    except ImportError as e:
        reqs_str = " ".join([]) if [] else str(e)
        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str
    except Exception as e:
        return f"Erreur inattendue : {e}"


