---
name: Project_Structure_Creation
description: "Короткий запрос-руководство для агента: создать базовую структуру проекта"
agent: agent
---
## Задача
- Создать базовую структуру нового Python-проекта по образцу.

## Требуемая структура
- `AppData/`
- `logs/`
- `tests/`
- `config/`
  - `settings.json`  # файл настроек (пустой JSON)
  - `env.example`    # пример переменных окружения (в `config/`)
- `scripts/`
- `modules/`
  - `appconfig/`  # включить короткий `README.md` с универсальными инструкциями (как использовать `get_config()`)
  - `core/`       # включить короткий `README.md` с указанием инициализации сервисов через `AppServices`
  - `logger/`     # включить короткий `README.md` про инициализацию логгера и правила логирования (без специальных функций)
  - `utils/`
- `main.py`        # минимальный точка входа
- `conftest.py`    # минимальный файл для pytest

## Инструкции для агента
- Создать перечислённые директории и файлы.
- В `config/settings.json` поместить `{}` как шаблон.
- В `config/env.example` добавить пример.
- В `modules/appconfig/README.md` указать подробности:
  - **Назначение:** централизованная загрузка конфигурации приложения.
  - **Как использовать:** импортировать `get_config` и вызывать `config = get_config()` в `__init__` сервисов.
  - **Правила:** хранить настройки в `config/settings.json`, секреты в `.env`; не читать файлы напрямую; добавлять новые параметры в `settings.json` и описывать их в `modules/appconfig/config.py` как `@dataclass`.
  - **Пример:**
    ```python
    from modules.appconfig import get_config

    class MyService:
        def __init__(self):
            self._config = get_config()
            self.timeout = self._config.my_module.api_timeout
    ```

- В `modules/core/README.md` указать подробности:
  - **Назначение:** контейнер инициализации критичных сервисов приложения (`AppServices`).
  - **Правило:** инициировать критичные, часто используемые сервисы через `AppServices` при старте; редкие сервисы — создавать локально по требованию.
  - **Запрещено:** инициализировать тяжёлые внешние клиенты при импорте модулей; не хранить глобальный mutable state вне `AppServices`.
  - **Пример:**
    ```python
    from modules.core.app_services import AppServices

    services = AppServices(config=get_config())
    db = services.database
    ```

- В `modules/logger/README.md` указать подробности:
  - **Назначение:** единая инициализация и правила использования логгера.
  - **Как инициализировать:** `logger = get_logger(__name__)` в каждом модуле.
  - **Правила логирования:** логировать только на русском; маскировать или не логировать секреты; использовать f-строки; не применять `print()` для трассировки.
  - **Уровни:** `debug`, `info`, `warning`, `error`, `critical`, `exception` (в блоках try/except).
  - **Пример:**
    ```python
    from modules.logger import get_logger

    logger = get_logger(__name__)
    try:
        do_work()
    except Exception as e:
        logger.exception(f"Ошибка выполнения задачи: {e}")
    ```
- Создать пустые `__init__.py` там, где это уместно.
- Быть кратким и придерживаться русского языка.
