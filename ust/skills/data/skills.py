""" ust.skills.data """
from __future__ import annotations
import os
import json
from ust.core.registry import skill

@skill(
    name="analyze_csv_data",
    branch="data",
    description="Analyse statistique d'un CSV (min, max, moyenne, etc.)",
    parameters={
    "properties": {
        "path": {
            "type": "string"
        }
    },
    "required": [
        "path"
    ]
},
)
def analyze_csv_data(path: str) -> str:
    import pandas as pd
    df = pd.read_csv(path)
    return df.describe().to_string()


@skill(
    name="generate_chart",
    branch="data",
    description="Génère un graphique à partir de données",
    parameters={
    "properties": {
        "x": {
            "type": "array"
        },
        "y": {
            "type": "array"
        },
        "title": {
            "type": "string"
        },
        "chart_type": {
            "type": "string"
        },
        "output": {
            "type": "string"
        }
    },
    "required": [
        "x",
        "y"
    ]
},
)
def generate_chart(x: list, y: list, title: str = "Chart", chart_type: str = "line", output: str = "chart.png") -> str:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    if chart_type == "bar": ax.bar(x, y)
    elif chart_type == "scatter": ax.scatter(x, y)
    else: ax.plot(x, y)
    ax.set_title(title)
    plt.savefig(output)
    plt.close()
    return f"Graphique sauvegardé : {output}"


@skill(
    name="sqlite_query",
    branch="data",
    description="Exécute une requête SQL sur une base de données SQLite",
    parameters={
    "properties": {
        "db_path": {
            "type": "string"
        },
        "query": {
            "type": "string"
        }
    },
    "required": [
        "db_path",
        "query"
    ]
},
)
def sqlite_query(db_path: str, query: str) -> list:
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.commit()
    conn.close()
    return rows


@skill(
    name="web_scrape_table",
    branch="data",
    description="Extrait les tableaux HTML d'une page web",
    parameters={
    "properties": {
        "url": {
            "type": "string"
        }
    },
    "required": [
        "url"
    ]
},
)
def web_scrape_table(url: str) -> list:
    import pandas as pd
    tables = pd.read_html(url)
    return [t.to_dict() for t in tables]


@skill(
    name="calculate_expression",
    branch="data",
    description="Calcule une expression mathématique",
    parameters={
    "properties": {
        "expression": {
            "type": "string"
        }
    },
    "required": [
        "expression"
    ]
},
)
def calculate_expression(expression: str) -> float:
    import math
    allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith('_')}
    allowed.update({'abs': abs, 'round': round})
    return eval(expression, {"__builtins__": {}}, allowed)


@skill(
    name="convert_json_to_csv",
    branch="data",
    description="Convertit un fichier JSON en CSV",
    parameters={
    "properties": {
        "json_path": {
            "type": "string"
        },
        "csv_path": {
            "type": "string"
        }
    },
    "required": [
        "json_path",
        "csv_path"
    ]
},
)
def convert_json_to_csv(json_path: str, csv_path: str) -> str:
    import pandas as pd
    df = pd.read_json(json_path)
    df.to_csv(csv_path, index=False)
    return f"CSV créé : {csv_path}"


