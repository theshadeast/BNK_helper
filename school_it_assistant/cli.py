"""Command line interface for the school IT support assistant."""
from __future__ import annotations

import argparse
from typing import Iterable

from .assistant import SupportAssistant


def build_parser(topics: Iterable[str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Сформировать подсказку для учителей и сотрудников школы по типовой ИТ-задаче."
        )
    )
    parser.add_argument(
        "topic",
        help="идентификатор темы или 'list' для отображения всех вариантов",
    )
    parser.add_argument(
        "--details",
        help="уточнения для обращения (кабинет, компьютер, имя)",
    )
    parser.add_argument(
        "--no-escalation",
        action="store_true",
        help="не добавлять напоминание о заявке",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    assistant = SupportAssistant()
    parser = build_parser(assistant.available_topics())
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.topic == "list":
        for key, title in assistant.topics_with_titles():
            print(f"{key} — {title}")
        return 0

    response = assistant.respond(
        args.topic,
        details=args.details,
        include_escalation=not args.no_escalation,
    )
    print(response)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
