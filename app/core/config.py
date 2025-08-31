from pydantic import BaseModel


class Settings(BaseModel):
    POSTGRES_URL: str = "postgresql+asyncpg://onlynone:NonGrata21@localhost/mydb"
    REDIS_URL: str = "redis://localhost:6379"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    TELEGRAM_BOT_TOKEN: str = "your_bot_token"

    class Config:
        env_file = ".env"


settings = Settings()