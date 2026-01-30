---
name: 'Terminal_Tools'
description: 'Расширенная инструкция по запуску tool при работе с терминалом в Windows: проверенные команды, настройки и решения всех проблем.'
---

## Рекомендуемые команды

### PowerShell (рекомендуется)

**Полный вывод с Out-Host (наиболее надёжно):**
```powershell
. .venv\Scripts\Activate.ps1
$OutputEncoding=[System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING='utf-8'
python -m pytest -q --tb=short | Out-Host
```
**Особенности:** Всегда возвращает вывод агенту немедленно, live-режим, UTF-8 корректна.

**Рекомендация:** Часто используйте флаг `--tb=short` (например `python -m pytest -q --tb=short`), чтобы сократить длинные трассировки и уменьшить объём вывода.

**С контролем ширины через Out-String:**
```powershell
. .venv\Scripts\Activate.ps1
$OutputEncoding=[System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING='utf-8'
python -m pytest -q --tb=short 2>&1 | Out-String -Width 4096 | Out-Host
```
**Особенности:** Контролирует ширину строк, всегда возвращает вывод агенту, live-режим.

**С фильтрацией через Select-String:**
```powershell
. .venv\Scripts\Activate.ps1
$OutputEncoding=[System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING='utf-8'
python -m pytest -q --tb=short 2>&1 | Select-String -Pattern 'passed|failed|ERROR'
```
**Особенности:** Фильтрует вывод по паттернам, может требовать `terminal_last_command`.

**⚠️ Избегай Select-Object:**
```powershell
# НЕ ИСПОЛЬЗУЙ для pytest:
python -m pytest -q --tb=short | Select-Object -First 10  # Обрезает итоговый результат!
```
**Проблема:** `-First/-Last` обрезает вывод до N строк, пропускает важную информацию о результатах тестов.

### cmd (альтернатива)

**Полный вывод UTF-8:**
```cmd
chcp 65001>nul
.venv\Scripts\activate.bat
set PYTHONIOENCODING=utf-8
python -m pytest -q --tb=short
```

### Резервный вариант (файл)

**Для детального анализа:**
```powershell
. .venv\Scripts\Activate.ps1
$env:PYTHONIOENCODING='utf-8'
python -m pytest -q --tb=short 2>&1 | Out-File -Encoding utf8 pytest_output.txt
Get-Content pytest_output.txt -TotalCount 400
```

## Фикстура pytest для подавления логов

Фикстура уже добавлена в `tests/conftest.py`:

```python
@pytest.fixture(autouse=True)
def reduce_logging():
    """Подавить DEBUG/INFO логи для чистого вывода тестов."""
    logging.getLogger().setLevel(logging.WARNING)
    for logger_name in ['modules.game', 'modules.telegram', 'modules.database', 'modules.openai']:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
```

## Резервные методы получения вывода

### Если run_in_terminal не возвращает вывод

Используйте инструмент `terminal_last_command` для получения вывода последней команды:

```python
# После запуска команды через run_in_terminal
terminal_last_command()
```

Этот инструмент возвращает:
- Последнюю выполненную команду
- Код выхода
- Полный вывод команды

**Применение:**
- Select-String и другие фильтры могут не возвращать вывод сразу
- `terminal_last_command` надёжно получает результат после завершения команды

### PowerShell Select-String с резервным получением

```powershell
. .venv\Scripts\Activate.ps1
$env:PYTHONIOENCODING='utf-8'
python -m pytest -q 2>&1 | Select-String -Pattern 'passed|failed|ERROR'
```

Затем вызвать `terminal_last_command()` для получения отфильтрованного вывода.

### Для фоновых команд: get_terminal_output

Используйте `get_terminal_output(id)` для получения вывода фоновых команд:

```python
# Запуск фоновой команды
result = run_in_terminal(command="...", isBackground=True)
terminal_id = result['terminal_id']  # Получить ID из результата

# Получить вывод по ID
get_terminal_output(id=terminal_id)
```

**Применение:**
- Работает только для фоновых команд (`isBackground=True`)
- Требует правильный UUID терминала из результата `run_in_terminal`
- Повторные вызовы возвращают одинаковый полный вывод
- **Не используй** строковые ID типа "powershell" — только UUID

## Альтернативные инструменты

### mcp_pylance_mcp_s_pylanceRunCodeSnippet

**Назначение:** Выполнение Python кода напрямую в workspace environment

**Преимущества:**
- **ПРЕДПОЧТИТЕЛЬНЕЕ** чем `python -c` для Python snippets
- Автоматически использует правильный Python интерпретатор workspace
- Избегает проблем с shell quoting/escaping
- Чистый вывод без терминальных артефактов
- Не требует создания временных файлов

**Требования для кириллицы:**
```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# ... остальной код
```

**Пример:**
```python
mcp_pylance_mcp_s_pylanceRunCodeSnippet(
    workspaceRoot="file:///d:/PythonProjects/MasterBot",
    codeSnippet="""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
print("Тест кириллицы")
"""
)
```

## Что избегать

- ❌ Не использовать `Select-Object -First/-Last` для pytest вывода (обрезает важную информацию)
- ❌ Не устанавливать `PYTHONUTF8` в cmd через однострочный вызов (вызывает ошибку preinit)
- ❌ Не использовать `Out-File` для live-режима
- ❌ Не запускать pytest без активации `.venv`

## Результаты тестирования

| Команда | Живой вывод | UTF-8 | Чистые логи | Агент получает ответ | Резервный метод |
|---------|-------------|-------|-------------|----------------------|-----------------|
| PowerShell `Out-Host` | ✓ | ✓ | ✓ (с фикстурой) | ✓ (всегда) | — |
| PowerShell `Out-String` | ✓ | ✓ | ✓ (с фикстурой) | ✓ (всегда) | — |
| cmd `chcp 65001` | ✓ | ✓ | ✓ (с фикстурой) | ✓/✗ (нестабильно) | ✓ (`terminal_last_command`) |
| PowerShell `Select-String` | ✓ | ✓ | ✓ (фильтр) | ✓/✗ (нестабильно) | ✓ (`terminal_last_command`) |
| `Out-File` | ✗ | ✓ | ✓ | ✓ (неживой) | — |

## Краткие выводы

- **Предпочтительно**: PowerShell с `Out-Host` + UTF-8 + фикстура pytest (наиболее надёжно, всегда возвращает вывод)
- **Альтернатива**: cmd с `chcp 65001` + фикстура pytest (может требовать `terminal_last_command`)
- **Фильтрация**: PowerShell `Select-String` с UTF-8 (может требовать `terminal_last_command`)
- **Резерв**: `Out-File` для анализа полного вывода
- **КРИТИЧНО**: Без установки UTF-8 кириллица в логах отображается как псевдографика CP866 (╬яЎш , ╦ютъюёЄ№)
- **Важно**: При отсутствии немедленного ответа используй `terminal_last_command` для получения результата
