# Проект-шаблон

Этот репозиторий — шаблон для старта новых Python-проектов. Включает базовую структуру модулей, конфигурацию, логгер и инструкции по работе в Windows.

## Ключевые возможности

- **Структура:** шаблон модулей и точек входа для быстрого старта.
- **Конфигурация:** централизованная загрузка конфигурации через `modules.appconfig.get_config()`.
- **Логгер:** готовая конфигурация логирования в `modules/logger`.
- **Агенты программирования:** дополнительные агенты для автоматизации задач и взаимодействия с кодом `.github/agents`.
- **Инструкции:** встроенные правила и вспомогательные файлы для агентов программирования GitHub Copilot `.github/instructions` и Google Antigravity `.agent/rules`.
- **Скиллы:** встроенные скиллы для агентов программирования GitHub Copilot `.github/skills`, включают работу с `openai-responses-api` и `telegram-aiogram`.

## Конфигурация и секреты

- **Настройки:** храните параметры в [config/settings.json](config/settings.json).
- **Секреты:** используйте `config/.env` (копируйте от [config/env.example](config/env.example)).
- **Получение конфигурации:** всегда загружайте настройки через `from modules.appconfig import get_config` и `config = get_config()` (см. [modules/appconfig](modules/appconfig/)).

Это правило — обязательная часть шаблона: не хардкодьте параметры в коде.

## Логирование

- Инициализируйте логгер через `modules.logger.get_logger(__name__)`.
- Логируйте сообщения на русском языке и не выводите секреты.
- Уровни логирования: `debug`, `info`, `warning`, `error`, `critical`, `exception`.

Пример использования конфигурации и логгера в коде:

```python
from modules.appconfig import get_config
from modules.logger import get_logger

logger = get_logger(__name__)

class MyService:
    def __init__(self):
        self._config = get_config()
        self._timeout = self._config.my_module.api_timeout

    def run(self):
        logger.info(f"Запуск сервиса: timeout={self._timeout}")
        return self._timeout
```

## Структура проекта (ключевые файлы)

- [main.py](main.py) — точка входа.
- [config/settings.json](config/settings.json) — настройки приложения.
- [config/env.example](config/env.example) — пример файла секретов.
- [modules/appconfig/](modules/appconfig/) — загрузка конфигурации (`get_config`).
- [modules/core/app_services.py](modules/core/app_services.py) — контейнер сервисов приложения.
- [modules/logger/](modules/logger/) — модуль логирования.
- [tests/](tests/) — тесты проекта.

## Рекомендации разработчику

- Всегда загружайте конфигурацию один раз в конструкторе класса.
- Не логируйте секреты и не используйте `print()` для трейсинга.
- Перед запуском тестов включайте UTF-8 в PowerShell (см. блок выше).

## Работа с агентами программирования

- **Инструкции**
- **Project_Description:** [.github/instructions/Project_Description.instructions.md](.github/instructions/Project_Description.instructions.md)
- **Project_Documentation:** [.github/instructions/Project_Documentation.instructions.md](.github/instructions/Project_Documentation.instructions.md)
- **OpenAI_ResponsesAPI:** [.github/instructions/OpenAI_ResponsesAPI.instructions.md](.github/instructions/OpenAI_ResponsesAPI.instructions.md)
- **OOP_Standard:** [.github/instructions/OOP_Standard.instructions.md](.github/instructions/OOP_Standard.instructions.md)
- **Logger_usage:** [.github/instructions/Logger_usage.instructions.md](.github/instructions/Logger_usage.instructions.md)
- **Project_python_interpreter:** [.github/instructions/Project_python_interpreter.instructions.md](.github/instructions/Project_python_interpreter.instructions.md)
- **Service_Initialization:** [.github/instructions/Service_Initialization.instructions.md](.github/instructions/Service_Initialization.instructions.md)
- **Project_structure:** [.github/instructions/Project_structure.instructions.md](.github/instructions/Project_structure.instructions.md)
- **Instructions (общие правила):** [.github/instructions/Instructions.instructions.md](.github/instructions/Instructions.instructions.md)
- **Environment_Activated_Reminder:** [.github/instructions/Environment_Activated_Reminder.instructions.md](.github/instructions/Environment_Activated_Reminder.instructions.md)
- **converter (MD↔JSON):** [.github/instructions/converter.instructions.md](.github/instructions/converter.instructions.md)
- **Configuration_Usage_Rules:** [.github/instructions/Configuration_Usage_Rules.instructions.md](.github/instructions/Configuration_Usage_Rules.instructions.md)
- **Tests_Terminal_Commands:** [.github/instructions/Tests_Terminal_Commands.instructions.md](.github/instructions/Tests_Terminal_Commands.instructions.md)
- **Terminal_Tools:** [.github/instructions/Terminal_Tools.instructions.md](.github/instructions/Terminal_Tools.instructions.md)

- **Prompts:**
- **Project_Structure_Creation:** [.github/prompts/Project_Structure_Creation.prompt.md](.github/prompts/Project_Structure_Creation.prompt.md)
- **Planning:** [.github/prompts/Planning.prompt.md](.github/prompts/Planning.prompt.md)
- **MD Generation Guidelines:** [.github/prompts/MD%20Generation%20Guidelines.prompt.md](.github/prompts/MD%20Generation%20Guidelines.prompt.md)
- **Instructions.prompt:** [.github/prompts/Instructions.prompt.md](.github/prompts/Instructions.prompt.md)
- **Implementation:** [.github/prompts/Implementation.prompt.md](.github/prompts/Implementation.prompt.md)
- **Analyze Project:** [.github/prompts/Analyze%20Project.prompt.md](.github/prompts/Analyze%20Project.prompt.md)

- **Агенты:**
- **Planning Agent:** [.github/agents/Planning%20Agent.agent.md](.github/agents/Planning%20Agent.agent.md)
- **Analyze Project Agent:** [.github/agents/Analyze%20Project.agent.md](.github/agents/Analyze%20Project.agent.md)

- **Скиллы:**
- **telegram-aiogram:** [.github/skills/telegram-aiogram/SKILL.md](.github/skills/telegram-aiogram/SKILL.md)
- **openai-responses-api:** [.github/skills/openai-responses-api/SKILL.md](.github/skills/openai-responses-api/SKILL.md)
