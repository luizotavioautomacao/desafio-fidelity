import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# Carrega variáveis do arquivo .env
load_dotenv()

# Verifica todas as variáveis obrigatórias
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_POOL_SIZE = os.getenv("DB_POOL_SIZE")
DB_MAX_OVERFLOW = os.getenv("DB_MAX_OVERFLOW")
DB_POOL_PRE_PING = os.getenv("DB_POOL_PRE_PING")
DB_POOL_RECYCLE = os.getenv("DB_POOL_RECYCLE")

required_vars = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME,
    "DB_POOL_SIZE": DB_POOL_SIZE,
    "DB_MAX_OVERFLOW": DB_MAX_OVERFLOW,
    "DB_POOL_PRE_PING": DB_POOL_PRE_PING,
    "DB_POOL_RECYCLE": DB_POOL_RECYCLE,
}

missing_vars = [k for k, v in required_vars.items() if not v]
if missing_vars:
    raise ValueError(f"❌ Variáveis obrigatórias ausentes no .env: {', '.join(missing_vars)}")

# Monta a URL de conexão
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criação do engine com parâmetros de performance
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=int(DB_POOL_SIZE),
    max_overflow=int(DB_MAX_OVERFLOW),
    pool_pre_ping=DB_POOL_PRE_PING.lower() == "true",
    pool_recycle=int(DB_POOL_RECYCLE),
    echo=False
)

# Criação da fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def get_db():
    """Fornece uma sessão do banco para uso em rotinas"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Cria todas as tabelas no banco com base nos modelos declarados"""
    Base.metadata.create_all(bind=engine)
