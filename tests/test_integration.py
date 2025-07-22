import pytest
from unittest.mock import Mock, patch, MagicMock
from services.config_service import ConfigService
from services.logging_service import LoggingService
from services.validation_service import ValidationService
from services.database_service import DatabaseService
from services.web_scraper_service import WebScraperService, ResultAnalyzer
from spv_automatico import SPVAutomatico, create_spv_automatico

class TestIntegration:
    """Testes de integração para demonstrar o funcionamento do sistema"""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock da sessão do banco de dados"""
        session = Mock()
        # Mock para get_pesquisas_pendentes
        session.execute.return_value.fetchall.return_value = [
            (1, 100, 'SP', '2024-01-01', 'João Silva', '123.456.789-09', '12.345.678-9', 
             '1990-01-01', 'Maria Silva', None, None, None)
        ]
        # Mock para get_pesquisas_por_filtro
        session.execute.return_value.scalar.return_value = 1
        return session
    
    @pytest.fixture
    def mock_config_service(self):
        """Mock do serviço de configuração"""
        config = ConfigService()
        # Override para modo de desenvolvimento
        config._scraping_config.max_execution_time = 10  # Tempo menor para testes
        return config
    
    @pytest.fixture
    def spv_instance(self, mock_db_session, mock_config_service):
        """Cria uma instância do SPV para testes"""
        # Mock do get_db
        with patch('src.spv_automatico.get_db') as mock_get_db:
            mock_get_db.return_value = iter([mock_db_session])
            
            # Cria instância do SPV
            spv = create_spv_automatico(mock_config_service)
            return spv
    
    def test_create_spv_automatico(self, mock_db_session, mock_config_service):
        """Testa criação da instância do SPV com injeção de dependência"""
        with patch('src.spv_automatico.get_db') as mock_get_db:
            mock_get_db.return_value = iter([mock_db_session])
            
            spv = create_spv_automatico(mock_config_service)
            
            # Verifica se todos os serviços foram injetados
            assert spv.database_service is not None
            assert spv.web_scraper_service is not None
            assert spv.result_analyzer is not None
            assert spv.config_service is not None
            assert spv.logging_service is not None
            assert spv.validation_service is not None
    
    def test_validation_service_integration(self, spv_instance):
        """Testa integração do serviço de validação"""
        # Testa validação de CPF válido
        result = spv_instance.validation_service.validate_cpf("123.456.789-09")
        assert result.is_valid is True
        assert result.corrected_value == "123.456.789-09"
        
        # Testa validação de CPF inválido
        result = spv_instance.validation_service.validate_cpf("123.456.789-10")
        assert result.is_valid is False
        
        # Testa validação de documento para filtro
        result = spv_instance.validation_service.validate_document_for_filter(
            0, "123.456.789-09", "", ""
        )
        assert result.is_valid is True
    
    def test_config_service_integration(self, spv_instance):
        """Testa integração do serviço de configuração"""
        config = spv_instance.config_service
        
        # Verifica se todas as configurações estão disponíveis
        assert config.database is not None
        assert config.webdriver is not None
        assert config.scraping is not None
        assert config.logging is not None
        
        # Verifica valores padrão
        assert config.scraping.website_type == "TJSP"
        assert config.webdriver.headless is True
        assert config.database.pool_size == 10
    
    def test_logging_service_integration(self, spv_instance):
        """Testa integração do serviço de logging"""
        logger = spv_instance.logging_service.get_logger("test")
        assert logger is not None
        assert logger.name == "test"
        
        # Testa métodos de logging
        with patch.object(logger, 'info') as mock_info:
            spv_instance.logging_service.log_execution_start(logger, 0, "TJSP")
            mock_info.assert_called_once()
    
    def test_database_service_integration(self, spv_instance, mock_db_session):
        """Testa integração do serviço de banco de dados"""
        # Mock para pesquisas pendentes
        spv_instance.database_service.get_pesquisas_pendentes = Mock(return_value=[(1, 100, 'Cliente Teste', 'SP', None, 'João Silva', '123.456.789-00', '12.345.678-9', None, 'Maria Silva', None, None, None)])
        # Mock para contagem por filtro
        spv_instance.database_service.get_pesquisas_por_filtro = Mock(return_value=1)
        # Mock para salvar resultado SPV
        spv_instance.database_service.salvar_resultado_spv = Mock(return_value=True)
        
        # Testa obtenção de pesquisas pendentes
        pesquisas = spv_instance.database_service.get_pesquisas_pendentes(filtro=0)
        assert len(pesquisas) == 1
        assert pesquisas[0][1] == 100  # cod_pesquisa
        
        # Testa contagem por filtro
        count = spv_instance.database_service.get_pesquisas_por_filtro(filtro=0)
        assert count == 1
        
        # Testa salvamento de resultado
        result = spv_instance.database_service.salvar_resultado_spv(
            cod_pesquisa=100, filtro=0, resultado=1, tempo_execucao=2.5
        )
        assert result is True
    
    def test_result_analyzer_integration(self, spv_instance):
        """Testa integração do analisador de resultados"""
        analyzer = spv_instance.result_analyzer
        
        # Testa análise de "nada consta"
        page_source = "Não existem informações disponíveis para os parâmetros informados."
        result = analyzer.analisar_resultado(page_source)
        assert result == 1  # Nada consta
        
        # Testa análise de "processos encontrados"
        page_source = "Processos encontrados"
        result = analyzer.analisar_resultado(page_source)
        assert result == 5  # Cível
        
        # Testa análise de página vazia
        result = analyzer.analisar_resultado("")
        assert result == 7  # Erro
    
    @patch('src.services.web_scraper_service.WebScraperFactory.create_scraper')
    def test_web_scraper_service_integration(self, mock_create_scraper, spv_instance):
        """Testa integração do serviço de web scraping"""
        # Mock do scraper
        mock_scraper = Mock()
        mock_scraper.pesquisar_por_cpf.return_value = "Processos encontrados"
        mock_create_scraper.return_value = mock_scraper
        
        # Mock do setup_driver para configurar o scraper
        with patch.object(spv_instance.web_scraper_service, 'setup_driver') as mock_setup:
            # Configura o scraper no serviço
            spv_instance.web_scraper_service.scraper = mock_scraper
            
            # Testa pesquisa
            page_source = spv_instance.web_scraper_service.pesquisar(0, "123.456.789-09")
            assert page_source == "Processos encontrados"
    
    def test_spv_executar_pesquisa_integration(self, spv_instance):
        """Testa integração da execução de pesquisa"""
        # Mock do web scraper
        spv_instance.web_scraper_service.pesquisar = Mock(return_value="Processos encontrados")
        
        # Mock do banco de dados
        spv_instance.database_service.salvar_resultado_spv = Mock(return_value=True)
        
        # Executa pesquisa
        result = spv_instance.executar_pesquisa(
            nome="João Silva",
            cpf="123.456.789-09",
            rg="12.345.678-9",
            cod_pesquisa=100
        )
        
        # Verifica se foi bem-sucedido
        assert result is True
        
        # Verifica se os serviços foram chamados
        spv_instance.web_scraper_service.pesquisar.assert_called_once()
        spv_instance.database_service.salvar_resultado_spv.assert_called_once()
    
    def test_spv_processar_pesquisas_pendentes_integration(self, spv_instance):
        """Testa integração do processamento de pesquisas pendentes"""
        # Mock da execução de pesquisa
        spv_instance.executar_pesquisa = Mock(return_value=True)
        # Mock para pesquisas pendentes
        spv_instance.database_service.get_pesquisas_pendentes = Mock(return_value=[(1, 100, 'Cliente Teste', 'SP', None, 'João Silva', '123.456.789-00', '12.345.678-9', None, 'Maria Silva', None, None, None)])
        
        # Processa pesquisas pendentes
        result = spv_instance.processar_pesquisas_pendentes(limit=10)
        
        # Verifica se processou uma pesquisa
        assert result == 1
        spv_instance.executar_pesquisa.assert_called_once()
    
    def test_error_handling_integration(self, spv_instance):
        """Testa tratamento de erros integrado"""
        # Mock de erro no web scraper
        spv_instance.web_scraper_service.pesquisar = Mock(side_effect=Exception("Erro de conexão"))
        
        # Mock do banco de dados
        spv_instance.database_service.salvar_resultado_spv = Mock(return_value=True)
        
        # Executa pesquisa com erro
        result = spv_instance.executar_pesquisa(
            nome="João Silva",
            cpf="123.456.789-09",
            rg="12.345.678-9",
            cod_pesquisa=100
        )
        
        # Verifica se retornou False em caso de erro
        assert result is False 