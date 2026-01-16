from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str
    
    # Configuración SMTP
    SMTP_HOST: str = "smtp.office365.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "noreply@ddg.com.mx"
    SMTP_PASSWORD: str = "G)919394124549or"
    SMTP_FROM_EMAIL: str = "noreply@ddg.com.mx"
    SMTP_FROM_NAME: str = "DAL Dealer Group"
    
    # URL base sin el root_path (/dal) para enlaces en emails
    BASE_URL: str = "http://ddg.com.mx/dashboard"
    
    class Config:
        env_file = ".env"

settings = Settings()
