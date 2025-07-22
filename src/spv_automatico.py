import datetime
import time
import logging
import sys
import os
from typing import List, Tuple, Optional
from tqdm import tqdm
from config.database import get_db
from interfaces.database_interface import IDatabaseService
from interfaces.web_scraper_interface import IWebScraperService, IResultAnalyzer
from services.database_service import DatabaseService
from services.web_scraper_service import WebScraperService, ResultAnalyzer
from services.config_service import ConfigService
from services.logging_service import LoggingService
from services.validation_service import ValidationService

class SPVAutomatico:
    """
    Sistema de Pesquisa Virtual Automático seguindo princípios SOLID
    """
    
    def __init__(self, 
                 database_service: IDatabaseService,
                 web_scraper_service: IWebScraperService,
                 result_analyzer: IResultAnalyzer,
                 config_service: ConfigService,
                 logging_service: LoggingService,
                 validation_service: ValidationService,
                 filtro: int = 0):
        """
        Inicializa o sistema SPV com injeção de dependência
        
        Args:
            database_service: Serviço de banco de dados
            web_scraper_service: Serviço de web scraping
            result_analyzer: Analisador de resultados
            config_service: Serviço de configuração
            logging_service: Serviço de logging
            validation_service: Serviço de validação
            filtro: Tipo de filtro (0=CPF, 1=RG, 2=Nome, 3=RG alternativo)
        """
        self.database_service = database_service
        self.web_scraper_service = web_scraper_service
        self.result_analyzer = result_analyzer
        self.config_service = config_service
        self.logging_service = logging_service
        self.validation_service = validation_service
        self.filtro = filtro
        self.tempo_inicio = None
        self.logger = logging_service.get_logger(__name__)
        
    def executar_pesquisa(self, nome: str, cpf: str, rg: str, cod_pesquisa: int, 
                         spv_tipo: Optional[int] = None) -> bool:
        """
        Executa uma pesquisa específica
        
        Args:
            nome: Nome da pessoa
            cpf: CPF da pessoa
            rg: RG da pessoa
            cod_pesquisa: Código da pesquisa
            spv_tipo: Tipo de SPV
            
        Returns:
            True se a pesquisa foi executada com sucesso
        """
        try:
            tempo_inicio_pesquisa = time.time()
            
            # Valida o documento apropriado para o filtro
            validation_result = self.validation_service.validate_document_for_filter(
                self.filtro, cpf, rg, nome
            )
            
            if not validation_result.is_valid:
                self.logging_service.log_pesquisa_error(
                    self.logger, 
                    cod_pesquisa, 
                    f"{validation_result.error_message} | Valor recebido: CPF='{cpf}', RG='{rg}', Nome='{nome}'"
                )
                return False
            
            documento = validation_result.corrected_value
            
            # Loga início da pesquisa
            self.logging_service.log_pesquisa_start(self.logger, cod_pesquisa, documento)
            
            # Executa a pesquisa usando o web scraper
            page_source = self.web_scraper_service.pesquisar(self.filtro, documento)
            
            # Analisa o resultado
            resultado = self.result_analyzer.analisar_resultado(page_source)
            
            # Calcula tempo de execução
            tempo_execucao = round(time.time() - tempo_inicio_pesquisa, 2)
            
            # Salva o resultado no banco
            sucesso = self.database_service.salvar_resultado_spv(
                cod_pesquisa=cod_pesquisa,
                filtro=self.filtro,
                resultado=resultado,
                tempo_execucao=tempo_execucao
            )
            
            if sucesso:
                self.logging_service.log_pesquisa_success(
                    self.logger, 
                    cod_pesquisa, 
                    resultado, 
                    tempo_execucao
                )
                return True
            else:
                self.logging_service.log_pesquisa_error(
                    self.logger, 
                    cod_pesquisa, 
                    "Erro ao salvar resultado no banco"
                )
                return False
                
        except Exception as e:
            self.logging_service.log_pesquisa_error(self.logger, cod_pesquisa, str(e))
            return False
    
    def processar_pesquisas_pendentes(self, limit: int = 100) -> int:
        """
        Processa pesquisas pendentes com paginação
        
        Args:
            limit: Número máximo de pesquisas a processar por vez
            
        Returns:
            Número de pesquisas processadas
        """
        try:
            # Obtém pesquisas pendentes
            pesquisas = self.database_service.get_pesquisas_pendentes(
                filtro=self.filtro,
                limit=limit,
                offset=0
            )
            
            if not pesquisas:
                self.logger.info(f"Nenhuma pesquisa pendente encontrada para filtro {self.filtro}")
                return 0
            
            self.logger.info(f"Processando {len(pesquisas)} pesquisas com filtro {self.filtro}")
            
            # Processa cada pesquisa
            pesquisas_processadas = 0
            for pesquisa in tqdm(pesquisas, desc=f"Filtro {self.filtro}"):
                # Verifica se o tempo máximo foi atingido
                if self.tempo_inicio and (time.time() - self.tempo_inicio) >= self.config_service.scraping.max_execution_time:
                    self.logger.info("Tempo máximo de execução atingido")
                    break
                
                # Extrai dados da pesquisa
                cod_pesquisa = pesquisa[0]
                cod_cliente = pesquisa[1]
                nome_cliente = pesquisa[2]
                uf = pesquisa[3]
                data_entrada = pesquisa[4]
                nome = pesquisa[5]
                cpf = pesquisa[6]
                rg = pesquisa[7]
                nascimento = pesquisa[8]
                mae = pesquisa[9]
                anexo = pesquisa[10]
                resultado = pesquisa[11]
                spv_tipo = pesquisa[12]
                
                # Executa a pesquisa
                if self.executar_pesquisa(nome, cpf, rg, cod_pesquisa, spv_tipo):
                    pesquisas_processadas += 1
                
                # Pequena pausa entre pesquisas para não sobrecarregar o servidor
                time.sleep(self.config_service.scraping.delay_between_requests)
            
            self.logger.info(f"Processadas {pesquisas_processadas} pesquisas com filtro {self.filtro}")
            return pesquisas_processadas
            
        except Exception as e:
            self.logger.error(f"Erro ao processar pesquisas pendentes: {e}")
            return 0
    
    def executar_ciclo_completo(self) -> bool:
        """
        Executa um ciclo completo de pesquisas com todos os filtros
        
        Returns:
            True se o ciclo foi executado com sucesso
        """
        try:
            self.tempo_inicio = time.time()
            self.logging_service.log_execution_start(
                self.logger, 
                self.filtro, 
                self.config_service.scraping.website_type
            )
            
            # Executa com cada filtro
            for filtro in range(4):  # 0, 1, 2, 3
                self.filtro = filtro
                
                # Verifica se há pesquisas pendentes para este filtro
                count = self.database_service.get_pesquisas_por_filtro(filtro)
                if count == 0:
                    self.logger.info(f"Nenhuma pesquisa pendente para filtro {filtro}")
                    continue
                
                self.logger.info(f"Executando filtro {filtro} com {count} pesquisas pendentes")
                
                # Processa pesquisas pendentes
                pesquisas_processadas = self.processar_pesquisas_pendentes()
                
                if pesquisas_processadas > 0:
                    self.logger.info(f"Filtro {filtro} concluído: {pesquisas_processadas} pesquisas processadas")
                
                # Verifica se o tempo máximo foi atingido
                if (time.time() - self.tempo_inicio) >= self.config_service.scraping.max_execution_time:
                    self.logger.info("Tempo máximo de execução atingido")
                    break
            
            tempo_total = time.time() - self.tempo_inicio
            self.logging_service.log_execution_end(self.logger, 0, tempo_total)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao executar ciclo completo: {e}")
            return False
    
    def executar_loop_continuo(self, intervalo_espera: int = 60, max_tentativas: int = 20) -> None:
        """
        Executa o sistema em loop contínuo
        
        Args:
            intervalo_espera: Tempo de espera entre ciclos em segundos
            max_tentativas: Número máximo de tentativas em caso de erro
        """
        tentativas = 0
        
        while tentativas < max_tentativas:
            try:
                self.logger.info(f"Iniciando ciclo {tentativas + 1}/{max_tentativas}")
                
                sucesso = self.executar_ciclo_completo()
                
                if sucesso:
                    tentativas = 0  # Reset contador de tentativas em caso de sucesso
                    self.logger.info(f"Ciclo {tentativas + 1} concluído com sucesso")
                else:
                    tentativas += 1
                    self.logger.warning(f"Ciclo {tentativas} falhou")
                
                # Aguarda antes do próximo ciclo
                if tentativas < max_tentativas:
                    self.logger.info(f"Aguardando {intervalo_espera} segundos antes do próximo ciclo...")
                    time.sleep(intervalo_espera)
                
            except KeyboardInterrupt:
                self.logger.info("Execução interrompida pelo usuário")
                break
            except Exception as e:
                tentativas += 1
                self.logger.error(f"Erro crítico no ciclo {tentativas}: {e}")
                
                if tentativas < max_tentativas:
                    self.logger.info(f"Aguardando {intervalo_espera} segundos antes de tentar novamente...")
                    time.sleep(intervalo_espera)
        
        if tentativas >= max_tentativas:
            self.logger.error(f"Número máximo de tentativas ({max_tentativas}) atingido")
    
    def reiniciar_programa(self) -> None:
        """Reinicia o programa"""
        self.logger.info("Reiniciando programa...")
        python = sys.executable
        os.execl(python, python, *sys.argv)

