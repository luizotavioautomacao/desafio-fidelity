#!/usr/bin/env python3
"""
Exemplo Prático de Web Scraping com Filtros

Este script demonstra como usar o sistema de web scraping
implementado com diferentes tipos de filtros.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.config_service import ConfigService
from src.services.logging_service import LoggingService
from src.services.validation_service import ValidationService
from src.services.web_scraper_service import WebScraperService, ResultAnalyzer
from src.spv_automatico import create_spv_automatico
from unittest.mock import Mock, patch

def exemplo_validacao_filtros():
    """Demonstra validação de documentos para diferentes filtros"""
    print("🔍 Exemplo de Validação por Filtros")
    print("=" * 50)
    
    validation_service = ValidationService()
    
    # Dados de exemplo
    dados_teste = [
        {
            "filtro": 0,
            "tipo": "CPF",
            "documento": "123.456.789-09",
            "nome": "João Silva",
            "rg": "12.345.678-9"
        },
        {
            "filtro": 1,
            "tipo": "RG",
            "documento": "12.345.678-9",
            "nome": "Maria Santos",
            "rg": "12.345.678-9"
        },
        {
            "filtro": 2,
            "tipo": "Nome",
            "documento": "João Silva",
            "nome": "João Silva",
            "rg": "12.345.678-9"
        },
        {
            "filtro": 3,
            "tipo": "RG Alternativo",
            "documento": "12.345.678-9",
            "nome": "Pedro Costa",
            "rg": "12.345.678-9"
        }
    ]
    
    for dados in dados_teste:
        print(f"\n📋 Filtro {dados['filtro']} - {dados['tipo']}:")
        
        # Valida o documento apropriado para o filtro
        result = validation_service.validate_document_for_filter(
            filtro=dados['filtro'],
            cpf=dados.get('cpf', ''),
            rg=dados['rg'],
            nome=dados['nome']
        )
        
        if result.is_valid:
            print(f"   ✅ Documento válido: {result.corrected_value}")
        else:
            print(f"   ❌ Documento inválido: {result.error_message}")
    
    print()

def exemplo_configuracao_webdriver():
    """Demonstra configuração do WebDriver"""
    print("⚙️ Configuração do WebDriver")
    print("=" * 50)
    
    config_service = ConfigService()
    
    print("1. Configurações atuais:")
    print(f"   Website: {config_service.scraping.website_type}")
    print(f"   Headless: {config_service.webdriver.headless}")
    print(f"   Timeout: {config_service.webdriver.timeout}s")
    print(f"   Driver Path: {config_service.webdriver.driver_path}")
    
    print("\n2. Configurações de scraping:")
    print(f"   Max Execution Time: {config_service.scraping.max_execution_time}s")
    print(f"   Delay Between Requests: {config_service.scraping.delay_between_requests}s")
    print(f"   Max Retries: {config_service.scraping.max_retries}")
    
    print()

def exemplo_web_scraping_simulado():
    """Demonstra web scraping com mocks (sem navegador real)"""
    print("🌐 Exemplo de Web Scraping (Simulado)")
    print("=" * 50)
    
    # Mock do banco de dados
    mock_db = Mock()
    mock_db.execute.return_value.fetchall.return_value = []
    mock_db.execute.return_value.scalar.return_value = 0
    
    with patch('src.spv_automatico.get_db') as mock_get_db:
        mock_get_db.return_value = iter([mock_db])
        
        # Cria instância do SPV
        config_service = ConfigService()
        spv = create_spv_automatico(config_service)
        
        # Dados de teste
        pesquisas_teste = [
            {
                "filtro": 0,
                "documento": "123.456.789-09",
                "nome": "João Silva",
                "cod_pesquisa": 1001
            },
            {
                "filtro": 1,
                "documento": "12.345.678-9",
                "nome": "Maria Santos",
                "cod_pesquisa": 1002
            },
            {
                "filtro": 2,
                "documento": "João Silva",
                "nome": "João Silva",
                "cod_pesquisa": 1003
            }
        ]
        
        print("🔍 Executando pesquisas simuladas:")
        
        for pesquisa in pesquisas_teste:
            print(f"\n📋 Pesquisa {pesquisa['cod_pesquisa']}:")
            print(f"   Filtro: {pesquisa['filtro']}")
            print(f"   Documento: {pesquisa['documento']}")
            
            # Mock do resultado do web scraping
            with patch.object(spv.web_scraper_service, 'pesquisar') as mock_pesquisar:
                # Simula diferentes resultados
                if pesquisa['filtro'] == 0:
                    mock_pesquisar.return_value = "Não existem informações disponíveis para os parâmetros informados."
                elif pesquisa['filtro'] == 1:
                    mock_pesquisar.return_value = "Processos encontrados"
                else:
                    mock_pesquisar.return_value = "Audiências"
                
                # Mock do salvamento no banco
                with patch.object(spv.database_service, 'salvar_resultado_spv') as mock_salvar:
                    mock_salvar.return_value = True
                    
                    # Executa a pesquisa
                    resultado = spv.executar_pesquisa(
                        nome=pesquisa['nome'],
                        cpf=pesquisa.get('cpf', ''),
                        rg=pesquisa.get('rg', ''),
                        cod_pesquisa=pesquisa['cod_pesquisa']
                    )
                    
                    if resultado:
                        # Analisa o resultado
                        page_source = mock_pesquisar.return_value
                        codigo_resultado = spv.result_analyzer.analisar_resultado(page_source)
                        
                        print(f"   ✅ Sucesso!")
                        print(f"   📄 Resultado: {codigo_resultado}")
                        
                        # Mapeia código para descrição
                        resultados = {
                            1: "Nada consta",
                            2: "Criminal",
                            5: "Cível",
                            7: "Erro"
                        }
                        print(f"   📊 Descrição: {resultados.get(codigo_resultado, 'Desconhecido')}")
                    else:
                        print(f"   ❌ Falha na pesquisa")
    
    print()

def exemplo_analise_resultados():
    """Demonstra análise de diferentes tipos de resultados"""
    print("📊 Análise de Resultados")
    print("=" * 50)
    
    analyzer = ResultAnalyzer()
    
    # Diferentes tipos de conteúdo de página
    paginas_teste = [
        {
            "conteudo": "Não existem informações disponíveis para os parâmetros informados.",
            "descricao": "Nada consta"
        },
        {
            "conteudo": "Processos encontrados",
            "descricao": "Processos encontrados"
        },
        {
            "conteudo": "Audiências",
            "descricao": "Audiências"
        },
        {
            "conteudo": "",
            "descricao": "Página vazia"
        },
        {
            "conteudo": "Erro interno do servidor",
            "descricao": "Erro do servidor"
        }
    ]
    
    for pagina in paginas_teste:
        resultado = analyzer.analisar_resultado(pagina['conteudo'])
        
        # Mapeia código para descrição
        resultados = {
            1: "Nada consta",
            2: "Criminal",
            5: "Cível",
            7: "Erro"
        }
        
        print(f"📄 {pagina['descricao']}:")
        print(f"   Código: {resultado}")
        print(f"   Resultado: {resultados.get(resultado, 'Desconhecido')}")
    
    print()

def exemplo_filtros_por_tipo():
    """Demonstra como usar diferentes tipos de filtros"""
    print("🎯 Tipos de Filtros Disponíveis")
    print("=" * 50)
    
    filtros = [
        {
            "codigo": 0,
            "nome": "CPF",
            "descricao": "Pesquisa por CPF da pessoa",
            "exemplo": "123.456.789-09"
        },
        {
            "codigo": 1,
            "nome": "RG",
            "descricao": "Pesquisa por RG da pessoa",
            "exemplo": "12.345.678-9"
        },
        {
            "codigo": 2,
            "nome": "Nome",
            "descricao": "Pesquisa por nome completo",
            "exemplo": "João Silva"
        },
        {
            "codigo": 3,
            "nome": "RG Alternativo",
            "descricao": "Pesquisa por RG (formato alternativo)",
            "exemplo": "12.345.678-9"
        }
    ]
    
    for filtro in filtros:
        print(f"🔍 Filtro {filtro['codigo']} - {filtro['nome']}:")
        print(f"   Descrição: {filtro['descricao']}")
        print(f"   Exemplo: {filtro['exemplo']}")
        print()
    
    print("💡 Como usar:")
    print("   spv.filtro = 0  # Define filtro para CPF")
    print("   spv.executar_pesquisa(nome, cpf, rg, cod_pesquisa)")
    print()

def exemplo_configuracao_avancada():
    """Demonstra configurações avançadas para web scraping"""
    print("⚙️ Configurações Avançadas")
    print("=" * 50)
    
    print("1. Configuração via variáveis de ambiente:")
    print("   export WEBSITE_TYPE=TJSP")
    print("   export HEADLESS=False")
    print("   export WEBDRIVER_TIMEOUT=60")
    print("   export DELAY_BETWEEN_REQUESTS=2.0")
    
    print("\n2. Configuração via arquivo .env:")
    print("   WEBSITE_TYPE=TJSP")
    print("   HEADLESS=True")
    print("   WEBDRIVER_TIMEOUT=30")
    print("   PAGE_LOAD_TIMEOUT=60")
    print("   MAX_EXECUTION_TIME=600")
    print("   DELAY_BETWEEN_REQUESTS=1.0")
    print("   MAX_RETRIES=3")
    
    print("\n3. Configuração de banco de dados:")
    print("   DATABASE_URL=postgresql://user:pass@localhost:5432/db")
    print("   DB_POOL_SIZE=10")
    print("   DB_MAX_OVERFLOW=20")
    
    print("\n4. Configuração de logging:")
    print("   LOG_LEVEL=DEBUG")
    print("   LOG_FILE=spv_automatico.log")
    
    print()

def main():
    """Função principal"""
    print("🚀 Exemplo Prático de Web Scraping com Filtros")
    print("=" * 60)
    print()
    
    try:
        # Demonstra validação de filtros
        exemplo_validacao_filtros()
        
        # Demonstra configuração do WebDriver
        exemplo_configuracao_webdriver()
        
        # Demonstra web scraping simulado
        exemplo_web_scraping_simulado()
        
        # Demonstra análise de resultados
        exemplo_analise_resultados()
        
        # Demonstra tipos de filtros
        exemplo_filtros_por_tipo()
        
        # Demonstra configurações avançadas
        exemplo_configuracao_avancada()
        
        print("✅ Exemplo concluído com sucesso!")
        print()
        print("🎯 Próximos Passos:")
        print("   1. Configure o WebDriver do Edge")
        print("   2. Configure o banco de dados PostgreSQL")
        print("   3. Execute o sistema completo")
        print("   4. Monitore os logs")
        
    except Exception as e:
        print(f"❌ Erro no exemplo: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 