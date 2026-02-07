---
# applyTo: '**'
name: 'Configuration_Usage_Rules'
description: 'Обязательное использование конфигурации для всех параметров и переменных модулей'
---

## Правила использования конфигурации

### Кратко

- **Модуль конфигурации:** `modules/appconfig/`
- **Модуль инициализации:** `modules/core/`
- **Единственный способ получить конфигурацию:** `from modules.appconfig import get_config` и `config = get_config()`

### ОБЯЗАТЕЛЬНО

- Загружать конфигурацию через `get_config()` из `modules.appconfig` для всех параметров, влияющих на поведение кода.
- Загружать конфигурацию один раз в конструкторе класса.
- Хранить настройки приложения в `config/settings.json`.
- Хранить секреты (токены, ключи) только в `.env`.

### ЗАПРЕЩЕНО

- Хардкодить параметры в коде (таймауты, пороги, пути, режимы работы).
- Читать `config/settings.json` или `.env` напрямую из модулей.
- Создавать константы настроек в модулях вместо конфигурации.

### Добавление нового параметра

- Добавить параметр в `config/settings.json`.
- Описать `@dataclass` для параметров в `modules/appconfig/config.py`.
- Включить новый dataclass в `AppConfig`.
- Экспортировать и использовать через `get_config()`.

### Примеры

Правильный подход — загрузить конфигурацию в `__init__` и сохранять в поле:
```python
from modules.appconfig import get_config
from modules.logger import get_logger

logger = get_logger(__name__)

class MyService:
    def __init__(self):
        self._config = get_config()
        self._timeout = self._config.my_module.api_timeout

    def run(self):
        return self._timeout
```

Неправильно — хардкод в коде:
```python
class MyService:
    TIMEOUT = 30  # Плохо: должно быть в конфигурации

    def run(self):
        return self.TIMEOUT
```
