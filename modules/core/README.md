Назначение: контейнер инициализации критичных сервисов приложения (`AppServices`).

Правило:

- Инициализировать критичные, часто используемые сервисы через `AppServices` при старте приложения.
- Редкие или тяжёлые сервисы — создавать локально по требованию.
- Не инициализировать тяжёлые внешние клиенты при импорте модулей.
- Не хранить глобальный изменяемый (`mutable`) state вне `AppServices`.

Пример:

```python
from modules.core.app_services import AppServices
from modules.appconfig import get_config

services = AppServices(config=get_config())
db = services.database
```
