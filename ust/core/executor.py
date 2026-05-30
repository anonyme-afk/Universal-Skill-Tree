"""
ust.core.executor
─────────────────
Receives a tool_call from the LLM response and dispatches
it to the right skill function.

Works synchronously and asynchronously.
"""
from __future__ import annotations

import asyncio
import inspect
import json
import traceback
from typing import Any, Callable

from .registry import get_registry


# ─── Result wrapper ───────────────────────────────────────────────────────────

class ToolResult:
    """Wraps the output of a skill execution."""

    def __init__(self, tool_call_id: str, name: str, output: Any, error: str | None = None):
        self.tool_call_id = tool_call_id
        self.name = name
        self.output = output
        self.error = error
        self.success = error is None

    def to_message(self) -> dict:
        """Format as an OpenAI-compatible tool result message."""
        content = self.output if self.success else f"ERROR: {self.error}"
        # Always stringify the content
        if not isinstance(content, str):
            content = json.dumps(content, ensure_ascii=False, default=str)
        return {
            "role": "tool",
            "tool_call_id": self.tool_call_id,
            "content": content,
        }

    def __repr__(self) -> str:
        if self.success:
            preview = str(self.output)[:80]
            return f"<ToolResult ✅ {self.name}: {preview}>"
        return f"<ToolResult ❌ {self.name}: {self.error}>"


# ─── Executor ─────────────────────────────────────────────────────────────────

class Executor:
    """
    Dispatches LLM tool_calls to registered UST skills.

    Usage:
        executor = Executor()
        results = await executor.run_all(response.choices[0].message.tool_calls)
        messages += [r.to_message() for r in results]
    """

    def __init__(self):
        self._registry = get_registry()
        self._confirmation_handler = None
        
    def set_confirmation_handler(self, handler: Callable[[str, dict], bool]) -> None:
        """
        Set a callback that will be called before executing a skill marked
        with `requires_confirmation=True`.
        If the callback returns False, the skill execution is aborted.
        Callback signature: handler(skill_name: str, args: dict) -> bool
        """
        self._confirmation_handler = handler

    # ── Single call ───────────────────────────────────────────────────────────

    async def run(self, tool_call: Any) -> ToolResult:
        """
        Execute a single tool_call object (OpenAI format).
        Accepts both dict and object forms.
        """
        # Normalize: support dict or object
        if isinstance(tool_call, dict):
            call_id   = tool_call.get("id", "unknown")
            fn_name   = tool_call["function"]["name"]
            raw_args  = tool_call["function"].get("arguments", "{}")
        else:
            call_id   = getattr(tool_call, "id", "unknown")
            fn_name   = tool_call.function.name
            raw_args  = tool_call.function.arguments

        # Parse arguments
        try:
            args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
        except json.JSONDecodeError as e:
            return ToolResult(call_id, fn_name, None, f"Invalid JSON args: {e}")

        # Look up skill
        skill = self._registry.get(fn_name)
        if skill is None:
            return ToolResult(call_id, fn_name, None, f"Unknown skill '{fn_name}'")

        if not skill.enabled:
            return ToolResult(call_id, fn_name, None, f"Skill '{fn_name}' is disabled")
            
        # Hardcoded list of dangerous commands in case requires_confirmation is missing from catalog
        dangerous = {"run_command", "kill_process", "docker_run", "create_dockerfile", "install_package", "git_commit_push"}
        needs_confirm = skill.requires_confirmation or (fn_name in dangerous)
        
        if needs_confirm:
            if self._confirmation_handler:
                if not self._confirmation_handler(fn_name, args):
                    return ToolResult(call_id, fn_name, None, f"Execution aborted by user confirmation handler")
            else:
                import logging
                logging.getLogger("ust").warning(f"⚠️ DANGEROUS SKILL '{fn_name}' RUNNING WITHOUT CONFIRMATION HANDLER!")

        # Execute
        try:
            if asyncio.iscoroutinefunction(skill.fn):
                output = await skill.fn(**args)
            else:
                # Run sync functions in thread pool to avoid blocking
                output = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: skill.fn(**args)
                )
            return ToolResult(call_id, fn_name, output)

        except TypeError as e:
            return ToolResult(call_id, fn_name, None, f"Bad arguments: {e}")
        except Exception as e:
            tb = traceback.format_exc()
            return ToolResult(call_id, fn_name, None, f"{type(e).__name__}: {e}\n{tb}")

    # ── Batch calls ───────────────────────────────────────────────────────────

    async def run_all(self, tool_calls: list[Any]) -> list[ToolResult]:
        """Execute all tool_calls from an LLM response (in parallel)."""
        if not tool_calls:
            return []
        return await asyncio.gather(*[self.run(tc) for tc in tool_calls])

    # ── Sync wrapper (for non-async code) ─────────────────────────────────────

    def run_sync(self, tool_call: Any) -> ToolResult:
        """Synchronous wrapper around run()."""
        return asyncio.run(self.run(tool_call))

    def run_all_sync(self, tool_calls: list[Any]) -> list[ToolResult]:
        """Synchronous wrapper around run_all()."""
        return asyncio.run(self.run_all(tool_calls))
