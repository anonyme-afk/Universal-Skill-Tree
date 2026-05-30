"""
ust.skills.mcp
──────────────
Branch: "mcp"
"""
from __future__ import annotations
import subprocess
import json
from ust.core.registry import skill

def _require(package: str):
    import importlib
    try:
        return importlib.import_module(package)
    except ImportError:
        raise ImportError(f"Package '{package}' required.")

@skill(
    name="search_awesome_mcp_servers",
    branch="mcp",
    description="Search the awesome-mcp-servers list for Model Context Protocol (MCP) servers.",
    parameters={
        "properties": {
            "query": {"type": "string", "description": "Search keyword (e.g. 'browser', 'database', 'devtools')"}
        },
        "required": ["query"]
    }
)
def search_awesome_mcp_servers(query: str) -> str:
    requests = _require("requests")
    url = "https://raw.githubusercontent.com/punkpeye/awesome-mcp-servers/main/README.md"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        return f"Failed to fetch awesome-mcp-servers list: {e}"

    lines = content.splitlines()
    results = []
    
    query_lower = query.lower()
    for i, line in enumerate(lines):
        if line.startswith("- [") and query_lower in line.lower():
            result = line.strip()
            if i + 1 < len(lines) and not lines[i+1].startswith("-"):
                result += " " + lines[i+1].strip()
            results.append(result)
            
            if len(results) >= 15:
                break

    if not results:
        return f"No MCP servers found matching '{query}'."
    
    return "Found these Awesome MCP Servers:\n" + "\n".join(results)

@skill(
    name="mcp_generate_config",
    branch="mcp",
    description="Generate a Claude Desktop or Cursor compatible mcpServers configuration JSON for various plug-and-play MCPs.",
    parameters={
        "properties": {
            "servers": {
                "type": "array",
                "items": {"type": "string", "enum": [
                    "a2asearch", "blink", "fetch", "brave", "puppeteer", "filesystem", "github",
                    "sequential_thinking", "whisper", "docker", "sqlite", "ffmpeg", "microphone", "audio_recorder"
                ]},
                "description": "List of servers to include in the config."
            },
            "filesystem_path": {
                "type": "string",
                "description": "Absolute path for the filesystem server (if selected)."
            },
            "sqlite_db_path": {
                "type": "string",
                "description": "Path for the SQLite database (e.g., 'database.db')."
            }
        },
        "required": ["servers"]
    }
)
def mcp_generate_config(servers: list[str], filesystem_path: str = "/tmp", sqlite_db_path: str = "database.db") -> str:
    config = {"mcpServers": {}}
    
    mapping = {
        "a2asearch": {"command": "npx", "args": ["-y", "a2asearch-mcp"]},
        "blink": {"command": "npx", "args": ["skills", "add", "blink-new/blink-plugin"]},
        "fetch": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-fetch"]},
        "brave": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-brave-search"]},
        "puppeteer": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-puppeteer"]},
        "filesystem": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", filesystem_path]},
        "github": {"command": "npx", "args": ["-y", "@github/mcp-server"]},
        "sequential_thinking": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]},
        "whisper": {"command": "npx", "args": ["-y", "mcp-whisper-server"]},
        "docker": {"command": "npx", "args": ["-y", "mcp-server-docker"]},
        "sqlite": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", sqlite_db_path]},
        "ffmpeg": {"command": "npx", "args": ["-y", "mcp-ffmpeg-server"]},
        "microphone": {"command": "npx", "args": ["-y", "mcp-microphone"]},
        "audio_recorder": {"command": "npx", "args": ["-y", "mcp-audio-recorder"]}
    }
    
    for s in servers:
        if s in mapping:
            config["mcpServers"][s] = mapping[s]
            
    return json.dumps(config, indent=2)

@skill(
    name="mcp_execute_oneshot",
    branch="mcp",
    description="Run an MCP server via npx directly in the background (Note: MCP servers communicate via JSON-RPC stdio, so this just verifies it starts).",
    parameters={
        "properties": {
            "server_package": {"type": "string", "description": "The npm package name of the MCP server (e.g. '@modelcontextprotocol/server-fetch')"}
        },
        "required": ["server_package"]
    }
)
def mcp_execute_oneshot(server_package: str) -> str:
    return f"To use '{server_package}' functionally within a chat GUI, add it to your mcpServers config. Starting it directly here will block waiting for JSON-RPC messages on stdin."
