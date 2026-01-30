"""
Модуль для загрузки конфигурации из .env и config/settings.json.
Объединяет конфигурацию приложения и логгера.
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

from dotenv import load_dotenv

@dataclass
class DatabaseConfig:
    """Конфигурация базы данных."""

    path: Path  # Путь к базе данных

@dataclass
class AppData:
    """Конфигурация данных приложения."""

    data_dir: Path  # Путь к директории с данными приложения

@dataclass
class LoggingConfig:
    """Конфигурация логирования."""

    mode: Literal["production", "development"]
    log_dir: Path
    retention_days: int
    console_level: str
    file_level: str
    format: str
    date_format: str

    @property
    def is_development(self) -> bool:
        """Проверка, включен ли режим разработки."""
        return self.mode == "development"

    @property
    def is_production(self) -> bool:
        """Проверка, включен ли режим production."""
        return self.mode == "production"


@dataclass
class AppConfig:
    """Основная конфигурация приложения."""
    database: DatabaseConfig
    appdata: AppData
    logging: LoggingConfig
    # Путь для сохранения результатов тестов
    tests_results_dir: Path
    @classmethod
    def load(
        cls, env_path: str = "config/.env", settings_path: str = "config/settings.json"
    ) -> "AppConfig":
        """
        Загрузка конфигурации из файлов.

        Args:
            env_path: Путь к .env файлу
            settings_path: Путь к settings.json

        Returns:
            Экземпляр AppConfig с загруженными настройками

        Raises:
            ValueError: Если отсутствуют обязательные параметры
            FileNotFoundError: Если не найден файл конфигурации
        """
        # Загрузка .env
        load_dotenv(env_path)

        # Проверка обязательных переменных окружения
        # TODO: Добавить проверку других переменных окружения при необходимости

        # Загрузка settings.json
        settings_file = Path(settings_path)
        if not settings_file.exists():
            raise FileNotFoundError(f"Файл конфигурации {settings_path} не найден")

        with open(settings_file, "r", encoding="utf-8") as f:
            settings = json.load(f)

        # Создание конфигурации базы данных
        db_settings = settings.get("database", {})
        database_config = DatabaseConfig(
            path=Path(db_settings.get("path", "DataBase/"))
        )

        # Создание конфигурации данных приложения
        app_data_settings = settings.get("appdata", {})
        app_data_config = AppData(
            data_dir=Path(app_data_settings.get("path", "AppData/"))
        )

        # Создание конфигурации логирования
        log_settings = settings.get("logging", {})
        logging_config = LoggingConfig(
            mode=log_settings.get("mode", "production"),
            log_dir=Path(log_settings.get("log_dir", "logs")),
            retention_days=log_settings.get("retention_days", 10),
            console_level=log_settings.get("console_level", "INFO"),
            file_level=log_settings.get("file_level", "DEBUG"),
            format=log_settings.get(
                "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            ),
            date_format=log_settings.get("date_format", "%Y-%m-%d %H:%M:%S"),
        )

        # Директория для результатов тестов
        tests_settings = settings.get("tests", {})
        tests_results_dir = Path(tests_settings.get("results_dir", "tests/result"))

        return cls(
            database=database_config,
            appdata=app_data_config,
            logging=logging_config,
            tests_results_dir=tests_results_dir,
        )


# Глобальный экземпляр конфигурации
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """
    Получение глобального экземпляра конфигурации.

    Returns:
        Экземпляр AppConfig

    Example:
        >>> from modules.appconfig import get_config
        >>> config = get_config()
        >>> print(config.telegram.bot_token)
        >>> print(config.logging.mode)
    """
    global _config

    if _config is None:
        _config = AppConfig.load()

    return _config
