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

    # ── Streaming chat (Simulated & Real) ──────────────────────────────────────────────────

    async def fake_stream(
        self,
        user_message: str,
        history: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        """
        Simulate streaming the response character by character.
        NOTE: This does NOT stream directly from the LLM. It fully resolves
        all tool calls and the final API response first, then yields characters
        to simulate a stream without utilizing HTTP streaming (SSE).
        """
        reply = await self.chat(user_message, history)
        for char in reply:
            import asyncio
            await asyncio.sleep(0.01)
            yield char

    async def stream(
        self,
        user_message: str,
        history: list[dict] | None = None,
        branch: str | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream the final response token by token in real-time.
        Tool calls are dynamically parsed and executed silently before the final text streams.
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        tools = self._registry.declarations(branch)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type":  "application/json",
            "HTTP-Referer":  "https://github.com/anonyme-afk/universal-skill-tree",
            "X-Title":       "Universal Skill Tree",
        }

        for iteration in range(self.max_iterations):
            payload: dict[str, Any] = {
                "model":    self.model,
                "messages": messages,
                "stream":   True,
            }
            if tools:
                payload["tools"]       = tools
                payload["tool_choice"] = "auto"

            tool_calls_accumulator = {}
            content_accumulator = []

            try:
                async with self._client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                ) as response:
                    if response.status_code != 200:
                        text = await response.aread()
                        raise RuntimeError(f"LLM API error {response.status_code}: {text[:400].decode('utf-8', errors='ignore')}")

                    async for line in response.aiter_lines():
                        line = line.strip()
                        if not line:
                            continue
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                choices = data.get("choices", [])
                                if not choices:
                                    continue
                                choice = choices[0]
                                delta = choice.get("delta", {})

                                # Parse tool calls delta
                                if "tool_calls" in delta:
                                    for tc in delta["tool_calls"]:
                                        idx = tc.get("index", 0)
                                        if idx not in tool_calls_accumulator:
                                            tool_calls_accumulator[idx] = {
                                                "id": tc.get("id", ""),
                                                "type": "function",
                                                "function": {
                                                    "name": tc.get("function", {}).get("name", "") or "",
                                                    "arguments": tc.get("function", {}).get("arguments", "") or ""
                                                }
                                            }
                                        else:
                                            item = tool_calls_accumulator[idx]
                                            if tc.get("id"):
                                                item["id"] = tc.get("id")
                                            if "function" in tc:
                                                f_delta = tc["function"]
                                                if f_delta.get("name"):
                                                    item["function"]["name"] += f_delta["name"]
                                                if f_delta.get("arguments"):
                                                    item["function"]["arguments"] += f_delta["arguments"]

                                # Parse text content delta
                                if "content" in delta and delta["content"]:
                                    content_piece = delta["content"]
                                    content_accumulator.append(content_piece)
                                    # Yield text only if LLM is not generating a tool call in this turn
                                    if not tool_calls_accumulator:
                                        yield content_piece
                            except json.JSONDecodeError:
                                continue
            except Exception as e:
                import logging
                logging.getLogger("ust").error(f"Error during streaming request: {e}")
                raise e

            if tool_calls_accumulator:
                # Resolve accumulated tool calls
                tool_calls = list(tool_calls_accumulator.values())
                assistant_message = {
                    "role": "assistant",
                    "content": "".join(content_accumulator) if content_accumulator else None,
                    "tool_calls": tool_calls
                }
                messages.append(assistant_message)

                results = await self._executor.run_all(tool_calls)
                for r in results:
                    status = "✅" if r.success else "❌"
                    import logging
                    logging.getLogger("ust").info(f"{status} {r.name}: {str(r.output)[:120]}")
                messages.extend(r.to_message() for r in results)
            else:
                # No more tool calls: final text response is fully streamed!
                final_content = "".join(content_accumulator)
                messages.append({"role": "assistant", "content": final_content})
                break

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
            
        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries):
            try:
                resp = await self._client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )

                if resp.status_code in (429, 500, 502, 503, 504):
                    delay = base_delay * (2 ** attempt)
                    import logging
                    logging.getLogger("ust").warning(f"⚠️ API Error {resp.status_code}. Retrying in {delay}s...")
                    import asyncio
                    await asyncio.sleep(delay)
                    continue

                if resp.status_code != 200:
                    raise RuntimeError(
                        f"LLM API error {resp.status_code}: {resp.text[:400]}"
                    )

                return resp.json()
            except Exception as e:
                import httpx
                if isinstance(e, httpx.RequestError):
                    delay = base_delay * (2 ** attempt)
                    import logging
                    logging.getLogger("ust").warning(f"⚠️ Network Error {e}. Retrying in {delay}s...")
                    import asyncio
                    await asyncio.sleep(delay)
                    continue
                raise
                
        # Fallback if loops exhaust without returning or raising proper context
        raise RuntimeError("Max retries exceeded while calling LLM API")

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
