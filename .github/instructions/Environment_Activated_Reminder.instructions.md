---
applyTo: '**'
name: 'Environment_Activated_Reminder'
description: 'Правила подготовки терминала перед работой: venv, UTF-8, использование terminal_last_command.'
---

<environmentActivatedReminder>

## Перед работой с терминалом

### 1. Активировать виртуальное окружение и установить UTF-8

```powershell
.venv\Scripts\Activate.ps1; $OutputEncoding=[System.Text.UTF8Encoding]::new(); [Console]::OutputEncoding=[System.Text.Encoding]::UTF8; $env:PYTHONIOENCODING='utf-8'
```

**Критично:** Без UTF-8 кириллица в логах отображается как псевдографика CP866.

### 2. Использовать `terminal_last_command` как надежный метод получения результатов работы терминала
Терминал запускается на устаревшем пк, поэтому код выполняется долго. Команды могут не успевать завершиться до получения вывода.
- Если `run_in_terminal` не вернул вывод — вызвать `terminal_last_command`.
- Если `run_in_terminal` вернул `(exit code 0)` — повторно вызвать `terminal_last_command`.
- Если `terminal_last_command` вернул предыдущую команду — повторно вызвать `terminal_last_command`.
- Надёжно получает полный вывод независимо от типа команды.

</environmentActivatedReminder>
