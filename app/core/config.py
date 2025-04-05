from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Параметры базы данных
    postgres_user: str = "postgres"
    postgres_password: str = "secret"
    postgres_db: str = "secrets_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Параметры Redis
    redis_host: str = "localhost"
    redis_port: int = 6379

    # Секрет для шифрования
    encryption_secret_key: str = "Yt7KTwOtWINvqbw0HMonsb8IRKhzcT1Y53Fy7sgBgg0="

    class Config:
        env_file = ".env"

settings = Settings()
