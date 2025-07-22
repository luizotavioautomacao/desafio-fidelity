import pytest
import logging
from unittest.mock import Mock, patch
from src.services.logging_service import LoggingService
from src.services.config_service import LoggingConfig

class TestLoggingService:
    """Testes para o serviço de logging"""
    
    @pytest.fixture
    def logging_config(self):
        """Fixture para configuração de logging"""
        return LoggingConfig(
            level="INFO",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            file_path="test.log"
        )
    
    @pytest.fixture
    def logging_service(self, logging_config):
        """Fixture para criar instância do LoggingService"""
        return LoggingService(logging_config)
    
    def test_get_logger(self, logging_service):
        """Testa obtenção de logger"""
        logger = logging_service.get_logger("test_module")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"
    
    def test_log_execution_start(self, logging_service):
        """Testa log de início de execução"""
        logger = Mock()
        
        logging_service.log_execution_start(logger, 0, "TJSP")
        
        logger.info.assert_called_once_with("Iniciando execução - Filtro: 0, Website: TJSP")
    
    def test_log_execution_end(self, logging_service):
        """Testa log de fim de execução"""
        logger = Mock()
        
        logging_service.log_execution_end(logger, 10, 25.5)
        
        logger.info.assert_called_once_with("Execução finalizada - Pesquisas processadas: 10, Tempo total: 25.50s")
    
    def test_log_pesquisa_start(self, logging_service):
        """Testa log de início de pesquisa"""
        logger = Mock()
        
        logging_service.log_pesquisa_start(logger, 123, "123.456.789-09")
        
        logger.debug.assert_called_once_with("Iniciando pesquisa 123 com documento: 123.456.789-09")
    
    def test_log_pesquisa_success(self, logging_service):
        """Testa log de sucesso de pesquisa"""
        logger = Mock()
        
        logging_service.log_pesquisa_success(logger, 123, 1, 2.5)
        
        logger.info.assert_called_once_with("Pesquisa 123 executada com sucesso. Resultado: 1, Tempo: 2.5s")
    
    def test_log_pesquisa_error(self, logging_service):
        """Testa log de erro de pesquisa"""
        logger = Mock()
        
        logging_service.log_pesquisa_error(logger, 123, "Erro de conexão")
        
        logger.error.assert_called_once_with("Erro na pesquisa 123: Erro de conexão")
    
    def test_log_database_error(self, logging_service):
        """Testa log de erro de banco de dados"""
        logger = Mock()
        
        logging_service.log_database_error(logger, "get_pesquisas", "Connection timeout")
        
        logger.error.assert_called_once_with("Erro de banco de dados na operação 'get_pesquisas': Connection timeout")
    
    def test_log_scraping_error(self, logging_service):
        """Testa log de erro de scraping"""
        logger = Mock()
        
        logging_service.log_scraping_error(logger, 0, "123.456.789-09", "Element not found")
        
        logger.error.assert_called_once_with("Erro de scraping - Filtro: 0, Documento: 123.456.789-09, Erro: Element not found")
    
    def test_log_configuration(self, logging_service):
        """Testa log de configuração"""
        logger = Mock()
        config_info = {"website_type": "TJSP", "headless": True}
        
        logging_service.log_configuration(logger, config_info)
        
        logger.info.assert_called_once_with("Configuração carregada: {'website_type': 'TJSP', 'headless': True}")
    
    def test_log_statistics(self, logging_service):
        """Testa log de estatísticas"""
        logger = Mock()
        stats = {"pendentes": 10, "concluidas": 20}
        
        logging_service.log_statistics(logger, stats)
        
        logger.info.assert_called_once_with("Estatísticas: {'pendentes': 10, 'concluidas': 20}")
    
    @patch('logging.basicConfig')
    def test_setup_logging(self, mock_basic_config, logging_config):
        """Testa configuração do sistema de logging"""
        logging_service = LoggingService(logging_config)
        
        # Verifica se basicConfig foi chamado
        mock_basic_config.assert_called_once()
        
        # Verifica os argumentos passados
        call_args = mock_basic_config.call_args
        assert call_args[1]['level'] == logging.INFO
        assert call_args[1]['format'] == logging_config.format
        assert len(call_args[1]['handlers']) == 2  # FileHandler e StreamHandler 