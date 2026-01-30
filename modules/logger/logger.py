"""
Основной модуль логирования.

Предоставляет настроенный логгер с автоматической ротацией файлов,
очисткой старых логов и поддержкой двух режимов работы.
"""

import logging
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from modules.appconfig import LoggingConfig


class ColoredFormatter(logging.Formatter):
    """Форматтер с цветным выводом для консоли."""
    
    # ANSI цветовые коды
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Форматирование записи лога с цветами.
        
        Args:
            record: Запись лога
            
        Returns:
            Отформатированная строка с ANSI кодами цветов
        """
        # Сохранение оригинальных значений
        original_levelname = record.levelname
        original_name = record.name
        
        # Получение цвета для уровня логирования
        color = self.COLORS.get(record.levelname, self.RESET)
        
        # Цветное имя уровня
        record.levelname = f"{self.BOLD}{color}{record.levelname}{self.RESET}"
        
        # Цветное имя модуля
        record.name = f"\033[34m{record.name}{self.RESET}"  # Blue
        
        # Форматирование сообщения
        formatted = super().format(record)
        
        # Восстановление оригинальных значений для других обработчиков
        record.levelname = original_levelname
        record.name = original_name
        
        return formatted


class DailyRotatingLogger:
    """
    Класс для управления логированием с ежедневной ротацией файлов.
    
    Особенности:
    - Ротация файлов по дням (один файл на день)
    - Автоматическая очистка файлов старше retention_days
    - Два режима работы: production и development
    - Вывод в консоль и файлы
    """
    
    def __init__(self, name: str, config: Optional["LoggingConfig"] = None) -> None:
        """
        Инициализация логгера.
        
        Args:
            name: Имя логгера (обычно __name__ модуля)
            config: Конфигурация логгера (если None, загружается из get_config())
        """
        self._name = name
        
        if config is None:
            from modules.appconfig import get_config
            config = get_config().logging
        
        self._config = config
        self._logger = self._setup_logger()
        self._cleanup_old_logs()
    
    def _setup_logger(self) -> logging.Logger:
        """
        Настройка логгера с обработчиками.
        
        Returns:
            Настроенный объект logging.Logger
        """
        logger = logging.getLogger(self._name)
        logger.setLevel(logging.DEBUG)  # Минимальный уровень для логгера
        
        # Очистка существующих обработчиков
        logger.handlers.clear()
        
        # Форматтер для файлов (без цветов)
        file_formatter = logging.Formatter(
            fmt=self._config.format,
            datefmt=self._config.date_format
        )
        
        # Форматтер для консоли (с цветами)
        console_formatter = ColoredFormatter(
            fmt=self._config.format,
            datefmt=self._config.date_format
        )
        
        # Обработчик консоли
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, self._config.console_level))
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # Обработчик файлов
        file_handler = self._get_file_handler()
        file_handler.setLevel(getattr(logging, self._config.file_level))
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def _get_file_handler(self) -> logging.FileHandler:
        """
        Создание обработчика для записи в файл.
        
        Returns:
            Настроенный FileHandler
        """
        # Создание директории для логов
        log_dir = self._config.log_dir
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Формирование имени файла с текущей датой
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"masterbot_{current_date}.log"
        
        # Создание обработчика
        handler = logging.FileHandler(log_file, encoding="utf-8")
        
        return handler
    
    def _cleanup_old_logs(self) -> None:
        """Удаление лог-файлов старше retention_days."""
        log_dir = self._config.log_dir
        
        if not log_dir.exists():
            return
        
        retention_date = datetime.now() - timedelta(days=self._config.retention_days)
        
        for log_file in log_dir.glob("masterbot_*.log"):
            try:
                # Извлечение даты из имени файла
                date_str = log_file.stem.replace("masterbot_", "")
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                
                # Удаление файла если он старше retention_days
                if file_date < retention_date:
                    log_file.unlink()
                    self._logger.debug(f"Удален старый лог-файл: {log_file.name}")
            except (ValueError, OSError) as e:
                # Пропуск файлов с некорректным форматом имени
                self._logger.warning(f"Не удалось обработать файл {log_file.name}: {e}")
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """Логирование на уровне DEBUG."""
        self._logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        """Логирование на уровне INFO."""
        self._logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """Логирование на уровне WARNING."""
        self._logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """Логирование на уровне ERROR."""
        self._logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """Логирование на уровне CRITICAL."""
        self._logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args, exc_info: bool = True, **kwargs) -> None:
        """Логирование исключений с трейсбеком (аналог logging.Logger.exception)."""
        self._logger.exception(message, *args, exc_info=exc_info, **kwargs)
    
    @property
    def is_development(self) -> bool:
        """Проверка режима разработки."""
        return self._config.is_development


# Глобальный кеш логгеров
_loggers: dict[str, DailyRotatingLogger] = {}


def get_logger(name: str) -> DailyRotatingLogger:
    """
    Получение экземпляра логгера.
    
    Args:
        name: Имя логгера (обычно __name__ модуля)
    
    Returns:
        Настроенный экземпляр DailyRotatingLogger
    
    Example:
        >>> from modules.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Приложение запущено")
    """
    if name not in _loggers:
        _loggers[name] = DailyRotatingLogger(name)
    
    return _loggers[name]
