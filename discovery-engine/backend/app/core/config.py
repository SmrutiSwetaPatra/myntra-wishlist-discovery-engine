from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Myntra Discovery Copilot"
    API_V1_STR: str = "/api/v1"
    
    SQLITE_DB_PATH: str = "data/myntra_copilot.db"
    YOUTUBE_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    ALLOWED_ORIGINS: str = ""

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Resolve absolute path so Alembic and FastAPI both find the same db file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(base_dir, self.SQLITE_DB_PATH)
        return f"sqlite+aiosqlite:///{db_path}"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"),
        case_sensitive=True, 
        extra="ignore"
    )

settings = Settings()
