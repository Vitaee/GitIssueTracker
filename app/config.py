from pydantic import ConfigDict
from pydantic_settings import BaseSettings
import os


def config() -> ConfigDict:
    env = os.getenv('ENV', 'development')
    
    if env == 'production':
        return ConfigDict(env_file=".env.prod")
    else:
        return ConfigDict(env_file=".env")
    

class Settings(BaseSettings):
    ENV: str
    PROJECT_NAME: str
    DATABASE_URL: str
    REDIS_URL: str
    GITHUB_TOKEN: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int 
    MAIL_SERVER: str
    MAIL_TLS: bool = False
    MAIL_SSL: bool = False
    MAIL_STARTTLS: bool = False  
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_PORT: int

    API_V1_STR: str

    model_config = config()


settings = Settings()

