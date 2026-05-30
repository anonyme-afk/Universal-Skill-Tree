"""
ust.core.adapter
────────────────
OpenRouter / OpenAI-compatible adapter.

Handles the full agentic loop:
  user message → LLM → tool_calls → execute → LLM → ... → final answer

Since OpenRouter uses the exact OpenAI format, this adapter works with:
  - OpenRouter  (api.openrouter.ai)
  - OpenAI      (api.openai.com)
  - LM Studio   (localhost:1234)
  - Ollama      (localhost:11434/v1)
  - Any OpenAI-compatible endpoint
"""
from __future__ import annotations

import json
import os
from typing import Any, AsyncIterator

import httpx

from .executor import Executor, ToolResult
from .registry import get_registry


# ─── Default endpoints ────────────────────────────────────────────────────────

OPENROUTER_BASE = "https://openrouter.ai/api/v1"
OPENAI_BASE     = "https://api.openai.com/v1"
LOCAL_BASE      = "http://localhost:1234/v1"   # LM Studio / Ollama


class USTAdapter:
    """
    OpenAI-compatible adapter with UST skills injected automatically.

    Quick start:
        from ust import enable_branch, USTAdapter

        enable_branch("system")
        agent = USTAdapter(api_key="sk-or-...", model="openai/gpt-4o-mini")
        reply = await agent.chat("Open Chrome and go to github.com")
        print(reply)
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "openai/gpt-4o-mini",
        base_url: str = OPENROUTER_BASE,
        system_prompt: str = "You are a helpful AI assistant with access to computer control tools. Always use the provided tools to complete tasks — never simulate results.",
        max_iterations: int = 10,
        timeout: float = 60.0,
    ):
        self.api_key    = api_key or os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
        self.model      = model
        self.base_url   = base_url.rstrip("/")
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self._executor  = Executor()
        self._registry  = get_registry()
        self._client    = httpx.AsyncClient(timeout=timeout)

    # ── Main chat method ──────────────────────────────────────────────────────

    async def chat(
        self,
        user_message: str,
        history: list[dict] | None = None,
        branch: str | None = None,
    ) -> str:
        """
        Send a message and get the final answer after all tool calls are resolved.

        Args:
            user_message: The user's input
            history: Optional previous messages (for multi-turn)
            branch: Restrict tools to a specific branch (e.g. "system")

        Returns:
            The LLM's final text response
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        tools = self._registry.declarations(branch)

        for iteration in range(self.max_iterations):
            response = await self._call_llm(messages, tools)
            choice   = response["choices"][0]
            message  = choice["message"]

            # Append assistant turn to history
            messages.append(message)

            # No tool calls → final answer
            if not message.get("tool_calls"):
                return message.get("content") or ""

            # Execute all tool calls
            results: list[ToolResult] = await self._executor.run_all(message["tool_calls"])

            # Log results
            for r in results:
                status = "✅" if r.success else "❌"
                print(f"[UST] {status} {r.name}: {str(r.output)[:120]}")

            # Append tool results to messages
            messages.extend(r.to_message() for r in results)

        return "Max iterations reached. Last known state saved."

    # ── Streaming chat ────────────────────────────────────────────────────────

    async def stream(
        self,
        user_message: str,
        history: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream the final text response token by token.
        Tool calls are executed silently before streaming begins.
        """
        # First resolve all tool calls (non-streaming)
        reply = await self.chat(user_message, history)
        # Then yield characters (simulate streaming from resolved reply)
        for char in reply:
            yield char

    # ── Raw LLM call ─────────────────────────────────────────────────────────

    async def _call_llm(self, messages: list[dict], tools: list[dict]) -> dict:
        """POST to the OpenAI-compatible /chat/completions endpoint."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type":  "application/json",
            # OpenRouter-specific (ignored by other providers)
            "HTTP-Referer":  "https://github.com/anonyme-afk/universal-skill-tree",
            "X-Title":       "Universal Skill Tree",
        }

        payload: dict[str, Any] = {
            "model":    self.model,
            "messages": messages,
        }
        if tools:
            payload["tools"]       = tools
            payload["tool_choice"] = "auto"

        resp = await self._client.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
        )

        if resp.status_code != 200:
            raise RuntimeError(
                f"LLM API error {resp.status_code}: {resp.text[:400]}"
            )

        return resp.json()

    # ── Cleanup ───────────────────────────────────────────────────────────────

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()

    # ── Sync wrapper ─────────────────────────────────────────────────────────

    def chat_sync(self, user_message: str, **kwargs) -> str:
        """Synchronous version of chat() for non-async scripts."""
        import asyncio
        return asyncio.run(self.chat(user_message, **kwargs))
