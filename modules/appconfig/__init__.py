"""
Модуль конфигурации приложения.

Предоставляет централизованную конфигурацию для всех модулей проекта.
Загружает настройки из .env и config/settings.json.

Exports:
    - AppConfig: Основной класс конфигурации
    - get_config: Функция получения глобального экземпляра конфигурации
    - TelegramConfig: Конфигурация Telegram бота
    - OpenAIConfig: Конфигурация OpenAI API
    - DatabaseConfig: Конфигурация базы данных
    - TranslatorConfig: Конфигурация переводчика
    - ConverterConfig: Конфигурация конвертора
    - LoggingConfig: Конфигурация логирования

Usage:
    >>> from modules.appconfig import get_config
    >>> config = get_config()
    >>> print(config.telegram.bot_token)
    >>> print(config.logging.mode)
"""

from .config import (
    AppConfig,
    DatabaseConfig,
    LoggingConfig,
    AppData,
    get_config,
)

__all__ = [
    "AppConfig",
    "get_config",
    "DatabaseConfig",
    "AppData",
    "LoggingConfig",
]
