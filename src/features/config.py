from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    image_provider: str = "openai"   # "openai" | "placeholder"
    openai_api_key: str | None = None
    default_tz: str = "Asia/Karachi"

    # pydantic-settings v2 style config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

# Purpose: centralize configuration from environment variables (e.g., .env).
#
# Functions/Classes:
#
# Settings(BaseSettings) (if you installed pydantic-settings):
#
# image_provider (openai or placeholder)
#
# openai_api_key
#
# default_tz
#
# model_config = SettingsConfigDict(env_file=".env") so it reads your .env.
#
# get_settings() -> Settings
#
# Why: cached accessor so you don’t re‑parse env repeatedly.
#
# Why we need it:
# Feature flags & secrets live here. It’s how assets.py knows whether to call OpenAI.

