---
trigger: always_on
---

<environmentActivatedReminder>

## Перед работой с терминалом

### Активировать виртуальное окружение и установить UTF-8

```powershell
.venv\Scripts\Activate.ps1; $OutputEncoding=[System.Text.UTF8Encoding]::new(); [Console]::OutputEncoding=[System.Text.Encoding]::UTF8; $env:PYTHONIOENCODING='utf-8'
```

**Критично:** Без UTF-8 кириллица в логах отображается как псевдографика CP866.

</environmentActivatedReminder>
