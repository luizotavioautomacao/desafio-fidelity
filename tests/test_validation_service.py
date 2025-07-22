import pytest
from src.services.validation_service import ValidationService, ValidationResult

class TestValidationService:
    """Testes para o serviço de validação"""
    
    @pytest.fixture
    def validation_service(self):
        """Fixture para criar instância do serviço de validação"""
        return ValidationService()
    
    def test_validate_cpf_valid(self, validation_service):
        """Testa validação de CPF válido"""
        cpf = "123.456.789-09"
        result = validation_service.validate_cpf(cpf)
        
        assert result.is_valid is True
        assert result.corrected_value == "123.456.789-09"
        assert result.error_message is None
    
    def test_validate_cpf_invalid(self, validation_service):
        """Testa validação de CPF inválido"""
        cpf = "123.456.789-10"
        result = validation_service.validate_cpf(cpf)
        
        assert result.is_valid is False
        assert "CPF inválido" in result.error_message
    
    def test_validate_cpf_empty(self, validation_service):
        """Testa validação de CPF vazio"""
        result = validation_service.validate_cpf("")
        
        assert result.is_valid is False
        assert "CPF não pode estar vazio" in result.error_message
    
    def test_validate_rg_valid(self, validation_service):
        """Testa validação de RG válido"""
        rg = "12.345.678-9"
        result = validation_service.validate_rg(rg)
        
        assert result.is_valid is True
        assert result.corrected_value == "12.345.678-9"
    
    def test_validate_nome_valid(self, validation_service):
        """Testa validação de nome válido"""
        nome = "João Silva"
        result = validation_service.validate_nome(nome)
        
        assert result.is_valid is True
        assert result.corrected_value == "João Silva"
    
    def test_validate_nome_invalid(self, validation_service):
        """Testa validação de nome inválido"""
        nome = "João123"
        result = validation_service.validate_nome(nome)
        
        assert result.is_valid is False
        assert "caracteres inválidos" in result.error_message
    
    def test_validate_document_for_filter_cpf(self, validation_service):
        """Testa validação de documento para filtro CPF"""
        result = validation_service.validate_document_for_filter(
            filtro=0, cpf="123.456.789-09", rg="", nome=""
        )
        
        assert result.is_valid is True
        assert result.corrected_value == "123.456.789-09"
    
    def test_validate_document_for_filter_rg(self, validation_service):
        """Testa validação de documento para filtro RG"""
        result = validation_service.validate_document_for_filter(
            filtro=1, cpf="", rg="12.345.678-9", nome=""
        )
        
        assert result.is_valid is True
        assert result.corrected_value == "12.345.678-9"
    
    def test_validate_document_for_filter_nome(self, validation_service):
        """Testa validação de documento para filtro Nome"""
        result = validation_service.validate_document_for_filter(
            filtro=2, cpf="", rg="", nome="João Silva"
        )
        
        assert result.is_valid is True
        assert result.corrected_value == "João Silva"
    
    def test_validate_document_for_filter_invalid(self, validation_service):
        """Testa validação de documento para filtro inválido"""
        result = validation_service.validate_document_for_filter(
            filtro=99, cpf="", rg="", nome=""
        )
        
        assert result.is_valid is False
        assert "Filtro 99 não suportado" in result.error_message
    
    def test_sanitize_document(self, validation_service):
        """Testa sanitização de documento"""
        documento = "123.456.789-09"
        sanitized = validation_service.sanitize_document(documento)
        
        assert sanitized == "12345678909"
    
    def test_sanitize_document_empty(self, validation_service):
        """Testa sanitização de documento vazio"""
        sanitized = validation_service.sanitize_document("")
        
        assert sanitized == "" 