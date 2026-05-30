"""
ust.core.gemini_adapter
───────────────────────
Native Google Gemini adapter for UST.

Supports:
  - google-genai SDK (new, recommended)
  - Gemini 1.5 Flash / Pro / 2.0 Flash

Connects your existing JARVIS to the UST skill tree.

Usage:
    from ust import enable_branch
    from ust.core.gemini_adapter import GeminiAdapter

    enable_branch("system")
    agent = GeminiAdapter(api_key="AIza...")
    reply = agent.chat_sync("Open Chrome")
"""
from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from .executor import Executor, ToolResult
from .registry import get_registry


DEFAULT_MODEL = "gemini-2.0-flash"


class GeminiAdapter:
    """
    Native Gemini adapter using the google-genai SDK.

    Converts UST skill declarations → Gemini FunctionDeclaration format,
    then handles the full tool-call loop.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        system_prompt: str = (
            "You are a helpful AI assistant with full access to the user's computer. "
            "Always use the provided tools to complete tasks — never simulate results."
        ),
        max_iterations: int = 10,
    ):
        self.api_key    = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model      = model
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self._executor  = Executor()
        self._registry  = get_registry()

        if not self.api_key:
            raise ValueError(
                "Gemini API key required. Set GEMINI_API_KEY env var "
                "or pass api_key= to GeminiAdapter()."
            )

    # ── Conversion helpers ────────────────────────────────────────────────────

    def _ust_to_gemini_tools(self, branch: str | None = None) -> list[dict]:
        """Convert UST declarations to Gemini's tool format."""
        try:
            from google.genai import types as gtypes
        except ImportError:
            raise ImportError(
                "Install google-genai: pip install google-genai"
            )

        declarations = self._registry.declarations(branch)
        gemini_tools = []

        for decl in declarations:
            fn = decl["function"]
            params = fn.get("parameters", {})

            # Build Gemini Schema
            properties = {}
            for prop_name, prop_schema in params.get("properties", {}).items():
                properties[prop_name] = self._convert_schema(prop_schema)

            func_decl = gtypes.FunctionDeclaration(
                name=fn["name"],
                description=fn["description"],
                parameters=gtypes.Schema(
                    type=gtypes.Type.OBJECT,
                    properties=properties,
                    required=params.get("required", []),
                ),
            )
            gemini_tools.append(func_decl)

        return [gtypes.Tool(function_declarations=gemini_tools)] if gemini_tools else []

    def _convert_schema(self, schema: dict):
        """Recursively convert JSON Schema to Gemini Schema."""
        try:
            from google.genai import types as gtypes
        except ImportError:
            return schema

        type_map = {
            "string":  gtypes.Type.STRING,
            "integer": gtypes.Type.INTEGER,
            "number":  gtypes.Type.NUMBER,
            "boolean": gtypes.Type.BOOLEAN,
            "array":   gtypes.Type.ARRAY,
            "object":  gtypes.Type.OBJECT,
        }

        schema_type = type_map.get(schema.get("type", "string"), gtypes.Type.STRING)
        kwargs: dict[str, Any] = {"type": schema_type}

        if "description" in schema:
            kwargs["description"] = schema["description"]
        if "enum" in schema:
            kwargs["enum"] = schema["enum"]

        return gtypes.Schema(**kwargs)

    # ── Main chat ─────────────────────────────────────────────────────────────

    async def chat(
        self,
        user_message: str,
        history: list[dict] | None = None,
        branch: str | None = None,
    ) -> str:
        try:
            from google import genai
            from google.genai import types as gtypes
        except ImportError:
            return "ERROR: Install google-genai — pip install google-genai"

        client = genai.Client(api_key=self.api_key)
        tools  = self._ust_to_gemini_tools(branch)

        # Build history in Gemini format
        gemini_history = []
        if history:
            for msg in history:
                role = "user" if msg["role"] == "user" else "model"
                gemini_history.append(
                    gtypes.Content(role=role, parts=[gtypes.Part.from_text(msg["content"])])
                )

        # Chat session config
        config = gtypes.GenerateContentConfig(
            system_instruction=self.system_prompt,
            tools=tools if tools else None,
        )

        contents = gemini_history + [
            gtypes.Content(role="user", parts=[gtypes.Part.from_text(user_message)])
        ]

        for _ in range(self.max_iterations):
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda c=contents: client.models.generate_content(
                    model=self.model,
                    contents=c,
                    config=config,
                )
            )

            candidate = response.candidates[0]
            part = candidate.content.parts[0] if candidate.content.parts else None

            # No tool calls → final text
            if not part or not hasattr(part, "function_call") or not part.function_call:
                return response.text or ""

            # Execute tool call
            fc = part.function_call
            tool_call = {
                "id": fc.name,
                "function": {
                    "name": fc.name,
                    "arguments": json.dumps(dict(fc.args)),
                }
            }
            result: ToolResult = await self._executor.run(tool_call)
            print(f"[UST/Gemini] {'✅' if result.success else '❌'} {result.name}: {str(result.output)[:120]}")

            # Append assistant turn + tool result to history
            contents.append(candidate.content)
            contents.append(gtypes.Content(
                role="user",
                parts=[gtypes.Part.from_function_response(
                    name=fc.name,
                    response={"result": str(result.output)},
                )]
            ))

        return "Max iterations reached."

    def chat_sync(self, user_message: str, **kwargs) -> str:
        return asyncio.run(self.chat(user_message, **kwargs))

    async def close(self):
        pass  # No persistent client to close

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        pass
