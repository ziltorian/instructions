---
name: openai-responses-api
description: Reference for OpenAI Responses API integration. Use this when writing code that interacts with OpenAI models, creating structured outputs, handling multi-turn conversations, or migrating from Chat Completions API.
---

# OpenAI Responses API

Responses API — основной API для взаимодействия с моделями OpenAI в этом проекте. Это современная замена Chat Completions API с улучшенной производительностью и встроенными инструментами.

## Когда использовать этот skill

Используй этот skill когда нужно:

- Создать или изменить код взаимодействия с OpenAI
- Использовать структурированные ответы (Structured Outputs)
- Организовать цепочки вызовов и мульти-turn диалоги
- Мигрировать код с Chat Completions API
- Подключить встроенные инструменты (`web_search`, `file_search`, `code_interpreter`)

## Обязательные правила

### ОБЯЗАТЕЛЬНО

- Используй **только Responses API** для взаимодействия с OpenAI
- Применяй `client.responses.create()` для всех запросов
- Применяй `client.responses.parse()` для структурированных ответов
- Храни контекст через `store: true` или `previous_response_id`
- Используй встроенные инструменты: `web_search`, `file_search`, `code_interpreter`
- Загружай конфигурацию через `get_config()` из `modules.appconfig`

### ЗАПРЕЩЕНО

- Использовать Chat Completions API: `client.chat.completions.create()` ❌
- Использовать Assistants API: `client.beta.assistants.*` ❌
- Использовать Threads API: `client.beta.threads.*` ❌

## Преимущества Responses API

| Аспект | Преимущество |
|--------|-------------|
| Производительность | +3% на SWE-bench по сравнению с Chat Completions |
| Кэширование | 40-80% снижение затрат |
| Мультимодальность | Нативная поддержка текста и изображений |
| Инструменты | Встроенные `web_search`, `file_search`, `code_interpreter`, MCP |

## Основные концепции

### Items вместо Messages

Responses API использует **Items** вместо **Messages**:

- `message` — сообщение в контексте
- `function_call` — вызов функции
- `function_call_output` — результат функции
- `text` — текстовый вывод модели
- `reasoning` — промежуточные рассуждения модели

### Основные методы SDK

```python
# Создание ответа
client.responses.create(**params) -> Response

# Получение ответа по ID
client.responses.retrieve(response_id, **params) -> Response

# Удаление ответа
client.responses.delete(response_id) -> None

# Отмена ответа
client.responses.cancel(response_id) -> Response

# Парсинг со схемой (Structured Outputs)
client.responses.parse(**params) -> ParsedResponse

# Потоковый вывод
client.responses.stream(**params) -> Stream
```

## Примеры использования

### Базовый запрос

```python
from openai import OpenAI
from modules.appconfig import get_config

config = get_config()
client = OpenAI(api_key=config.openai.api_key)

# Простой текстовый запрос
response = client.responses.create(
    model=config.openai.model_name,
    input="Что такое D&D?"
)
text = response.output_text

# С системной инструкцией
response = client.responses.create(
    model="gpt-4o",
    instructions="Ты - Dungeon Master",
    input="Начни приключение"
)
```

### Список сообщений

```python
response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "system", "content": "Ты переводчик"},
        {"role": "user", "content": "Переведи: dragon"}
    ]
)
text = response.output_text
```

### Цепочка вызовов (multi-turn)

```python
# С previous_response_id
response1 = client.responses.create(
    model="gpt-4o",
    input="Создай персонажа D&D",
    store=True
)

response2 = client.responses.create(
    model="gpt-4o",
    previous_response_id=response1.id,
    input="Добавь описание внешности"
)

# Ручное управление контекстом
context = [{"role": "user", "content": "Что такое магия?"}]
res1 = client.responses.create(model="gpt-4o", input=context)

context += res1.output
context += [{"role": "user", "content": "Расскажи подробнее"}]

res2 = client.responses.create(model="gpt-4o", input=context)
```

## Structured Outputs

Структурированные ответы гарантируют, что модель вернёт данные в заданном JSON-формате.

### С Pydantic (рекомендуется)

```python
from openai import OpenAI
from pydantic import BaseModel
from modules.appconfig import get_config

config = get_config()
client = OpenAI(api_key=config.openai.api_key)

class TranslationResult(BaseModel):
    translated_text: str

response = client.responses.parse(
    model=config.openai.model_name,
    instructions="Ты - профессиональный переводчик.",
    input="Spell",
    text_format=TranslationResult,
)

translated = response.output_parsed.translated_text
```

### Сложная структура

```python
from pydantic import BaseModel

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Ты - репетитор по математике."},
        {"role": "user", "content": "Реши: 8x + 7 = -23"}
    ],
    text_format=MathReasoning,
)

math_result = response.output_parsed
```

### С JSON Schema

```python
response = client.responses.create(
    model="gpt-4o-2024-08-06",
    input="Извлеки данные персонажа",
    text={
        "format": {
            "type": "json_schema",
            "strict": True,
            "name": "character_data",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "level": {"type": "integer"},
                    "class": {"type": "string"}
                },
                "required": ["name", "level", "class"],
                "additionalProperties": False
            }
        }
    }
)
```

### Ограничения JSON Schema

