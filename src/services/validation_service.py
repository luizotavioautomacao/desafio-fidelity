import re
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass
from interfaces.validation_result import ValidationResult

class ValidationService:
    """Serviço de validação de dados"""
    
    def __init__(self):
        self.cpf_pattern = re.compile(r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$')
        self.rg_pattern = re.compile(r'^\d{1,2}\.?\d{3}\.?\d{3}-?\d{1}$')
        self.nome_pattern = re.compile(r'^[a-zA-ZÀ-ÿ\s]+$')
    
    def validate_cpf(self, cpf: str) -> ValidationResult:
        """Valida um CPF"""
        if not cpf:
            return ValidationResult(False, "CPF não pode estar vazio")
        
        # Remove caracteres especiais
        cpf_clean = re.sub(r'[^\d]', '', cpf)
        
        if len(cpf_clean) != 11:
            return ValidationResult(False, "CPF deve ter 11 dígitos")
        
        # Verifica se todos os dígitos são iguais
        if cpf_clean == cpf_clean[0] * 11:
            return ValidationResult(False, "CPF inválido")
        
        # Validação dos dígitos verificadores
        if not self._validate_cpf_digits(cpf_clean):
            return ValidationResult(False, "CPF inválido")
        
        # Formata o CPF
        formatted_cpf = f"{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}"
        
        return ValidationResult(True, corrected_value=formatted_cpf)
    
    def _validate_cpf_digits(self, cpf: str) -> bool:
        """Valida os dígitos verificadores do CPF"""
        # Primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        if int(cpf[9]) != digito1:
            return False
        
        # Segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        return int(cpf[10]) == digito2
    
    def validate_rg(self, rg: str) -> ValidationResult:
        """Valida um RG"""
        if not rg:
            return ValidationResult(False, "RG não pode estar vazio")
        
        # Remove caracteres especiais
        rg_clean = re.sub(r'[^\d]', '', rg)
        
        if len(rg_clean) < 8 or len(rg_clean) > 9:
            return ValidationResult(False, "RG deve ter 8 ou 9 dígitos")
        
        # Formata o RG
        if len(rg_clean) == 8:
            formatted_rg = f"{rg_clean[:1]}.{rg_clean[1:4]}.{rg_clean[4:7]}-{rg_clean[7:]}"
        else:
            formatted_rg = f"{rg_clean[:2]}.{rg_clean[2:5]}.{rg_clean[5:8]}-{rg_clean[8:]}"
        
        return ValidationResult(True, corrected_value=formatted_rg)
    
    def validate_nome(self, nome: str) -> ValidationResult:
        """Valida um nome"""
        if not nome:
            return ValidationResult(False, "Nome não pode estar vazio")
        
        if len(nome.strip()) < 2:
            return ValidationResult(False, "Nome deve ter pelo menos 2 caracteres")
        
        if not self.nome_pattern.match(nome):
            return ValidationResult(False, "Nome contém caracteres inválidos")
        
        # Capitaliza o nome
        corrected_nome = nome.strip().title()
        
        return ValidationResult(True, corrected_value=corrected_nome)
    
    def validate_document_for_filter(self, filtro: int, cpf: str, rg: str, nome: str) -> ValidationResult:
        """Valida o documento apropriado para o filtro especificado"""
        if filtro == 0:  # CPF
            return self.validate_cpf(cpf)
        elif filtro in [1, 3]:  # RG
            return self.validate_rg(rg)
        elif filtro == 2:  # Nome
            return self.validate_nome(nome)
        else:
            return ValidationResult(False, f"Filtro {filtro} não suportado")
    
    def validate_pesquisa_data(self, pesquisa_data: Dict[str, Any]) -> ValidationResult:
        """Valida dados completos de uma pesquisa"""
        required_fields = ['cod_pesquisa', 'nome', 'cpf', 'rg']
        
        for field in required_fields:
            if field not in pesquisa_data:
                return ValidationResult(False, f"Campo obrigatório '{field}' não encontrado")
        
        if not pesquisa_data['cod_pesquisa']:
            return ValidationResult(False, "Código da pesquisa não pode estar vazio")
        
        return ValidationResult(True)
    
    def sanitize_document(self, documento: str) -> str:
        """Remove caracteres especiais de um documento"""
        if not documento:
            return ""
        return re.sub(r'[^\w\s]', '', documento).strip() 