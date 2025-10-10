#!/usr/bin/env python3
"""
Demonstração das Melhorias SOLID Implementadas no Sistema SPV

Este script demonstra como as melhorias seguindo os princípios SOLID
tornaram o sistema mais modular, testável e extensível.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.config_service import ConfigService
from src.services.logging_service import LoggingService
from src.services.validation_service import ValidationService
from src.services.database_service import DatabaseService
from src.services.web_scraper_service import WebScraperService, ResultAnalyzer
from src.spv_automatico import create_spv_automatico
from unittest.mock import Mock, patch

def demo_validation_service():
    """Demonstra o serviço de validação"""
    print("🔍 Demonstração do ValidationService (SRP)")
    print("=" * 50)
    
    validation_service = ValidationService()
    
    # Testa validação de CPF
    print("1. Validação de CPF:")
    cpf_valido = "123.456.789-09"
    result = validation_service.validate_cpf(cpf_valido)
    print(f"   CPF: {cpf_valido} -> Válido: {result.is_valid}")
    
    cpf_invalido = "123.456.789-10"
    result = validation_service.validate_cpf(cpf_invalido)
    print(f"   CPF: {cpf_invalido} -> Válido: {result.is_valid}")
    
    # Testa validação de RG
    print("\n2. Validação de RG:")
    rg_valido = "12.345.678-9"
    result = validation_service.validate_rg(rg_valido)
    print(f"   RG: {rg_valido} -> Válido: {result.is_valid}")
    
    # Testa validação de nome
    print("\n3. Validação de Nome:")
    nome_valido = "João Silva"
    result = validation_service.validate_nome(nome_valido)
    print(f"   Nome: {nome_valido} -> Válido: {result.is_valid}")
    print(f"   Nome corrigido: {result.corrected_value}")
    
    print()

def demo_config_service():
    """Demonstra o serviço de configuração"""
    print("⚙️ Demonstração do ConfigService (SRP)")
    print("=" * 50)
    
    config_service = ConfigService()
    
    print("1. Configurações do Banco de Dados:")
    print(f"   URL: {config_service.database.url}")
    print(f"   Pool Size: {config_service.database.pool_size}")
    print(f"   Max Overflow: {config_service.database.max_overflow}")
    
    print("\n2. Configurações do WebDriver:")
    print(f"   Headless: {config_service.webdriver.headless}")
    print(f"   Timeout: {config_service.webdriver.timeout}s")
    
    print("\n3. Configurações de Scraping:")
    print(f"   Website Type: {config_service.scraping.website_type}")
    print(f"   Max Execution Time: {config_service.scraping.max_execution_time}s")
    print(f"   Delay Between Requests: {config_service.scraping.delay_between_requests}s")
    
    print("\n4. Configurações de Logging:")
    print(f"   Level: {config_service.logging.level}")
    print(f"   File: {config_service.logging.file_path}")
    
    print()

def demo_logging_service():
    """Demonstra o serviço de logging"""
    print("📝 Demonstração do LoggingService (SRP)")
    print("=" * 50)
    
    config = ConfigService().logging
    logging_service = LoggingService(config)
    
    logger = logging_service.get_logger("demo")
    print(f"1. Logger criado: {logger.name}")
    
    print("2. Métodos de logging disponíveis:")
    print("   - log_execution_start()")
    print("   - log_execution_end()")
    print("   - log_pesquisa_start()")
    print("   - log_pesquisa_success()")
    print("   - log_pesquisa_error()")
    print("   - log_database_error()")
    print("   - log_scraping_error()")
    print("   - log_configuration()")
    print("   - log_statistics()")
    
    print()

def demo_dependency_injection():
    """Demonstra a injeção de dependência"""
    print("🔧 Demonstração da Injeção de Dependência (DIP)")
    print("=" * 50)
    
    # Mock do banco de dados para demonstração
    mock_db = Mock()
    mock_db.execute.return_value.fetchall.return_value = []
    mock_db.execute.return_value.scalar.return_value = 0
    
    with patch('src.spv_automatico.get_db') as mock_get_db:
        mock_get_db.return_value = iter([mock_db])
        
        config_service = ConfigService()
        spv = create_spv_automatico(config_service)
        
        print("1. Serviços injetados:")
        print(f"   - DatabaseService: {type(spv.database_service).__name__}")
        print(f"   - WebScraperService: {type(spv.web_scraper_service).__name__}")
        print(f"   - ResultAnalyzer: {type(spv.result_analyzer).__name__}")
        print(f"   - ConfigService: {type(spv.config_service).__name__}")
        print(f"   - LoggingService: {type(spv.logging_service).__name__}")
        print(f"   - ValidationService: {type(spv.validation_service).__name__}")
        
        print("\n2. Benefícios da Injeção de Dependência:")
        print("   - Baixo acoplamento entre componentes")
        print("   - Fácil substituição de implementações")
        print("   - Testabilidade melhorada")
        print("   - Flexibilidade para diferentes ambientes")
    
    print()

def demo_interfaces():
    """Demonstra o uso de interfaces"""
    print("🔌 Demonstração das Interfaces (ISP)")
    print("=" * 50)
    
    print("1. Interfaces implementadas:")
    print("   - IDatabaseService: Contrato para serviços de banco")
    print("   - IWebScraperService: Contrato para web scraping")
    print("   - IResultAnalyzer: Contrato para análise de resultados")
    
    print("\n2. Benefícios das Interfaces:")
    print("   - Contratos claros entre componentes")
    print("   - Múltiplas implementações possíveis")
    print("   - Facilita testes com mocks")
    print("   - Segue o princípio de segregação de interface")
    
    print("\n3. Exemplo de implementação alternativa:")
    print("   class MongoDBService(IDatabaseService):")
    print("       def get_pesquisas_pendentes(self):")
    print("           # Implementação específica para MongoDB")
    print("           pass")
    
    print()

def demo_error_handling():
    """Demonstra o tratamento de erros melhorado"""
    print("🛡️ Demonstração do Tratamento de Erros")
    print("=" * 50)
    
    validation_service = ValidationService()
    
    print("1. Validação com tratamento de erro:")
    result = validation_service.validate_cpf("")
    print(f"   CPF vazio -> Válido: {result.is_valid}")
    print(f"   Mensagem: {result.error_message}")
    
    result = validation_service.validate_cpf("123")
    print(f"   CPF inválido -> Válido: {result.is_valid}")
    print(f"   Mensagem: {result.error_message}")
    
    print("\n2. Logging estruturado de erros:")
    print("   - Erros de banco de dados")
    print("   - Erros de web scraping")
    print("   - Erros de validação")
    print("   - Erros de configuração")
    
    print()

def demo_testability():
    """Demonstra a testabilidade melhorada"""
    print("🧪 Demonstração da Testabilidade")
    print("=" * 50)
    
    print("1. Testes unitários isolados:")
    print("   - Cada serviço pode ser testado independentemente")
    print("   - Mocks facilitam testes sem dependências externas")
    print("   - Cobertura de testes abrangente")
    
    print("\n2. Testes de integração:")
    print("   - Verificação da integração entre componentes")
    print("   - Testes de fluxo completo")
    print("   - Validação de cenários reais")
    
    print("\n3. Executar testes:")
    print("   pytest tests/ -v")
    print("   pytest tests/ --cov=src")
    print("   pytest tests/test_validation_service.py")
    
    print()

def main():
    """Função principal da demonstração"""
    print("🚀 Demonstração das Melhorias SOLID no Sistema SPV")
    print("=" * 60)
    print()
    
    try:
        demo_validation_service()
        demo_config_service()
        demo_logging_service()
        demo_dependency_injection()
        demo_interfaces()
        demo_error_handling()
        demo_testability()
        
        print("✅ Demonstração concluída com sucesso!")
        print()
        print("📊 Resumo das Melhorias:")
        print("   - ✅ Single Responsibility Principle (SRP)")
        print("   - ✅ Open/Closed Principle (OCP)")
        print("   - ✅ Liskov Substitution Principle (LSP)")
        print("   - ✅ Interface Segregation Principle (ISP)")
        print("   - ✅ Dependency Inversion Principle (DIP)")
        print()
        print("🎯 Benefícios Alcançados:")
        print("   - Código mais modular e organizado")
        print("   - Alta testabilidade")
        print("   - Fácil extensão e manutenção")
        print("   - Baixo acoplamento")
        print("   - Tratamento robusto de erros")
        print("   - Configuração centralizada")
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 