---
name: telegram-aiogram
description: Навык для разработки Telegram ботов с использованием aiogram 3.x. Используй этот навык когда пользователь работает с модулем `modules/telegram` или его подмодулями; упоминает Telegram, бота, aiogram, роутеры (routers), обработчики (handlers); создаёт или изменяет клавиатуры (keyboards), middleware, FSM состояния; пишет тесты для Telegram-функциональности (tests/test_telegram*, tests/test_*bot*); задаёт вопросы о структуре Telegram-бота в проекте; работает с callback_query, message handlers, inline keyboards; упоминает StatesGroup, FSMContext, Router, Dispatcher; спрашивает о групповых чатах, топиках, FSM storage; работает с файлами bot.py, states.py, routers/*.py, keyboards/*.py, middleware/*.py, utils/*.py.
---

# Telegram aiogram 3.x Development Skill

Этот навык предоставляет руководство по разработке Telegram ботов с использованием фреймворка aiogram версии 3.22.0 в проекте MasterBot.

## Версия и совместимость

- **Версия aiogram**: 3.22.0
- **Telegram Bot API**: 9.2
- **Python**: 3.13.9 (async/await)

## Структура модуля `modules/telegram/`

```
modules/telegram/
├── __init__.py           # Экспорт публичного API модуля
├── bot.py                # Класс MasterBot: инициализация и запуск бота
├── states.py             # FSM состояния (StatesGroup)
├── keyboards/            # Клавиатуры (InlineKeyboardMarkup)
│   ├── admin_keyboards.py
│   ├── character_keyboards.py
│   ├── download_keyboards.py
│   └── game_keyboards.py
├── middleware/           # Middleware для авторизации и проверок
│   ├── admin_check.py    # AdminCheckMiddleware
│   └── session_check.py  # SessionCheckMiddleware
├── routers/              # Обработчики событий (Router)
│   ├── admin.py          # Админ-панель
│   ├── character.py      # Создание персонажей
│   ├── download.py       # Загрузка данных Open5e
│   ├── game.py           # Игровые команды
│   ├── service_messages.py # Логирование сервисных сообщений
│   └── topic_cache.py    # Кеширование топиков
└── utils/                # Вспомогательные утилиты
    ├── group_fsm_storage.py  # FSM Storage для групповых чатов
    ├── message_utils.py      # Безопасное редактирование сообщений
    └── session_id_helper.py  # Утилиты для session_id
```

## Обязательные требования

### Синтаксис aiogram 3.x

1. **Используй async/await** для всех обработчиков
2. **Организуй обработчики через Router** — не через Dispatcher напрямую
3. **Используй Dependency Injection** через аннотации типов
4. **Применяй FSM** (`StatesGroup`, `State`) для управления диалогами

### Регистрация обработчиков

Регистрируйте обработчики через декораторы:

```python
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

router = Router(name="my_router")

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer("Hello!")

@router.callback_query(F.data == "button:action")
async def handle_button(callback: CallbackQuery) -> None:
    await callback.answer()

@router.callback_query(F.data.startswith("prefix:"))
async def handle_prefix(callback: CallbackQuery) -> None:
    action = callback.data.split(":")[-1]
    await callback.answer()

@router.message(SomeState.waiting_input)
async def handle_state(message: Message, state: FSMContext) -> None:
    await state.clear()
```

### Структура роутера

```python
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

router = Router(name="my_router")

_service: MyService = None

def init_router(service: MyService) -> None:
    """Инициализация зависимостей роутера."""
    global _service
    _service = service

@router.callback_query(F.data == "action")
async def handler(callback: CallbackQuery) -> None:
    ...
```

## Запреты

**НЕ используй синтаксис aiogram 2.x:**

| Устаревшее (2.x) | Правильное (3.x) |
|------------------|------------------|
| `dp.register_*` | `@router.*` декораторы |
| `content_types=` | Фильтры как аргументы декоратора |
| `bot.send_message()` | `message.answer()` |
| `router.*.register()` | `@router.*` декораторы |

## FSM в групповых чатах

### Проблема

По умолчанию `aiogram` использует ключ `(bot_id, chat_id, user_id)` для хранения `FSM state`.
В групповых чатах это приводит к проблеме:

- User A отправляет команду — создается state для `user_id=A`
- User B нажимает кнопку — aiogram ищет state для `user_id=B` — не находит — обработчик возвращает `UNHANDLED`

### Решение

Используй кастомный storage `modules/telegram/utils/group_fsm_storage.py`:

```python
from modules.telegram.utils import GroupFSMStorage

class AppServices:
    def __init__(self):
        self._dispatcher = Dispatcher(storage=GroupFSMStorage())
```

**Поведение GroupFSMStorage:**

- **Групповой чат** (`chat_id < 0`): все участники работают с общим FSM state (`user_id=0`)
- **Личный чат** (`chat_id > 0`): каждый пользователь имеет свой FSM state

## Middleware

### Типы middleware

- **AdminCheckMiddleware** — проверка прав администратора
- **SessionCheckMiddleware** — проверка доступа к игровым командам

### Подключение middleware

```python
router.message.middleware(AdminCheckMiddleware())
router.callback_query.middleware(SessionCheckMiddleware(services))
```

### Реализация middleware

```python
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from modules.appconfig import get_config

class AdminCheckMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()
        self.admin_ids = get_config().telegram.admin_user_id
    
    async def __call__(self, handler, event, data):
        if event.from_user.id not in self.admin_ids:
            return
        return await handler(event, data)
```

## FSM состояния

Определяй состояния через `StatesGroup`:

```python
from aiogram.fsm.state import State, StatesGroup

class SessionCreationStates(StatesGroup):
    """Состояния для создания новой игровой сессии."""
    
    waiting_for_session_name = State()
    selecting_scenario = State()
    selecting_addons = State()
    adding_players = State()
    binding_character = State()
    confirmation = State()
```

Используй `FSMContext` для управления состояниями:

```python
@router.message(SessionCreationStates.waiting_for_session_name)
async def handle_session_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(SessionCreationStates.selecting_scenario)
    await message.answer("Выберите сценарий")

@router.callback_query(F.data == "confirm")
async def confirm_creation(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await callback.answer("Создано!")
```

## Клавиатуры

Используй `InlineKeyboardBuilder` для построения клавиатур:

```python
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def build_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Кнопка 1", callback_data="action:1")
    builder.button(text="Кнопка 2", callback_data="action:2")
    builder.adjust(2)  # 2 кнопки в ряд
    return builder.as_markup()
```

## Конфигурация

Загружай через `get_config()` из `modules.appconfig`:

```python
from modules.appconfig import get_config

config = get_config()
bot_token = config.telegram.bot_token
admin_ids = config.telegram.admin_user_id
```

## Документация и ресурсы

### Локальная документация проекта

- `AgentsHelpCentr/aiogram/README.rst` — общее описание библиотеки
- `AgentsHelpCentr/aiogram/CHANGES.rst` — история изменений версий
- `.agent/rules/telegram_aiogram_guide.md` — правила проекта для aiogram

### Официальные источники

- [Документация aiogram 3.x](https://docs.aiogram.dev/en/latest/)
- [Миграция с 2.x на 3.x](https://docs.aiogram.dev/en/latest/migration_2_to_3.html)
- [GitHub aiogram](https://github.com/aiogram/aiogram)
- [Примеры кода](https://github.com/aiogram/aiogram/tree/dev-3.x/examples)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## Примеры типичных задач

### Создание нового роутера

1. Создай файл в `modules/telegram/routers/`
2. Определи `router = Router(name="...")`
3. Добавь обработчики через декораторы
4. Экспортируй роутер в `__init__.py`
5. Подключи в `MasterBot.setup_routers()`

### Добавление новой команды

```python
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="my_commands")

@router.message(Command("mycommand"))
async def cmd_mycommand(message: Message) -> None:
    await message.answer("Ответ на команду")
```

### Обработка callback_query с данными

```python
@router.callback_query(F.data.startswith("item:"))
async def handle_item(callback: CallbackQuery) -> None:
    item_id = callback.data.split(":")[1]
    await callback.message.edit_text(f"Выбран элемент: {item_id}")
    await callback.answer()
```

## Тестирование

При написании тестов для Telegram-функциональности:

1. Используй фикстуры из `tests/conftest.py`
2. Мокируй `Bot` и `Dispatcher` при необходимости
3. Тестируй логику обработчиков отдельно от aiogram
4. Проверяй FSM переходы и данные состояний
