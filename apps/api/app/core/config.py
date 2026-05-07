from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "CNVerse"
    ENV: str = "development"

    DATABASE_URL: str
    REDIS_URL: str
    OPENSEARCH_URL: str

    OPENAI_API_KEY: str
    UPLOAD_DIR: str
    URL_DOWNLOAD_DIR: str
    MAX_UPLOAD_SIZE_MB: int = 100

    class Config:
        env_file = ".env"


settings = Settings()
