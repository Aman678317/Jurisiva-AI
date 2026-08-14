# Typed Environment Configuration Validation

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    app_env: string = os.getenv("APP_ENV", "development")
    database_url: string = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/legal_db")
    redis_url: string = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    object_storage_endpoint: string = os.getenv("OBJECT_STORAGE_ENDPOINT", "http://localhost:9000")
    object_storage_bucket: string = os.getenv("OBJECT_STORAGE_BUCKET", "legal-documents")
    object_storage_access_key: string = os.getenv("OBJECT_STORAGE_ACCESS_KEY", "minioadmin")
    object_storage_secret_key: string = os.getenv("OBJECT_STORAGE_SECRET_KEY", "minioadmin")
    jwt_secret: string = os.getenv("JWT_SECRET", "super-secret-production-key-32-chars-minimum-hash")
    jwt_algorithm: string = "HS256"
    jwt_expiration_hours: int = 24

settings = Settings()
