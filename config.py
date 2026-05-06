from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    # Configuración SMTP (leer desde .env)
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    SMTP_FROM_NAME: str

    # URL base sin el root_path (/dal) para enlaces en emails
    BASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    EXPORT_QUEUE_DRIVER: str = "redis"
    NOTIFICATION_QUEUE_DRIVER: str = "thread"
    NOTIFICATION_QUEUE_NAME: str = "notifications"
    EXPORT_BASE_URL: str | None = None
    EXPORT_TMP_DIR: str = "tmp/exports"
    EXPORT_URL_TTL_MINUTES: int = 1440
    EXPORT_MAX_SIZE_MB: int = 500
    EXPORT_STATUS_CACHE_TTL_SECONDS: int = 30

    # Firebase Cloud Messaging
    FIREBASE_ENABLED: bool = False
    FIREBASE_PROJECT_ID: str | None = None
    FIREBASE_CREDENTIALS_FILE: str | None = None
    FIREBASE_CREDENTIALS_JSON: str | None = None
    FIREBASE_ANDROID_CHANNEL_ID: str | None = None
    FIREBASE_NOTIFICATION_SOUND: str = "default"
    
    class Config:
        env_file = ".env"

settings = Settings()
