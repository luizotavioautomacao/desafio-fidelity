import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from services.database_service import DatabaseService

class TestDatabaseService:
    
    @pytest.fixture
    def mock_db(self):
        """Mock da sessão do banco de dados"""
        return Mock()
    
    @pytest.fixture
    def db_service(self, mock_db):
        """Instância do DatabaseService com mock"""
        mock_logging = Mock()
        return DatabaseService(mock_db, mock_logging)
    
    def test_get_pesquisas_pendentes(self, db_service, mock_db):
        """Testa obtenção de pesquisas pendentes"""
        # Mock dos dados retornados
        mock_result = [
            (1, 100, 'Cliente Teste', 'SP', datetime.now(), 'João Silva', '123.456.789-00', '12.345.678-9', None, 'Maria Silva', None, None, None)
        ]
        mock_db.execute.return_value.fetchall.return_value = mock_result
        
        # Executa o teste
        result = db_service.get_pesquisas_pendentes(filtro=0, limit=10, offset=0)
        
        # Verifica se a função foi chamada
        mock_db.execute.assert_called_once()
        assert len(result) == 1
        assert result[0][1] == 100  # cod_pesquisa
    
    def test_salvar_resultado_spv_novo(self, db_service, mock_db):
        """Testa salvamento de novo resultado SPV"""
        # Mock para pesquisa não existente
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Executa o teste
        result = db_service.salvar_resultado_spv(
            cod_pesquisa=100,
            filtro=0,
            resultado=1,
            tempo_execucao=2.5
        )
        
        # Verifica se foi bem-sucedido
        assert result is True
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    def test_salvar_resultado_spv_existente(self, db_service, mock_db):
        """Testa atualização de resultado SPV existente"""
        # Mock para pesquisa existente
        mock_pesquisa_spv = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_pesquisa_spv
        
        # Executa o teste
        result = db_service.salvar_resultado_spv(
            cod_pesquisa=100,
            filtro=0,
            resultado=2,
            tempo_execucao=3.0
        )
        
        # Verifica se foi bem-sucedido
        assert result is True
        assert mock_pesquisa_spv.resultado == 2
        assert mock_pesquisa_spv.tempo_execucao == 3.0
        mock_db.commit.assert_called_once()
    
    def test_marcar_pesquisa_concluida(self, db_service, mock_db):
        """Testa marcação de pesquisa como concluída"""
        # Mock para pesquisa existente
        mock_pesquisa = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_pesquisa
        
        # Executa o teste
        result = db_service.marcar_pesquisa_concluida(cod_pesquisa=100)
        
        # Verifica se foi bem-sucedido
        assert result is True
        assert mock_pesquisa.status == 'CONCLUIDA'
        assert mock_pesquisa.data_conclusao is not None
        mock_db.commit.assert_called_once()
    
    def test_marcar_pesquisa_concluida_nao_encontrada(self, db_service, mock_db):
        """Testa marcação de pesquisa não encontrada"""
        # Mock para pesquisa não existente
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Executa o teste
        result = db_service.marcar_pesquisa_concluida(cod_pesquisa=999)
        
        # Verifica se retornou False
        assert result is False
        mock_db.commit.assert_not_called()
    
    def test_get_estatisticas_pesquisas(self, db_service, mock_db):
        """Testa obtenção de estatísticas"""
        # Mock das contagens
        mock_db.query.return_value.filter.return_value.count.side_effect = [10, 20, 5, 3, 2]
        
        # Executa o teste
        result = db_service.get_estatisticas_pesquisas()
        
        # Verifica o resultado
        expected = {
            "pendentes": 10,
            "concluidas": 20,
            "nada_consta": 5,
            "criminal": 3,
            "civel": 2,
            "total": 30
        }
        assert result == expected
    
    def test_get_pesquisas_por_filtro(self, db_service, mock_db):
        """Testa contagem de pesquisas por filtro"""
        # Mock do execute().scalar() para retornar 15
        mock_db.execute.return_value.scalar.return_value = 15
        
        # Executa o teste
        result = db_service.get_pesquisas_por_filtro(filtro=0)
        
        # Verifica o resultado
        assert result == 15
    
    def test_erro_na_consulta(self, db_service, mock_db):
        """Testa tratamento de erro na consulta"""
        # Mock de erro
        mock_db.execute.side_effect = Exception("Erro de banco")
        
        # Executa o teste
        result = db_service.get_pesquisas_pendentes()
        
        # Verifica se retorna lista vazia em caso de erro
        assert result == []
    
    def test_erro_ao_salvar(self, db_service, mock_db):
        """Testa tratamento de erro ao salvar"""
        # Mock de erro
        mock_db.commit.side_effect = Exception("Erro ao salvar")
        
        # Executa o teste
        result = db_service.salvar_resultado_spv(
            cod_pesquisa=100,
            filtro=0,
            resultado=1
        )
        
        # Verifica se retorna False em caso de erro
        assert result is False
        mock_db.rollback.assert_called_once() 