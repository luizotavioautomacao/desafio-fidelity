import time
import logging
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from abc import ABC, abstractmethod
import json
from interfaces.web_scraper_interface import IWebScraperService, IResultAnalyzer
from services.logging_service import LoggingService

class WebScraperBase(ABC):
    """Classe base abstrata para web scrapers"""
    
    def __init__(self, headless: bool = True, timeout: int = 30, logging_service: LoggingService = None):
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.logging_service = logging_service
        self.logger = logging_service.get_logger(__name__) if logging_service else logging.getLogger(__name__)
        
    def setup_driver(self, driver_path: str = None) -> webdriver.Edge:
        """Configura o driver do Edge"""
        try:
            service = Service(executable_path=driver_path) if driver_path else Service()
            options = Options()
            
            if self.headless:
                options.add_argument("-headless")
            
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            self.driver = webdriver.Edge(service=service, options=options)
            self.driver.implicitly_wait(10)
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar driver: {e}")
            raise
    
    def close_driver(self):
        """Fecha o driver"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                self.logger.error(f"Erro ao fechar driver: {e}")
    
    @abstractmethod
    def pesquisar_por_cpf(self, cpf: str) -> str:
        """Pesquisa por CPF"""
        pass
    
    @abstractmethod
    def pesquisar_por_rg(self, rg: str) -> str:
        """Pesquisa por RG"""
        pass
    
    @abstractmethod
    def pesquisar_por_nome(self, nome: str) -> str:
        """Pesquisa por nome"""
        pass
    
    def wait_for_element(self, by: By, value: str, timeout: int = None) -> Optional[Any]:
        """Aguarda elemento aparecer na página"""
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.warning(f"Elemento não encontrado: {value}")
            return None

class TJSPWebScraper(WebScraperBase):
    """Web scraper específico para o TJSP"""
    
    def __init__(self, headless: bool = True, logging_service: LoggingService = None):
        super().__init__(headless, logging_service=logging_service)
        self.base_url = "https://esaj.tjsp.jus.br/cpopg/open.do"
        self.selectors = {
            "tipo_pesquisa": "//*[@id=\"cbPesquisa\"]",
            "campo_cpf": "//*[@id=\"campo_DOCPARTE\"]",
            "campo_nome": "//*[@id=\"campo_NMPARTE\"]",
            "botao_consultar": "//*[@id=\"botaoConsultarProcessos\"]",
            "pesquisar_por_nome": "//*[@id=\"pesquisarPorNomeCompleto\"]"
        }
    
    def pesquisar_por_cpf(self, cpf: str) -> str:
        """Pesquisa por CPF no TJSP"""
        try:
            self.driver.get(self.base_url)
            
            # Seleciona tipo de pesquisa
            select_element = self.wait_for_element(By.XPATH, self.selectors["tipo_pesquisa"])
            if not select_element:
                raise Exception("Elemento de seleção de tipo não encontrado")
            
            select = Select(select_element)
            select.select_by_value('DOCPARTE')
            
            # Preenche CPF
            campo_cpf = self.wait_for_element(By.XPATH, self.selectors["campo_cpf"])
            if not campo_cpf:
                raise Exception("Campo CPF não encontrado")
            
            campo_cpf.clear()
            campo_cpf.send_keys(cpf)
            
            # Clica em consultar
            botao_consultar = self.wait_for_element(By.XPATH, self.selectors["botao_consultar"])
            if not botao_consultar:
                raise Exception("Botão consultar não encontrado")
            
            botao_consultar.click()
            
            # Aguarda carregamento da página
            time.sleep(3)
            
            return self.driver.page_source
            
        except Exception as e:
            self.logger.error(f"Erro na pesquisa por CPF: {e}")
            return ""
    
    def pesquisar_por_rg(self, rg: str) -> str:
        """Pesquisa por RG no TJSP (mesmo que CPF)"""
        return self.pesquisar_por_cpf(rg)
    
    def pesquisar_por_nome(self, nome: str) -> str:
        """Pesquisa por nome no TJSP"""
        try:
            self.driver.get(self.base_url)
            
            # Seleciona tipo de pesquisa
            select_element = self.wait_for_element(By.XPATH, self.selectors["tipo_pesquisa"])
            if not select_element:
                raise Exception("Elemento de seleção de tipo não encontrado")
            
            select = Select(select_element)
            select.select_by_value('NMPARTE')
            
            # Clica em pesquisar por nome completo
            pesquisar_nome = self.wait_for_element(By.XPATH, self.selectors["pesquisar_por_nome"])
            if not pesquisar_nome:
                raise Exception("Botão pesquisar por nome não encontrado")
            
            pesquisar_nome.click()
            
            # Preenche nome
            campo_nome = self.wait_for_element(By.XPATH, self.selectors["campo_nome"])
            if not campo_nome:
                raise Exception("Campo nome não encontrado")
            
            campo_nome.clear()
            campo_nome.send_keys(nome)
            
            # Clica em consultar
            botao_consultar = self.wait_for_element(By.XPATH, self.selectors["botao_consultar"])
            if not botao_consultar:
                raise Exception("Botão consultar não encontrado")
            
            botao_consultar.click()
            
            # Aguarda carregamento da página
            time.sleep(3)
            
            return self.driver.page_source
            
        except Exception as e:
            self.logger.error(f"Erro na pesquisa por nome: {e}")
            return ""

class WebScraperFactory:
    """Factory para criar web scrapers específicos"""
    
    @staticmethod
    def create_scraper(website_type: str, headless: bool = True, logging_service: LoggingService = None) -> WebScraperBase:
        """Cria um web scraper baseado no tipo de website"""
        if website_type.upper() == "TJSP":
            return TJSPWebScraper(headless, logging_service)
        else:
            raise ValueError(f"Tipo de website não suportado: {website_type}")

class WebScraperService(IWebScraperService):
    """Serviço principal de web scraping"""
    
    def __init__(self, website_type: str = "TJSP", headless: bool = True, driver_path: str = None, logging_service: LoggingService = None):
        self.website_type = website_type
        self.headless = headless
        self.driver_path = driver_path
        self.scraper = None
        self.logging_service = logging_service
        self.logger = logging_service.get_logger(__name__) if logging_service else logging.getLogger(__name__)
    
    def setup_driver(self) -> None:
        """Configura o driver do navegador"""
        try:
            self.scraper = WebScraperFactory.create_scraper(
                self.website_type, 
                self.headless, 
                self.logging_service
            )
            self.scraper.setup_driver(self.driver_path)
        except Exception as e:
            self.logger.error(f"Erro ao configurar driver: {e}")
            raise
    
    def close_driver(self) -> None:
        """Fecha o driver do navegador"""
        if self.scraper:
            self.scraper.close_driver()
    
    def pesquisar(self, filtro: int, documento: str) -> str:
        """Executa uma pesquisa no website do tribunal"""
        try:
            if not self.scraper:
                # Configura o driver automaticamente se não estiver configurado
                self.setup_driver()
            
            if filtro == 0:  # CPF
                return self.scraper.pesquisar_por_cpf(documento)
            elif filtro in [1, 3]:  # RG
                return self.scraper.pesquisar_por_rg(documento)
            elif filtro == 2:  # Nome
                return self.scraper.pesquisar_por_nome(documento)
            else:
                raise ValueError(f"Filtro {filtro} não suportado")
                
        except Exception as e:
            self.logger.error(f"Erro na pesquisa: {e}")
            return ""
    
    def __enter__(self):
        """Context manager entry"""
        self.setup_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_driver()

class ResultAnalyzer(IResultAnalyzer):
    """Analisador de resultados das pesquisas"""
    
    # Constantes para resultados
    NADA_CONSTA = 'Não existem informações disponíveis para os parâmetros informados.'
    CONSTA01 = 'Processos encontrados'
    CONSTA02 = 'Audiências'
    
    @staticmethod
    def analisar_resultado(page_source: str) -> int:
        """
        Analisa o resultado da pesquisa e retorna o código do resultado
        
        Returns:
            1: Nada consta
            2: Criminal
            5: Cível
            7: Erro
        """
        try:
            if not page_source:
                return 7  # Erro
            
            # Verifica se não há resultados
            if ResultAnalyzer.NADA_CONSTA in page_source:
                return 1  # Nada consta
            
            # Verifica se há processos
            if ResultAnalyzer.CONSTA01 in page_source:
                # Aqui você pode implementar lógica mais sofisticada
                # para determinar se é criminal ou cível baseado no conteúdo
                # Por enquanto, retorna cível como padrão
                return 5  # Cível
            
            # Verifica se há audiências
            if ResultAnalyzer.CONSTA02 in page_source:
                return 5  # Cível
            
            # Se chegou até aqui, assume que há algo mas não conseguiu classificar
            return 5  # Cível (padrão)
            
        except Exception as e:
            logging.getLogger(__name__).error(f"Erro ao analisar resultado: {e}")
            return 7  # Erro 