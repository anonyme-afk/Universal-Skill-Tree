"""
ust.core.litellm_adapter
────────────────────────
Native LiteLLM adapter. Supports over 100+ LLMs (Anthropic, Gemini, OpenAI,
Ollama, vLLM, Bedrock, etc) through a standard standard interface.

Usage:
    from ust import enable_branch
    from ust.core.litellm_adapter import LiteLLMAdapter

    enable_branch("system")
    # Using Anthropic
    agent = LiteLLMAdapter(model="claude-3-5-sonnet-20240620", api_key="sk-ant-...")
    
    # Using local Ollama
    agent_local = LiteLLMAdapter(model="ollama/llama3")
    
    reply = agent.chat_sync("Check my battery percentage")
"""
from __future__ import annotations

import asyncio
import json
import os
from typing import Any, AsyncIterator

from .executor import Executor, ToolResult
from .registry import get_registry

class LiteLLMAdapter:
    """
    Adapter using the 'litellm' Python package directly.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: str | None = None,
        base_url: str | None = None,
        system_prompt: str = "You are a helpful AI assistant with access to tools. Always use the provided tools to complete tasks — never simulate results.",
        max_iterations: int = 10,
        **litellm_kwargs
    ):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.litellm_kwargs = litellm_kwargs
        
        self._executor = Executor()
        self._registry = get_registry()

    def _ust_to_litellm_tools(self, branch: str | None = None) -> list[dict]:
        """LiteLLM uses the exact same tool schema as OpenAI."""
        declarations = self._registry.declarations(branch)
        tools = []
        for decl in declarations:
            # decl is already formatted like an OpenAI function payload: 
            # {"type": "function", "function": {"name": ..., "description": ..., "parameters": ...}}
            # Actually wait, registry.declarations() returns {"type": "function", "function": ...} in adapter.py?
            # Let's check: Yes, adapter.py uses it straight.
            tools.append(decl)
        return tools

    async def chat(
        self,
        user_message: str,
        history: list[dict] | None = None,
        branch: str | None = None,
    ) -> str:
        """
        Send a message and get the final answer after all tool calls are resolved.
        """
        try:
            from litellm import acompletion
        except ImportError:
            return "ERROR: Install litellm — pip install litellm"

        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        tools = self._ust_to_litellm_tools(branch)

        kwargs = self.litellm_kwargs.copy()
        if self.api_key:
            kwargs["api_key"] = self.api_key
        if self.base_url:
            kwargs["base_url"] = self.base_url

        for iteration in range(self.max_iterations):
            if tools:
                response = await acompletion(
                    model=self.model,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    **kwargs
                )
            else:
                response = await acompletion(
                    model=self.model,
                    messages=messages,
                    **kwargs
                )

            choice = response.choices[0]
            message = choice.message
            
            # Message is a Pydantic object usually or dict. Convert to dict for safety.
            msg_dict = message.model_dump() if hasattr(message, "model_dump") else dict(message)

            if not msg_dict.get("tool_calls"):
                return msg_dict.get("content") or ""

            # We need to append the exact assistant message containing the tool calls
            messages.append(msg_dict)

            # Execute all tool calls
            tool_calls = msg_dict.get("tool_calls", [])
            results: list[ToolResult] = await self._executor.run_all(tool_calls)

            # Log results
            for r in results:
                status = "✅" if r.success else "❌"
                preview = str(r.output)[:120].replace('\n', ' ')
                print(f"[UST/LiteLLM] {status} {r.name}: {preview}")

            # Append tool results to messages
            messages.extend(r.to_message() for r in results)

        return "Max iterations reached. Last known state saved."

    def chat_sync(self, user_message: str, **kwargs) -> str:
        import asyncio
        return asyncio.run(self.chat(user_message, **kwargs))

    async def close(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        pass
