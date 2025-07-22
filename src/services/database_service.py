from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, or_
from src.models.models import Pesquisa, PesquisaSPV, Cliente, Estado, Servico
from src.interfaces.database_interface import IDatabaseService
from src.services.logging_service import LoggingService
from datetime import datetime
import logging

class DatabaseService(IDatabaseService):
    """Implementação do serviço de banco de dados"""
    
    def __init__(self, db: Session, logging_service: LoggingService):
        self.db = db
        self.logging_service = logging_service
        self.logger = logging_service.get_logger(__name__)

    def get_pesquisas_pendentes(
        self, 
        filtro: int = 0, 
        limit: int = 100, 
        offset: int = 0
    ) -> List[Tuple]:
        """
        Obtém pesquisas pendentes com paginação usando a função do PostgreSQL
        """
        try:
            # Usando a função PostgreSQL criada no schema
            query = text("""
                SELECT * FROM get_pesquisas_pendentes(:filtro, :limit, :offset)
            """)
            
            result = self.db.execute(query, {
                "filtro": filtro,
                "limit": limit,
                "offset": offset
            })
            
            return result.fetchall()
            
        except Exception as e:
            self.logging_service.log_database_error(
                self.logger, 
                "get_pesquisas_pendentes", 
                str(e)
            )
            return []

    def get_pesquisas_pendentes_alternative(
        self, 
        filtro: int = 0, 
        limit: int = 100, 
        offset: int = 0
    ) -> List[Pesquisa]:
        """
        Alternativa usando SQLAlchemy ORM para buscar pesquisas pendentes
        """
        try:
            # Construindo a query base
            query = self.db.query(Pesquisa).join(
                Cliente, Pesquisa.cod_cliente == Cliente.cod_cliente
            ).join(
                Estado, Pesquisa.cod_uf == Estado.cod_uf
            ).join(
                Servico, Pesquisa.cod_servico == Servico.cod_servico
            ).outerjoin(
                PesquisaSPV, and_(
                    PesquisaSPV.cod_pesquisa == Pesquisa.cod_pesquisa,
                    PesquisaSPV.cod_spv == 1,
                    PesquisaSPV.filtro == filtro
                )
            )

            # Aplicando filtros
            query = query.filter(
                Pesquisa.data_conclusao.is_(None),
                PesquisaSPV.resultado.is_(None),
                Pesquisa.tipo == 0,
                Pesquisa.cpf.isnot(None),
                Pesquisa.cpf != '',
                or_(
                    Estado.uf == 'SP',
                    Pesquisa.cod_uf_nascimento == 26,
                    Pesquisa.cod_uf_rg == 26
                )
            )

            # Filtros específicos baseados no tipo de filtro
            if filtro in [1, 3]:
                query = query.filter(
                    Pesquisa.rg.isnot(None),
                    Pesquisa.rg != ''
                )

            # Ordenação e paginação
            query = query.order_by(Pesquisa.nome.asc(), PesquisaSPV.resultado.desc())
            query = query.limit(limit).offset(offset)

            return query.all()

        except Exception as e:
            self.logging_service.log_database_error(
                self.logger, 
                "get_pesquisas_pendentes_alternative", 
                str(e)
            )
            return []

    def salvar_resultado_spv(
        self, 
        cod_pesquisa: int, 
        filtro: int, 
        resultado: int, 
        tempo_execucao: float = None,
        erro: str = None
    ) -> bool:
        """
        Salva o resultado de uma pesquisa SPV
        """
        try:
            # Verifica se já existe um registro para esta pesquisa e filtro
            pesquisa_spv = self.db.query(PesquisaSPV).filter(
                and_(
                    PesquisaSPV.cod_pesquisa == cod_pesquisa,
                    PesquisaSPV.cod_spv == 1,
                    PesquisaSPV.filtro == filtro
                )
            ).first()

            if pesquisa_spv:
                # Atualiza o registro existente
                pesquisa_spv.resultado = resultado
                pesquisa_spv.tempo_execucao = tempo_execucao
                pesquisa_spv.erro = erro
                pesquisa_spv.data_execucao = datetime.now()
            else:
                # Cria um novo registro
                pesquisa_spv = PesquisaSPV(
                    cod_pesquisa=cod_pesquisa,
                    cod_spv=1,
                    cod_spv_computador=36,  # Valor padrão do código original
                    cod_spv_tipo=None,
                    cod_funcionario=1,  # Sistema automático - usando funcionário existente
                    filtro=filtro,
                    website_id=1,
                    resultado=resultado,
                    tempo_execucao=tempo_execucao,
                    erro=erro
                )
                self.db.add(pesquisa_spv)

            self.db.commit()
            return True

        except Exception as e:
            self.logging_service.log_database_error(
                self.logger, 
                "salvar_resultado_spv", 
                str(e)
            )
            self.db.rollback()
            return False

    def marcar_pesquisa_concluida(self, cod_pesquisa: int) -> bool:
        """
        Marca uma pesquisa como concluída
        """
        try:
            pesquisa = self.db.query(Pesquisa).filter(
                Pesquisa.cod_pesquisa == cod_pesquisa
            ).first()

            if pesquisa:
                pesquisa.data_conclusao = datetime.now()
                pesquisa.status = 'CONCLUIDA'
                self.db.commit()
                return True

            return False

        except Exception as e:
            self.logging_service.log_database_error(
                self.logger, 
                "marcar_pesquisa_concluida", 
                str(e)
            )
            self.db.rollback()
            return False

    def get_estatisticas_pesquisas(self) -> Dict[str, Any]:
        """
        Retorna estatísticas das pesquisas
        """
        try:
            total_pendentes = self.db.query(Pesquisa).filter(
                Pesquisa.data_conclusao.is_(None)
            ).count()

            total_concluidas = self.db.query(Pesquisa).filter(
                Pesquisa.data_conclusao.isnot(None)
            ).count()

            nada_consta = self.db.query(PesquisaSPV).filter(
                PesquisaSPV.resultado == 1
            ).count()

            criminal = self.db.query(PesquisaSPV).filter(
                PesquisaSPV.resultado == 2
            ).count()

            civel = self.db.query(PesquisaSPV).filter(
                PesquisaSPV.resultado == 5
            ).count()

            return {
                "pendentes": total_pendentes,
                "concluidas": total_concluidas,
                "nada_consta": nada_consta,
                "criminal": criminal,
                "civel": civel,
                "total": total_pendentes + total_concluidas
            }

        except Exception as e:
            self.logging_service.log_database_error(
                self.logger, 
                "get_estatisticas_pesquisas", 
                str(e)
            )
            return {
                "pendentes": 0,
                "concluidas": 0,
                "nada_consta": 0,
                "criminal": 0,
                "civel": 0,
                "total": 0
            }

    def get_pesquisas_por_filtro(self, filtro: int) -> int:
        """
        Retorna o número de pesquisas pendentes por filtro
        """
        try:
            query = text("""
                SELECT COUNT(*) FROM get_pesquisas_pendentes(:filtro, 1000000, 0)
            """)
            
            result = self.db.execute(query, {"filtro": filtro})
            return result.scalar() or 0
            
        except Exception as e:
            self.logging_service.log_database_error(
                self.logger, 
                "get_pesquisas_por_filtro", 
                str(e)
            )
            return 0 