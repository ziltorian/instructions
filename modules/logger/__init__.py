"""
Модуль логирования для MasterBot.

Предоставляет настраиваемое логирование с поддержкой:
- 5 уровней логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Ротации файлов по дням
- Хранения логов за последние 10 дней
- Двух режимов: production и development
"""

from modules.logger.logger import get_logger

__all__ = ["get_logger"]
