"""
examples/gemini_jarvis.py
──────────────────────────
Connect your existing Gemini JARVIS to UST in 3 lines.

Requirements:
    pip install 'universal-skill-tree[system,web,files]' google-genai
    export GEMINI_API_KEY=AIza...

Run:
    python examples/gemini_jarvis.py
"""
import asyncio
import os
import sys

# ─── THE 3 LINES ──────────────────────────────────────────────────────────────

from ust import enable_branch, GeminiAdapter

enable_branch("system")                        # Line 1
enable_branch("web")                           # Load web skills too
agent = GeminiAdapter(model="gemini-2.0-flash")  # Line 2 (reads GEMINI_API_KEY)

# ─────────────────────────────────────────────────────────────────────────────


async def main():
    from ust import status
    print("\n" + "═" * 60)
    print("  JARVIS × Universal Skill Tree — Gemini Edition")
    print("═" * 60)
    status()
    print("\nType your command (or 'quit' to exit):")
    print("Example: 'What's my CPU usage?' / 'Search for Python news'")
    print()

    history = []
    while True:
        try:
            user_input = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if not user_input or user_input.lower() in ("quit", "exit"):
            break

        print("JARVIS > ", end="", flush=True)
        reply = await agent.chat(user_input, history=history)
        print(reply)

        history.append({"role": "user",      "content": user_input})
        history.append({"role": "assistant", "content": reply})
        print()


if __name__ == "__main__":
    if not os.environ.get("GEMINI_API_KEY"):
        print("⚠️  Set GEMINI_API_KEY before running.")
        sys.exit(1)
    asyncio.run(main())
