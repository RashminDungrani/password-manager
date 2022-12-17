import enum
from typing import Optional

from pydantic import BaseSettings
from yarl import URL

from app.utils.app_paths import app_paths

# TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    # host: str = "192.168.1.237"
    host: str = "0.0.0.0"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    db_scheme: str = "sqlite"
    db_host: str = ""
    db_port: Optional[int] = None  # 5432
    db_user: Optional[str] = None
    db_pass: Optional[str] = None
    db_path: str = ""
    db_echo: bool = False

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        self.db_host = self.db_host if self.db_host != "" else "/" + app_paths.DB_FILE
        # self.db_path = self.db_path if self.db_path != "" else app_paths.DB_FILE
        generated_url = URL.build(
            scheme=self.db_scheme,
            user=self.db_user,
            password=self.db_pass,
            host=self.db_host,
            port=self.db_port,
            path=self.db_path,  # path should be commented only while creating db from main file
        )
        # generated_url = f"{self.db_scheme}://///{app_paths.DB_FILE}"
        # print("Generated DB URL ::", generated_url)
        # print(URL(generated_url))
        # return URL("mysql+aiomysql://mysql:password@localhost:3306/dyv_db")
        return generated_url

    class Config:
        env_file = "envs/dev.env"
        env_file_encoding = "utf-8"


settings = Settings()
