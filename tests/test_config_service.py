import pytest
import os
from dotenv import load_dotenv
from unittest.mock import patch
from src.services.config_service import ConfigService, DatabaseConfig, WebDriverConfig, ScrapingConfig, LoggingConfig

# Carrega .env e valida variáveis obrigatórias
load_dotenv()

REQUIRED_ENV_VARS = [
    "DATABASE_URL", "DB_POOL_SIZE", "DB_MAX_OVERFLOW", "DB_POOL_PRE_PING", "DB_POOL_RECYCLE",
    "EDGE_DRIVER_PATH", "HEADLESS", "WEBDRIVER_TIMEOUT", "PAGE_LOAD_TIMEOUT",
    "WEBSITE_TYPE", "MAX_EXECUTION_TIME", "DELAY_BETWEEN_REQUESTS", "MAX_RETRIES",
    "BATCH_SIZE", "WAITING_INTERVAL", "MAX_ATTEMPTS", "DISABLE_SCRAPING",
    "LOG_LEVEL", "LOG_FILE", "LOG_FORMAT"
]

missing_vars = [key for key in REQUIRED_ENV_VARS if not os.getenv(key)]
if missing_vars:
    raise ValueError(f"\u274c Variáveis obrigatórias ausentes no .env: {', '.join(missing_vars)}")

class TestConfigService:
    """Testes para o serviço de configuração"""

    @pytest.fixture
    def config_service(self):
        """Instância padrão com .env carregado corretamente"""
        return ConfigService()

    def test_config_from_env(self, config_service):
        """Testa se todas as configurações são corretamente carregadas das variáveis de ambiente"""
        config = config_service

        # Database
        db = config.database
        assert isinstance(db, DatabaseConfig)
        assert db.pool_size == int(os.getenv("DB_POOL_SIZE"))
        assert db.max_overflow == int(os.getenv("DB_MAX_OVERFLOW"))
        assert db.pool_pre_ping == (os.getenv("DB_POOL_PRE_PING").lower() == "true")
        assert db.pool_recycle == int(os.getenv("DB_POOL_RECYCLE"))

        # WebDriver
        wd = config.webdriver
        assert isinstance(wd, WebDriverConfig)
        assert wd.driver_path == os.getenv("EDGE_DRIVER_PATH")
        assert wd.headless == (os.getenv("HEADLESS").lower() == "true")
        assert wd.timeout == int(os.getenv("WEBDRIVER_TIMEOUT"))
        assert wd.page_load_timeout == int(os.getenv("PAGE_LOAD_TIMEOUT"))

        # Scraping
        sc = config.scraping
        assert isinstance(sc, ScrapingConfig)
        assert sc.website_type == os.getenv("WEBSITE_TYPE")
        assert sc.max_execution_time == int(os.getenv("MAX_EXECUTION_TIME"))
        assert sc.delay_between_requests == float(os.getenv("DELAY_BETWEEN_REQUESTS"))
        assert sc.max_retries == int(os.getenv("MAX_RETRIES"))
        assert sc.batch_size == int(os.getenv("BATCH_SIZE"))
        assert sc.intervalo_espera == int(os.getenv("WAITING_INTERVAL"))
        assert sc.max_tentativas == int(os.getenv("MAX_ATTEMPTS"))
        assert sc.disable_scraping == (os.getenv("DISABLE_SCRAPING").lower() == "true")

        # Logging
        log = config.logging
        assert isinstance(log, LoggingConfig)
        assert log.level == os.getenv("LOG_LEVEL")
        assert log.file_path == os.getenv("LOG_FILE")
        assert log.format == os.getenv("LOG_FORMAT")

    @patch.dict(os.environ, {'DISABLE_SCRAPING': 'true'})
    def test_is_development_mode_true(self):
        """Verifica que o modo de desenvolvimento retorna True quando DISABLE_SCRAPING=true"""
        config = ConfigService()
        assert config.is_development_mode() is True

    def test_is_development_mode_false(self, config_service):
        """Verifica que o modo de desenvolvimento retorna False por padrão"""
        assert config_service.is_development_mode() is False

    def test_dataclass_representations(self):
        """Garante que as dataclasses podem ser instanciadas diretamente"""
        assert DatabaseConfig(
            url="x",
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600
        ).url == "x"
        assert WebDriverConfig(
            driver_path="/d",
            headless=True,
            timeout=10,
            page_load_timeout=20
        ).driver_path == "/d"
        assert ScrapingConfig(
            website_type="X",
            max_execution_time=1,
            delay_between_requests=0.1,
            max_retries=1,
            batch_size=1,
            intervalo_espera=1,
            max_tentativas=1,
            disable_scraping=False
        ).website_type == "X"
        assert LoggingConfig(
            level="DEBUG",
            file_path="/tmp/test.log",
            format="%(message)s"
        ).level == "DEBUG"
