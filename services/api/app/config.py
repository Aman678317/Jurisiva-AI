# Typed Environment Configuration Validation

import os
from dataclasses import dataclass

# Zero-dependency .env file auto-loader
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

@dataclass(frozen=True)
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Jurisiva AI")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    SECRET_KEY: str = os.getenv("JWT_SECRET", "super-secret-production-key-32-chars-minimum-hash")
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/legal_db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    object_storage_endpoint: str = os.getenv("OBJECT_STORAGE_ENDPOINT", "http://localhost:9000")
    object_storage_bucket: str = os.getenv("OBJECT_STORAGE_BUCKET", "legal-documents")
    object_storage_access_key: str = os.getenv("OBJECT_STORAGE_ACCESS_KEY", "minioadmin")
    object_storage_secret_key: str = os.getenv("OBJECT_STORAGE_SECRET_KEY", "minioadmin")
    jwt_secret: str = os.getenv("JWT_SECRET", "super-secret-production-key-32-chars-minimum-hash")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_hours: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    llm_provider: str = os.getenv("LLM_PROVIDER", "ollama")
    ocr_engine: str = os.getenv("OCR_ENGINE", "tesseract")

settings = Settings()
