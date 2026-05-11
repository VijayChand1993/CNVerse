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

    EMBEDDING_MODEL_NAME: str = ("storage/models/bge-base-en-v1.5")
    OPENSEARCH_HOST: str = "localhost"
    OPENSEARCH_PORT: int = 9200
    OPENSEARCH_USERNAME: str = "admin"
    OPENSEARCH_PASSWORD: str = "CNVerse@OpenSearch2026!"
    OPENSEARCH_INDEX_NAME: str = ("cnverse_chunks")
    OPENSEARCH_TOP_K_RESULTS: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
