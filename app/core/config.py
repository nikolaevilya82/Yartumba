"""
Конфигурация приложения Yartumba.
Все настройки читаются из переменных окружения (файл .env).
"""
import os
from typing import List


class Settings:
    """Настройки приложения"""

    def __init__(self):
        # База данных
        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL",
            "sqlite:///./test.db"
        )

        # Окружение
        self.ENV: str = os.getenv("ENV", "DEV")  # DEV | PROD

        # CORS — разрешённые источники (через запятую)
        self._cors_origins: str = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://localhost:3000"
        )

        # SQL-логирование (включать только для отладки)
        self.SQL_ECHO: bool = os.getenv("SQL_ECHO", "false").lower() == "true"

        # Секреты (обязательно сменить в продакшне!)
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
        self.SESSION_SECRET: str = os.getenv("SESSION_SECRET", "change-me-in-production")

    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Список разрешённых CORS-источников"""
        return [o.strip() for o in self._cors_origins.split(",") if o.strip()]


# Единый экземпляр настроек (синглтон)
settings = Settings()