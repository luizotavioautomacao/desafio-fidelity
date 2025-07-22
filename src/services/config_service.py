import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

def get_required_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None or value.strip() == "":
        raise ValueError(f"❌ A variável obrigatória '{var_name}' não está definida no arquivo .env.")
    return value

def get_required_int(var_name: str) -> int:
    return int(get_required_env(var_name))

def get_required_float(var_name: str) -> float:
    return float(get_required_env(var_name))

def get_required_bool(var_name: str) -> bool:
    return get_required_env(var_name).lower() == "true"

@dataclass
class DatabaseConfig:
    url: str
    pool_size: int
    max_overflow: int
    pool_pre_ping: bool
    pool_recycle: int

@dataclass
class WebDriverConfig:
    driver_path: str
    headless: bool
    timeout: int
    page_load_timeout: int

@dataclass
class ScrapingConfig:
    website_type: str
    max_execution_time: int
    delay_between_requests: float
    max_retries: int
    batch_size: int
    intervalo_espera: int
    max_tentativas: int
    disable_scraping: bool

@dataclass
class LoggingConfig:
    level: str
    format: str
    file_path: str

class ConfigService:
    def __init__(self, env_file: str = ".env"):
        load_dotenv(env_file)
        self._database_config = self._load_database_config()
        self._webdriver_config = self._load_webdriver_config()
        self._scraping_config = self._load_scraping_config()
        self._logging_config = self._load_logging_config()

    def _load_database_config(self) -> DatabaseConfig:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            user = get_required_env("DB_USER")
            password = get_required_env("DB_PASSWORD")
            host = get_required_env("DB_HOST")
            port = get_required_env("DB_PORT")
            name = get_required_env("DB_NAME")
            db_url = f"postgresql://{user}:{password}@{host}:{port}/{name}"

        return DatabaseConfig(
            url=db_url,
            pool_size=get_required_int("DB_POOL_SIZE"),
            max_overflow=get_required_int("DB_MAX_OVERFLOW"),
            pool_pre_ping=get_required_bool("DB_POOL_PRE_PING"),
            pool_recycle=get_required_int("DB_POOL_RECYCLE"),
        )

    def _load_webdriver_config(self) -> WebDriverConfig:
        return WebDriverConfig(
            driver_path=get_required_env("EDGE_DRIVER_PATH"),
            headless=get_required_bool("HEADLESS"),
            timeout=get_required_int("WEBDRIVER_TIMEOUT"),
            page_load_timeout=get_required_int("PAGE_LOAD_TIMEOUT"),
        )

    def _load_scraping_config(self) -> ScrapingConfig:
        return ScrapingConfig(
            website_type=get_required_env("WEBSITE_TYPE"),
            max_execution_time=get_required_int("MAX_EXECUTION_TIME"),
            delay_between_requests=get_required_float("DELAY_BETWEEN_REQUESTS"),
            max_retries=get_required_int("MAX_RETRIES"),
            batch_size=get_required_int("BATCH_SIZE"),
            intervalo_espera=get_required_int("WAITING_INTERVAL"),
            max_tentativas=get_required_int("MAX_ATTEMPTS"),
            disable_scraping=get_required_bool("DISABLE_SCRAPING"),
        )

    def _load_logging_config(self) -> LoggingConfig:
        return LoggingConfig(
            level=get_required_env("LOG_LEVEL"),
            format=get_required_env("LOG_FORMAT"),
            file_path=get_required_env("LOG_FILE"),
        )

    @property
    def database(self) -> DatabaseConfig:
        return self._database_config

    @property
    def webdriver(self) -> WebDriverConfig:
        return self._webdriver_config

    @property
    def scraping(self) -> ScrapingConfig:
        return self._scraping_config

    @property
    def logging(self) -> LoggingConfig:
        return self._logging_config

    def is_development_mode(self) -> bool:
        return self.scraping.disable_scraping
