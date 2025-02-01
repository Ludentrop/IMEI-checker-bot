from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path


env_file = env_file_path = Path(__file__).parent / '.env'


class Settings(BaseSettings):
    TOKEN: SecretStr
    API_KEY: SecretStr
    WHITELIST_USERS: list[int] = [65102721, 1140069329]
    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding='utf-8')


settings = Settings()