- Все поля должны быть `required`
- Объект верхнего уровня не может быть `anyOf`
- Максимум 5000 свойств объекта
- Максимум 10 уровней вложенности
- Максимум 1000 значений enum
- Обязательно `additionalProperties: false` для объектов

### Эмуляция опциональных полей

```python
{
    "name": {"type": "string"},
    "description": {"anyOf": [{"type": "string"}, {"type": "null"}]}
}
```

### Поддерживаемые модели

- `gpt-4o-2024-08-06` и позднее
- `gpt-4o-mini` и `gpt-4o-mini-2024-07-18` и позднее
- Для старых моделей: `text={"format": {"type": "json_object"}}`

## Встроенные инструменты

```python
# Web Search
response = client.responses.create(
    model="gpt-4o",
    input="Найди информацию о драконах",
    tools=[{"type": "web_search"}]
)

# File Search (требует vector_store)
response = client.responses.create(
    model="gpt-4o",
    input="Найди в документах информацию",
    tools=[{"type": "file_search", "vector_store_ids": ["vs_xxx"]}]
)

# Code Interpreter
response = client.responses.create(
    model="gpt-4o",
    input="Посчитай среднее значение: [1, 2, 3, 4, 5]",
    tools=[{"type": "code_interpreter"}]
)
```

## Асинхронное использование

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def main():
    response = await client.responses.create(
        model="gpt-4o",
        input="Создай персонажа"
    )
    print(response.output_text)

asyncio.run(main())
```

## Потоковый вывод (Streaming)

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class EntitiesModel(BaseModel):
    attributes: list[str]
    locations: list[str]

with client.responses.stream(
    model="gpt-4o",
    input="Извлеки сущности из текста",
    text_format=EntitiesModel,
) as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="")
    
    final_response = stream.get_final_response()
```

## Обработка ошибок

```python
import openai
from openai import OpenAI

client = OpenAI()

try:
    response = client.responses.create(
        model="gpt-4o",
        input="Текст запроса"
    )
except openai.APIConnectionError as e:
    print("Сервер недоступен")
    print(e.__cause__)
except openai.RateLimitError as e:
    print("Превышен лимит запросов")
except openai.APIStatusError as e:
    print(f"Ошибка: {e.status_code}")
    print(e.response)
```

### Коды ошибок

| Код | Тип ошибки |
|-----|------------|
| 400 | `BadRequestError` |
| 401 | `AuthenticationError` |
| 403 | `PermissionDeniedError` |
| 404 | `NotFoundError` |
| 422 | `UnprocessableEntityError` |
| 429 | `RateLimitError` |
| >=500 | `InternalServerError` |
| N/A | `APIConnectionError` |

## Обработка отказов (Refusals)

```python
from pydantic import BaseModel

class MathReasoning(BaseModel):
    steps: list[str]
    final_answer: str

response = client.responses.parse(
    model="gpt-4o",
    input="Реши задачу",
    text_format=MathReasoning,
)

if response.output_parsed is None:
    print("Модель отказалась отвечать")
else:
    print(response.output_parsed.final_answer)
```

## Сравнение с Chat Completions

| Параметр | Chat Completions | Responses API |
|----------|------------------|---------------|
| Endpoint | `/v1/chat/completions` | `/v1/responses` |
| Входные данные | `messages` | `input` |
| Системный промпт | `messages[0]` с `role: system` | `instructions` |
| Результат | `choices[0].message.content` | `output_text` или `output` |
| Структурированный вывод | `response_format` | `text.format` или `text_format` |
| Хранение контекста | Ручное | `store: true` или `previous_response_id` |
| Встроенные инструменты | Нет | Да |

## Миграция с Chat Completions

**Было (ЗАПРЕЩЕНО):**

```python
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a translator"},
        {"role": "user", "content": "Translate: dragon"}
    ]
)
text = completion.choices[0].message.content
```

**Стало (ОБЯЗАТЕЛЬНО):**

```python
response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "system", "content": "You are a translator"},
        {"role": "user", "content": "Translate: dragon"}
    ]
)
text = response.output_text
```

## Логирование

```python
from modules.logger import get_logger

logger = get_logger(__name__)

# Запрос
logger.log_api_request(
    service="OpenAI",
    endpoint="/v1/responses",
    data={"model": model, "input": input_data}
)

# Ответ
logger.log_api_response(
    service="OpenAI",
    endpoint="/v1/responses",
    response=response
)

# Или напрямую
logger.log_openai_response(response)
```

## Дополнительные ресурсы

### Локальная документация

- [api.md](../AgentsHelpCentr/Openai_API/api.md) — полный API reference
- [README.md](../AgentsHelpCentr/Openai_API/README.md) — документация SDK
- [Migrate to the Responses API.md](../AgentsHelpCentr/Openai_API/Migrate%20to%20the%20Responses%20API.md) — руководство по миграции
- [Structured model outputs.md](../AgentsHelpCentr/Openai_API/Structured%20model%20outputs.md) — структурированные ответы

### Официальная документация

- [OpenAI Platform Docs](https://platform.openai.com/docs/)
- [Responses API Reference](https://platform.openai.com/docs/api-reference/responses)
- [Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)
- [Migration Guide](https://platform.openai.com/docs/guides/migrate-to-responses)
- [GitHub openai-python](https://github.com/openai/openai-python)
