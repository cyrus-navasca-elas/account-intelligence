from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "account-intelligence"
    version: str = "0.1.0"
    environment: str = "development"
    log_level: str = "INFO"

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-opus-4-7"
    apify_api_key: str = ""
    apify_jobs_actor_id: str = ""
    tavily_api_key: str = ""

    capability_map_path: str = "app/capability_map.yaml"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
