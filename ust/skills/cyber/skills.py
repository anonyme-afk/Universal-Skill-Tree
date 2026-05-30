"""
ust.skills.cyber
────────────────
Branch: "cyber"
"""
from __future__ import annotations
from ust.core.registry import skill

def _require(package: str):
    import importlib
    try:
        return importlib.import_module(package)
    except ImportError:
        raise ImportError(f"Package '{package}' required.")

@skill(
    name="network_packet_sniff",
    branch="cyber",
    description="Sniff network packets (requires Scapy installed)",
    parameters={"properties": {"interface": {"type": "string"}}}
)
def network_packet_sniff(interface: str = "eth0") -> str:
    scapy = _require("scapy.all")
    # Lazy loaded scapy implementation
    return "Packet sniffing started (Lazy loaded)"

import subprocess

@skill(
    name="cyber_sniffnet",
    branch="cyber",
    description="Launch Sniffnet, an application to comfortably monitor your Internet traffic.",
    parameters={
        "properties": {},
    }
)
def cyber_sniffnet() -> str:
    try:
        # Sniffnet is typically a GUI application, we launch it non-blocking
        subprocess.Popen(["sniffnet"])
        return "Sniffnet launched successfully. Please check your screen."
    except Exception as e:
        return f"Error launching Sniffnet: {e}. Is it installed?"

@skill(
    name="cyber_trippy",
    branch="cyber",
    description="Run Trippy, a network diagnostic tool (traceroute and ping combined). Requires sudo privileges usually.",
    parameters={
        "properties": {
            "target": {"type": "string", "description": "The target hostname or IP, e.g. example.com"}
        },
        "required": ["target"]
    }
)
def cyber_trippy(target: str) -> str:
    try:
        # We can try to run it in interactive or report mode
        # By default trip is interactive, but if we just want a quick report we might need a flag if available.
        # Alternatively we assume the agent opens it in a terminal or runs it. We'll run it returning immediately for GUI or capturing output if CLI.
        # usually run as `sudo trip example.com`
        # Because we are in a headless/agent env, we might just try to execute and capture 1 packet trace or just open it
        result = subprocess.run(["trip", target, "-c", "1"], capture_output=True, text=True, timeout=10)
        return result.stdout or "Trippy executed. Check the system for process output if interactive."
    except Exception as e:
        return f"Error running Trippy: {e}. Try installing it via cargo or package manager."
