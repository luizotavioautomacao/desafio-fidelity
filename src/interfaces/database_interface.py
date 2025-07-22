from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

class IDatabaseService(ABC):
    """Interface para serviços de banco de dados"""
    
    @abstractmethod
    def get_pesquisas_pendentes(
        self, 
        filtro: int = 0, 
        limit: int = 100, 
        offset: int = 0
    ) -> List[Tuple]:
        """Obtém pesquisas pendentes com paginação"""
        pass
    
    @abstractmethod
    def salvar_resultado_spv(
        self, 
        cod_pesquisa: int, 
        filtro: int, 
        resultado: int, 
        tempo_execucao: float = None,
        erro: str = None
    ) -> bool:
        """Salva o resultado de uma pesquisa SPV"""
        pass
    
    @abstractmethod
    def marcar_pesquisa_concluida(self, cod_pesquisa: int) -> bool:
        """Marca uma pesquisa como concluída"""
        pass
    
    @abstractmethod
    def get_estatisticas_pesquisas(self) -> Dict[str, Any]:
        """Retorna estatísticas das pesquisas"""
        pass
    
    @abstractmethod
    def get_pesquisas_por_filtro(self, filtro: int) -> int:
        """Retorna o número de pesquisas pendentes por filtro"""
        pass 