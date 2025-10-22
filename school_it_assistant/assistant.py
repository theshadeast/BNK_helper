"""Rendering logic for support responses."""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from .data import (
    DEFAULT_DETAILS_PROMPT,
    KNOWLEDGE_BASE,
)


@dataclass(frozen=True)
class ResponseEntry:
    """Normalized structure describing a support response."""

    title: str
    steps: Sequence[str]
    commands: Sequence[str]
    escalate_text: str | None
    needs_details: bool
    details_prompt: str


class SupportAssistant:
    """Formats predefined responses for the school IT help desk."""

    def __init__(
        self,
        knowledge_base: Mapping[str, Mapping[str, object]] | None = None,
        *,
        greeting: str = "Здравствуйте!",
    ) -> None:
        self._knowledge_base = knowledge_base or KNOWLEDGE_BASE
        self._greeting = greeting

    def available_topics(self) -> tuple[str, ...]:
        """Return a tuple with available topic identifiers."""

        return tuple(self._knowledge_base.keys())

    def topics_with_titles(self) -> tuple[tuple[str, str], ...]:
        """Return pairs of topic identifiers and human friendly titles."""

        result: list[tuple[str, str]] = []
        for key, raw_entry in self._knowledge_base.items():
            title = str(raw_entry.get("title", key)) if isinstance(raw_entry, Mapping) else key
            result.append((key, title))
        return tuple(result)

    def respond(
        self,
        topic: str,
        *,
        details: str | None = None,
        include_escalation: bool = True,
    ) -> str:
        """Return a formatted response for the given topic."""

        entry_data = self._knowledge_base.get(topic)
        if entry_data is None:
            return self._render_unknown()

        entry = self._normalize_entry(entry_data)
        if entry.needs_details and not details:
            return self._render_details_request(entry)

        return self._render_entry(entry, details=details, include_escalation=include_escalation)

    def _normalize_entry(self, raw_entry: Mapping[str, object]) -> ResponseEntry:
        steps = tuple(str(item) for item in raw_entry.get("steps", ()) if item)
        commands = tuple(str(item) for item in raw_entry.get("commands", ()))
        title = str(raw_entry.get("title", ""))
        escalate_text = raw_entry.get("escalate_text")
        needs_details = bool(raw_entry.get("needs_details", False))
        details_prompt = str(
            raw_entry.get("details_prompt", DEFAULT_DETAILS_PROMPT)
        )
        return ResponseEntry(
            title=title,
            steps=steps,
            commands=commands,
            escalate_text=str(escalate_text) if escalate_text else None,
            needs_details=needs_details,
            details_prompt=details_prompt,
        )

    def _render_entry(
        self,
        entry: ResponseEntry,
        *,
        details: str | None,
        include_escalation: bool,
    ) -> str:
        lines: list[str] = [self._greeting, ""]
        for index, raw_step in enumerate(entry.steps, start=1):
            step = raw_step.format(details=details or "")
            lines.append(f"{index}. {step}")

        for command in entry.commands:
            lines.extend(["", "```", command, "```"])

        if include_escalation and entry.escalate_text:
            lines.extend(["", entry.escalate_text])

        return "\n".join(lines)

    def _render_unknown(self) -> str:
        return "\n".join(
            [
                self._greeting,
                "",
                "1. Уточните, пожалуйста, что именно требуется, кабинет и номер компьютера — помогу оформить заявку.",
            ]
        )

    def _render_details_request(self, entry: ResponseEntry) -> str:
        return "\n".join(
            [
                self._greeting,
                "",
                f"1. {entry.details_prompt}",
            ]
        )


__all__ = ["SupportAssistant"]
