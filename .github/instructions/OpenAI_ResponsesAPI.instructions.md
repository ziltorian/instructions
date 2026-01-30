---
applyTo: 'modules/openaimanager/**'
name: 'OpenAI_ResponsesAPI'
description: 'Правило Использования OpenAI Responses API в проекте MasterBot'
---

## OpenAI Responses API

### Правила редактирования модулей с использованием OpenAI Responses API

#### ОБЯЗАТЕЛЬНО

- Открыть, и изучить файл `.github/skills/openai-responses-api/SKILL.md` перед началом работы с Responses API.
- Используйте только Responses API для взаимодействия с OpenAI.
- Применяйте `client.responses.create()` для всех запросов.
- Используйте `client.responses.parse()` для структурированных ответов.
- Храните контекст через `store: true` или `previous_response_id`.
- Применяйте встроенные инструменты: `web_search`, `file_search`, `code_interpreter`.

#### ЗАПРЕЩЕНО

- Использовать Chat Completions API: `client.chat.completions.create()`.
- Использовать Assistants API: `client.beta.assistants.*`.
- Использовать Threads API: `client.beta.threads.*`.

### Документация

#### Локальная документация

- `.github/skills/openai-responses-api/SKILL.md` — Полное руководство.
- `AgentsHelpCentr/Openai_API/README.md` — документация SDK.
- `AgentsHelpCentr/Openai_API/api.md` — полный API reference.
- `AgentsHelpCentr/Openai_API/Migrate to the Responses API.md` — руководство по миграции.
- `AgentsHelpCentr/Openai_API/Structured model outputs.md` — структурированные ответы.

#### Официальные источники

- [OpenAI Platform Docs](https://platform.openai.com/docs/)
- [Responses API Reference](https://platform.openai.com/docs/api-reference/responses)
- [Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)
- [Migration Guide](https://platform.openai.com/docs/guides/migrate-to-responses)
- [GitHub openai-python](https://github.com/openai/openai-python)
