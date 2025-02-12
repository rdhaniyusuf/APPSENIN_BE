from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5432/appsenindb"

    # class Config:
    #     env_file = ".env"  # Load dari file .env jika ada

settings = Settings()