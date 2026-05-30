"""
examples/openrouter_agent.py
────────────────────────────
Demonstration: Connect any LLM to your PC in 3 lines.

Requirements:
    pip install 'universal-skill-tree[system]'
    export OPENROUTER_API_KEY=sk-or-...

Run:
    python examples/openrouter_agent.py
"""
import sys
import os
import asyncio

# ─── THE 3 LINES THAT MATTER ──────────────────────────────────────────────────

from ust import enable_branch, USTAdapter

enable_branch("system")                              # Line 1: load PC control skills
agent = USTAdapter(model="openai/gpt-4o-mini")       # Line 2: create agent (reads OPENROUTER_API_KEY)

# ─────────────────────────────────────────────────────────────────────────────


async def demo():
    print("\n" + "═"*60)
    print("  Universal Skill Tree — Demo")
    print("═"*60)

    # Show what skills are loaded
    from ust import status
    status()

    # Interactive loop
    print("\nType your command (or 'quit' to exit):")
    print("Example: 'What is my CPU usage?' or 'Open notepad'")
    print()

    history = []

    while True:
        try:
            user_input = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input or user_input.lower() in ("quit", "exit", "q"):
            break

        print("Agent > ", end="", flush=True)
        reply = await agent.chat(user_input, history=history)
        print(reply)

        # Keep conversation history
        history.append({"role": "user",      "content": user_input})
        history.append({"role": "assistant", "content": reply})
        print()


if __name__ == "__main__":
    # Quick check
    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Set OPENROUTER_API_KEY or OPENAI_API_KEY before running.")
        print("   export OPENROUTER_API_KEY=sk-or-...")
        sys.exit(1)

    asyncio.run(demo())
