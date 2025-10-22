# School IT Assistant

Telegram-based helper for teachers and staff.

## Overview

This repository contains a small knowledge base and formatter that generate
готовые ответы для школьной службы поддержки. Ответы уже настроены по требуемому
формату: приветствие, шаги диагностики, команды и уточнение данных.

## Usage

The assistant can be used from the command line:

```bash
python -m school_it_assistant.cli list
python -m school_it_assistant.cli printer_connection
python -m school_it_assistant.cli tech_request --details "Иванова, кабинет 204"
```

Each ответ включает шаги для Windows 10/11, Android и iOS там, где это актуально.
Если готового сценария нет, ассистент попросит уточнить проблему и подсказать
данные для оформления заявки.

## Tests

Run the automated checks with:

```bash
pytest
```
