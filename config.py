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
    
    class Config:
        env_file = ".env"

settings = Settings()
