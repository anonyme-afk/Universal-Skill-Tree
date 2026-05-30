"""
ust.core.registry
─────────────────
Central registry for all UST skills.

A "skill" = a Python function + its OpenAI-compatible tool declaration.
The registry is the single source of truth: adapters read from it,
the executor dispatches to it.
"""
from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable


# ─── Data structures ──────────────────────────────────────────────────────────

@dataclass
class Skill:
    """A registered skill: function + its LLM tool declaration."""
    name: str
    branch: str                         # e.g. "system", "web", "files"
    fn: Callable                        # The actual Python function
    declaration: dict                   # OpenAI-compatible tool schema
    enabled: bool = True
    requires_confirmation: bool = False

    def __repr__(self) -> str:
        status = "✅" if self.enabled else "❌"
        return f"<Skill {status} [{self.branch}] {self.name}>"


@dataclass
class SkillRegistry:
    """
    Singleton-like registry holding all registered skills.
    Branches are lazy: skills are only registered when a branch is loaded.
    """
    _skills: dict[str, Skill] = field(default_factory=dict)

    # ── Registration ──────────────────────────────────────────────────────────

    def register(self, skill: Skill) -> None:
        """Add a skill to the registry."""
        if skill.name in self._skills:
            import logging
            logging.getLogger("ust").debug(f"Skill '{skill.name}' is already registered. Overwriting with the latest version.")
        self._skills[skill.name] = skill

    def register_many(self, skills: list[Skill]) -> None:
        for s in skills:
            self.register(s)

    # ── Lookup ────────────────────────────────────────────────────────────────

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name)

    def get_or_raise(self, name: str) -> Skill:
        s = self._skills.get(name)
        if s is None:
            raise KeyError(f"Unknown skill: '{name}'. Is the branch loaded?")
        return s

    def branch(self, branch_name: str) -> list[Skill]:
        """Return all skills belonging to a branch."""
        res = []
        for s in self._skills.values():
            if s.branch == branch_name:
                res.append(s)
            elif s.name == "screenshot" and branch_name in ("system", "vision") and s not in res:
                res.append(s)
        return res

    def all_enabled(self) -> list[Skill]:
        return [s for s in self._skills.values() if s.enabled]

    def all_branches(self) -> set[str]:
        return {s.branch for s in self._skills.values()}

    # ── Tool declarations (what you send to the LLM) ─────────────────────────

    def declarations(self, branch: str | None = None) -> list[dict]:
        """
        Return OpenAI-compatible tool declarations.
        Pass branch='system' to get only system skills, or None for all enabled.
        """
        skills = self.branch(branch) if branch else self.all_enabled()
        return [
            {"type": "function", "function": s.declaration}
            for s in skills
            if s.enabled
        ]

    # ── Enable / Disable ─────────────────────────────────────────────────────

    def enable(self, name: str) -> None:
        self.get_or_raise(name).enabled = True

    def disable(self, name: str) -> None:
        self.get_or_raise(name).enabled = False

    def disable_branch(self, branch_name: str) -> None:
        for s in self.branch(branch_name):
            s.enabled = False

    # ── Debug ─────────────────────────────────────────────────────────────────

    def summary(self) -> str:
        lines = ["── UST Skill Registry ──────────────────"]
        for branch_name in sorted(self.all_branches()):
            skills = self.branch(branch_name)
            enabled = sum(1 for s in skills if s.enabled)
            lines.append(f"  [{branch_name}]  {enabled}/{len(skills)} skills active")
            for s in skills:
                mark = "✅" if s.enabled else "  "
                lines.append(f"    {mark} {s.name}")
        lines.append("────────────────────────────────────────")
        return "\n".join(lines)


# ─── Global singleton ─────────────────────────────────────────────────────────

_registry = SkillRegistry()


def get_registry() -> SkillRegistry:
    """Get the global skill registry."""
    return _registry


# ─── Decorator helper ─────────────────────────────────────────────────────────

def skill(
    name: str,
    branch: str,
    description: str,
    parameters: dict,
    requires_confirmation: bool = False,
) -> Callable:
    """
    Decorator to register a function as a UST skill.

    Usage:
        @skill(
            name="run_command",
            branch="system",
            description="Run a shell command.",
            parameters={...},  # JSON Schema
            requires_confirmation=True
        )
        def run_command(command: str) -> str:
            ...
    """
    def decorator(fn: Callable) -> Callable:
        declaration = {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                **parameters,
            },
        }
        _registry.register(Skill(
            name=name,
            branch=branch,
            fn=fn,
            declaration=declaration,
            requires_confirmation=requires_confirmation,
        ))
        return fn
    return decorator
