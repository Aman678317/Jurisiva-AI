# Typed Environment Configuration Validation

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    APP_NAME: str = "Jurisiva AI"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    SECRET_KEY: str = os.getenv("JWT_SECRET", "super-secret-production-key-32-chars-minimum-hash")
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/legal_db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    object_storage_endpoint: str = os.getenv("OBJECT_STORAGE_ENDPOINT", "http://localhost:9000")
    object_storage_bucket: str = os.getenv("OBJECT_STORAGE_BUCKET", "legal-documents")
    object_storage_access_key: str = os.getenv("OBJECT_STORAGE_ACCESS_KEY", "minioadmin")
    object_storage_secret_key: str = os.getenv("OBJECT_STORAGE_SECRET_KEY", "minioadmin")
    jwt_secret: str = os.getenv("JWT_SECRET", "super-secret-production-key-32-chars-minimum-hash")
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

settings = Settings()