def create_spv_automatico(config_service: ConfigService) -> SPVAutomatico:
    """
    Factory function para criar uma instância do SPVAutomatico
    Seguindo o princípio de inversão de dependência
    """
    # Inicializa serviços
    logging_service = LoggingService(config_service.logging)
    validation_service = ValidationService()
    
    # Obtém conexão com banco
    db = next(get_db())
    database_service = DatabaseService(db, logging_service)
    
    # Cria web scraper service
    web_scraper_service = WebScraperService(
        website_type=config_service.scraping.website_type,
        headless=config_service.webdriver.headless,
        driver_path=config_service.webdriver.driver_path,
        logging_service=logging_service
    )
    
    # Cria analisador de resultados
    result_analyzer = ResultAnalyzer()
    
    # Cria instância principal
    return SPVAutomatico(
        database_service=database_service,
        web_scraper_service=web_scraper_service,
        result_analyzer=result_analyzer,
        config_service=config_service,
        logging_service=logging_service,
        validation_service=validation_service
    )

def main():
    """Função principal"""
    try:
        # Carrega configuração
        config_service = ConfigService()
        
        # Loga configuração
        logging_service = LoggingService(config_service.logging)
        logger = logging_service.get_logger(__name__)
        
        config_info = {
            "website_type": config_service.scraping.website_type,
            "headless": config_service.webdriver.headless,
            "max_execution_time": config_service.scraping.max_execution_time
        }
        logging_service.log_configuration(logger, config_info)
        
        # Verifica modo de desenvolvimento
        if config_service.is_development_mode():
            logger.info("Executando em modo de desenvolvimento (sem web scraping)")
            return
        
        # Cria e executa o sistema
        spv = create_spv_automatico(config_service)
        spv.executar_ciclo_completo()
        
    except Exception as e:
        print(f"Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 