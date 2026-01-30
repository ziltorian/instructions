Назначение: централизованная загрузка конфигурации приложения.

Как использовать:

- Импортировать `get_config` и вызывать `config = get_config()` в `__init__` сервисов.

Правила:

- Хранить настройки в `config/settings.json`, секреты в `.env`.
- Загружать конфигурацию через `get_config()` один раз в конструкторе класса.
- Не читать `config/settings.json` или `.env` напрямую из модулей.
- При добавлении нового параметра: добавить его в `config/settings.json` и описать в `modules/appconfig/config.py` как `@dataclass`.

Пример:

```python
from modules.appconfig import get_config

class MyService:
    def __init__(self):
        self._config = get_config()
        self.timeout = self._config.my_module.api_timeout
```
