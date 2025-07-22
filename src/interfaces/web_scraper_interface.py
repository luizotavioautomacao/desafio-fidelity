from abc import ABC, abstractmethod
from typing import Optional, ContextManager

class IWebScraperService(ABC):
    """Interface para serviços de web scraping"""
    
    @abstractmethod
    def pesquisar(self, filtro: int, documento: str) -> str:
        """Executa uma pesquisa no website do tribunal"""
        pass
    
    @abstractmethod
    def setup_driver(self) -> None:
        """Configura o driver do navegador"""
        pass
    
    @abstractmethod
    def close_driver(self) -> None:
        """Fecha o driver do navegador"""
        pass
    
    def __enter__(self):
        """Context manager entry"""
        self.setup_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_driver()

class IResultAnalyzer(ABC):
    """Interface para análise de resultados"""
    
    @abstractmethod
    def analisar_resultado(self, page_source: str) -> int:
        """Analisa o resultado da pesquisa e retorna o código do resultado"""
        pass 