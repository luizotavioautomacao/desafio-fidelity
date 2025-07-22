import logging
import sys
from typing import Optional
from src.services.config_service import LoggingConfig

class LoggingService:
    """Serviço de logging centralizado"""
    
    def __init__(self, config: LoggingConfig):
        self.config = config
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Configura o sistema de logging"""
        # Configura o logger raiz
        logging.basicConfig(
            level=getattr(logging, self.config.level.upper()),
            format=self.config.format,
            handlers=[
                logging.FileHandler(self.config.file_path),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def get_logger(self, name: str) -> logging.Logger:
        """Retorna um logger configurado para o módulo especificado"""
        return logging.getLogger(name)
    
    def log_execution_start(self, logger: logging.Logger, filtro: int, website_type: str) -> None:
        """Loga o início da execução"""
        logger.info(f"Iniciando execução - Filtro: {filtro}, Website: {website_type}")
    
    def log_execution_end(self, logger: logging.Logger, pesquisas_processadas: int, tempo_total: float) -> None:
        """Loga o fim da execução"""
        logger.info(f"Execução finalizada - Pesquisas processadas: {pesquisas_processadas}, Tempo total: {tempo_total:.2f}s")
    
    def log_pesquisa_start(self, logger: logging.Logger, cod_pesquisa: int, documento: str) -> None:
        """Loga o início de uma pesquisa"""
        logger.debug(f"Iniciando pesquisa {cod_pesquisa} com documento: {documento}")
    
    def log_pesquisa_success(self, logger: logging.Logger, cod_pesquisa: int, resultado: int, tempo: float) -> None:
        """Loga o sucesso de uma pesquisa"""
        logger.info(f"Pesquisa {cod_pesquisa} executada com sucesso. Resultado: {resultado}, Tempo: {tempo}s")
    
    def log_pesquisa_error(self, logger: logging.Logger, cod_pesquisa: int, error: str) -> None:
        """Loga erro em uma pesquisa"""
        logger.error(f"Erro na pesquisa {cod_pesquisa}: {error}")
    
    def log_database_error(self, logger: logging.Logger, operation: str, error: str) -> None:
        """Loga erro de banco de dados"""
        logger.error(f"Erro de banco de dados na operação '{operation}': {error}")
    
    def log_scraping_error(self, logger: logging.Logger, filtro: int, documento: str, error: str) -> None:
        """Loga erro de scraping"""
        logger.error(f"Erro de scraping - Filtro: {filtro}, Documento: {documento}, Erro: {error}")
    
    def log_configuration(self, logger: logging.Logger, config_info: dict) -> None:
        """Loga informações de configuração"""
        logger.info(f"Configuração carregada: {config_info}")
    
    def log_statistics(self, logger: logging.Logger, stats: dict) -> None:
        """Loga estatísticas do sistema"""
        logger.info(f"Estatísticas: {stats}") 