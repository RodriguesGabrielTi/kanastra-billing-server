from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Kanastra Billing Server"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/db"
    MONGO_URI: str
    # Comment: 50000 por chunk foi a melhor eficiência que eu obtive nos meus testes
    CHUNK_SIZE_TO_SAVE: int = 50_000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
