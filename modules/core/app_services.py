"""
Централизованное управление жизненным циклом сервисов приложения.

Отвечает за ленивую инициализацию и корректное завершение
основных компонентов бота.
"""

from __future__ import annotations

import asyncio
from typing import Optional

from modules.appconfig import get_config
from modules.logger import get_logger

logger = get_logger(__name__)


class AppServices:
    """Контейнер зависимостей приложения с ленивой инициализацией."""

    def __init__(self) -> None:
        self._config = get_config()
        self._init_lock = asyncio.Lock()
        logger.info("AppServices инициализирован (только критичные сервисы)")

    @property
    def config(self):
        """Возвращает загруженную конфигурацию приложения."""
        return self._config

    async def init_all(self) -> None:
        """Предварительная инициализация критичных сервисов."""
        async with self._init_lock:
            # TODO: Добавить инициализацию других критичных сервисов
            pass
            logger.info("Критичные сервисы предварительно инициализированы")

    async def shutdown(self) -> None:
        """Корректное завершение асинхронных ресурсов."""
        # TODO: Добавить корректное завершение других асинхронных ресурсов
        pass
        logger.info("AppServices завершил работу")
