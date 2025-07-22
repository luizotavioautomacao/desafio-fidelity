from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Text, ForeignKey, DECIMAL, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.config.database import Base

class Estado(Base):
    __tablename__ = "estados"
    
    cod_uf = Column(Integer, primary_key=True, index=True)
    uf = Column(String(2), unique=True, nullable=False, index=True)
    cod_fornecedor = Column(Integer)
    nome = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Servico(Base):
    __tablename__ = "servicos"
    
    cod_servico = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    civel = Column(Boolean, default=False)
    criminal = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Cliente(Base):
    __tablename__ = "clientes"
    
    cod_cliente = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    cnpj = Column(String(18))
    cpf = Column(String(14))
    email = Column(String(100))
    telefone = Column(String(20))
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    pesquisas = relationship("Pesquisa", back_populates="cliente")

class Funcionario(Base):
    __tablename__ = "funcionarios"
    
    cod_funcionario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    email = Column(String(100))
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Lote(Base):
    __tablename__ = "lotes"
    
    cod_lote = Column(Integer, primary_key=True, index=True)
    cod_lote_prazo = Column(Integer)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    cod_funcionario = Column(Integer, ForeignKey("funcionarios.cod_funcionario"))
    tipo = Column(String(50))
    prioridade = Column(Integer, default=1)
    status = Column(String(20), default="ABERTO")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Pesquisa(Base):
    __tablename__ = "pesquisas"
    
    cod_pesquisa = Column(Integer, primary_key=True, index=True)
    cod_cliente = Column(Integer, ForeignKey("clientes.cod_cliente"))
    cod_uf = Column(Integer, ForeignKey("estados.cod_uf"))
    cod_servico = Column(Integer, ForeignKey("servicos.cod_servico"))
    tipo = Column(Integer, default=0)  # 0: Normal, 1: Urgente, etc.
    cpf = Column(String(14), index=True)
    cod_uf_nascimento = Column(Integer, ForeignKey("estados.cod_uf"))
    cod_uf_rg = Column(Integer, ForeignKey("estados.cod_uf"))
    data_entrada = Column(DateTime(timezone=True), server_default=func.now())
    data_conclusao = Column(DateTime(timezone=True))
    nome = Column(String(200), index=True)
    nome_corrigido = Column(String(200))
    rg = Column(String(20), index=True)
    rg_corrigido = Column(String(20))
    nascimento = Column(Date)
    mae = Column(String(200))
    mae_corrigido = Column(String(200))
    anexo = Column(Text)
    status = Column(String(20), default="PENDENTE", index=True)
    prioridade = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="pesquisas")
    pesquisa_spv = relationship("PesquisaSPV", back_populates="pesquisa")

class LotePesquisa(Base):
    __tablename__ = "lote_pesquisas"
    
    cod_lote_pesquisa = Column(Integer, primary_key=True, index=True)
    cod_lote = Column(Integer, ForeignKey("lotes.cod_lote"), index=True)
    cod_pesquisa = Column(Integer, ForeignKey("pesquisas.cod_pesquisa"), index=True)
    cod_funcionario = Column(Integer, ForeignKey("funcionarios.cod_funcionario"))
    cod_funcionario_conclusao = Column(Integer, ForeignKey("funcionarios.cod_funcionario"))
    cod_fornecedor = Column(Integer)
    data_entrada = Column(DateTime(timezone=True), server_default=func.now())
    data_conclusao = Column(DateTime(timezone=True))
    cod_uf = Column(Integer, ForeignKey("estados.cod_uf"))
    obs = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class PesquisaSPV(Base):
    __tablename__ = "pesquisa_spv"
    
    cod_pesquisa_spv = Column(Integer, primary_key=True, index=True)
    cod_pesquisa = Column(Integer, ForeignKey("pesquisas.cod_pesquisa"), index=True)
    cod_spv = Column(Integer, default=1)
    cod_spv_computador = Column(Integer)
    cod_spv_tipo = Column(Integer)
    cod_funcionario = Column(Integer, ForeignKey("funcionarios.cod_funcionario"))
    filtro = Column(Integer, nullable=False, index=True)  # 0: CPF, 1: RG, 2: Nome, 3: RG alternativo
    website_id = Column(Integer, default=1)
    resultado = Column(Integer, index=True)  # 1: Nada consta, 2: Criminal, 5: Cível, 7: Erro
    data_execucao = Column(DateTime(timezone=True), server_default=func.now())
    tempo_execucao = Column(DECIMAL(10, 2))
    erro = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    pesquisa = relationship("Pesquisa", back_populates="pesquisa_spv")

class Website(Base):
    __tablename__ = "websites"
    
    website_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    url = Column(String(500), nullable=False)
    tipo = Column(String(50))  # TJSP, TJRJ, etc.
    ativo = Column(Boolean, default=True)
    configuracao = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 