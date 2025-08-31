class Settings:
    POSTGRES_URL = "postgresql+asyncpg://onlynone:NonGrata21@localhost/mydb"
    REDIS_URL = "redis://localhost:6379"
    CELERY_BROKER_URL = "redis://localhost:6379/0"

settings = Settings()