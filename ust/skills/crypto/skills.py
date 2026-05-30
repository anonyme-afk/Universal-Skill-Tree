"""
ust.skills.crypto
─────────────────
Branch: "crypto"
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
    name="crypto_price",
    branch="crypto",
    description="Get current crypto prices via CCXT",
    parameters={"properties": {"symbol": {"type": "string", "description": "e.g., BTC/USDT"}}}
)
def crypto_price(symbol: str) -> str:
    ccxt = _require("ccxt")
    exchange = ccxt.binance()
    ticker = exchange.fetch_ticker(symbol)
    return f"Current price of {symbol}: {ticker['last']}"
