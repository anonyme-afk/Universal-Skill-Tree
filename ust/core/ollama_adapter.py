"""
ust.core.ollama_adapter
───────────────────────
Native Ollama adapter. Supports local models cleanly via the 'ollama' python package.

Usage:
    from ust import enable_branch
    from ust.core.ollama_adapter import OllamaAdapter

    enable_branch("system")
    agent = OllamaAdapter(model="llama3.1")
    reply = agent.chat_sync("Look up the system memory usage")
"""
from __future__ import annotations

import asyncio
import json
from typing import Any

from .executor import Executor, ToolResult
from .registry import get_registry

class OllamaAdapter:
    """
    Adapter for the official `ollama` Python SDK.
    Note: Tool calling requires an Ollama model that supports it (like llama3.1, mistral).
    """

    def __init__(
        self,
        model: str = "llama3.1",
        system_prompt: str = "You are a helpful AI assistant with access to tools. Always use the provided tools.",
        max_iterations: int = 10,
        host: str | None = None,
    ):
        self.model = model
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.host = host
        
        self._executor = Executor()
        self._registry = get_registry()

    def _ust_to_ollama_tools(self, branch: str | None = None) -> list[dict]:
        """Ollama supports exactly the OpenAI tool schema."""
        return self._registry.declarations(branch)

    async def chat(
        self,
        user_message: str,
        history: list[dict] | None = None,
        branch: str | None = None,
    ) -> str:
        try:
            from ollama import AsyncClient
        except ImportError:
            return "ERROR: Install ollama — pip install ollama"

        client = AsyncClient(host=self.host)
        
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        tools = self._ust_to_ollama_tools(branch)

        for iteration in range(self.max_iterations):
            response = await client.chat(
                model=self.model,
                messages=messages,
                tools=tools if tools else None
            )

            message = response.get("message", {})

            if not message.get("tool_calls"):
                return message.get("content") or ""

            # Standardize message format to append
            assistant_message = {
                "role": "assistant",
                "content": message.get("content", ""),
                "tool_calls": message.get("tool_calls", [])
            }
            messages.append(assistant_message)

            tool_calls = message.get("tool_calls", [])
            results: list[ToolResult] = []
            
            # Ollama sdk parses arguments straight as dict. Let's fix up tool_call objects for the executor
            # Executor expects {"function": {"name": ..., "arguments": "{...}"}, "id": "..."}
            formatted_tool_calls = []
            for tc in tool_calls:
                func = tc.get("function", {})
                args = func.get("arguments", {})
                # Stringify args if it's a dict (expected by executor)
                str_args = json.dumps(args) if isinstance(args, dict) else args
                formatted_tool_calls.append({
                    "id": tc.get("id", "call_ollama"),
                    "function": {"name": func.get("name"), "arguments": str_args}
                })

            results = await self._executor.run_all(formatted_tool_calls)

            for r in results:
                status = "✅" if r.success else "❌"
                preview = str(r.output)[:120].replace('\n', ' ')
                print(f"[UST/Ollama] {status} {r.name}: {preview}")

            messages.extend(r.to_message() for r in results)

        return "Max iterations reached."

    def chat_sync(self, user_message: str, **kwargs) -> str:
        import asyncio
        return asyncio.run(self.chat(user_message, **kwargs))
