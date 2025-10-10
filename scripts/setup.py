#!/usr/bin/env python3
"""
Script de Setup para o Sistema de Pesquisa Virtual Automático (SPV)

Este script automatiza o processo de instalação e configuração inicial
do sistema SPV.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header():
    """Imprime o cabeçalho do setup"""
    print("=" * 60)
    print("🚀 Sistema de Pesquisa Virtual Automático - Setup")
    print("=" * 60)

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print("📋 Verificando versão do Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def create_virtual_environment():
    """Cria ambiente virtual"""
    print("\n🐍 Criando ambiente virtual...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("⚠️  Ambiente virtual já existe")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Ambiente virtual criado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar ambiente virtual: {e}")
        return False

def install_dependencies():
    """Instala as dependências"""
    print("\n📦 Instalando dependências...")
    
    # Determina o comando pip correto
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Linux/Mac
        pip_cmd = "venv/bin/pip"
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def setup_database():
    """Configura o banco de dados"""
    print("\n🗄️ Configurando banco de dados...")
    
    # Verifica se PostgreSQL está instalado
    try:
        subprocess.run(["psql", "--version"], check=True, capture_output=True)
        print("✅ PostgreSQL detectado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  PostgreSQL não encontrado")
        print("   Instale o PostgreSQL e execute manualmente:")
        print("   psql -U postgres -c 'CREATE DATABASE spv_automatico;'")
        print("   psql -U postgres -d spv_automatico -f database/schema.sql")
        return False
    
    # Pergunta sobre configuração do banco
    db_host = input("Host do PostgreSQL (padrão: localhost): ").strip() or "localhost"
    db_port = input("Porta do PostgreSQL (padrão: 5432): ").strip() or "5432"
    db_name = input("Nome do banco (padrão: spv_automatico): ").strip() or "spv_automatico"
    db_user = input("Usuário do PostgreSQL (padrão: postgres): ").strip() or "postgres"
    db_password = input("Senha do PostgreSQL: ").strip()
    
    if not db_password:
        print("❌ Senha é obrigatória!")
        return False
    
    # Cria o arquivo .env
    env_content = f"""# Configuração do Banco de Dados PostgreSQL
        DATABASE_URL=postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}

        # Caminho para o Microsoft Edge WebDriver
        EDGE_DRIVER_PATH=

        # Configurações do Sistema
        MAX_EXECUTION_TIME=600
        INTERVALO_ESPERA=60
        MAX_TENTATIVAS=20

        # Configurações de Logging
        LOG_LEVEL=INFO
        LOG_FILE=spv_automatico.log

        # Configurações do Web Scraper
        WEBSITE_TYPE=TJSP
        HEADLESS=true
        TIMEOUT=30

        # Configurações de Performance
        BATCH_SIZE=100
        PAUSE_BETWEEN_REQUESTS=1
        """
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado")
    
    # Tenta criar o banco e executar o schema
    try:
        print("   Criando banco de dados...")
        subprocess.run([
            "psql", "-U", db_user, "-h", db_host, "-p", db_port,
            "-c", f"CREATE DATABASE {db_name};"
        ], check=True, input=db_password.encode())
        
        print("   Executando schema...")
        subprocess.run([
            "psql", "-U", db_user, "-h", db_host, "-p", db_port, "-d", db_name,
            "-f", "database/schema.sql"
        ], check=True, input=db_password.encode())
        
        print("✅ Banco de dados configurado com sucesso")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao configurar banco: {e}")
        print("   Execute manualmente:")
        print(f"   psql -U {db_user} -h {db_host} -p {db_port} -c 'CREATE DATABASE {db_name};'")
        print(f"   psql -U {db_user} -h {db_host} -p {db_port} -d {db_name} -f database/schema.sql")
        return False

def setup_webdriver():
    """Configura o WebDriver"""
    print("\n🌐 Configurando WebDriver...")
    
    # Verifica se o Edge está instalado
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(["msedge", "--version"], check=True, capture_output=True)
        else:  # Linux/Mac
            subprocess.run(["microsoft-edge", "--version"], check=True, capture_output=True)
        print("✅ Microsoft Edge detectado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Microsoft Edge não encontrado")
        print("   Instale o Microsoft Edge para usar o sistema")
        return False
    
    # Pergunta sobre o WebDriver
    driver_path = input("Caminho para o msedgedriver (deixe vazio para automático): ").strip()
    
    if driver_path:
        if not os.path.exists(driver_path):
            print("❌ Caminho do WebDriver não encontrado!")
            return False
        
        # Atualiza o .env
        with open(".env", "r") as f:
            env_content = f.read()
        
        env_content = env_content.replace("EDGE_DRIVER_PATH=", f"EDGE_DRIVER_PATH={driver_path}")
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("✅ WebDriver configurado")
    
    return True

def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios...")
    
    directories = ["logs", "data"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Diretório {directory} criado")
    
    return True

def run_tests():
    """Executa testes básicos"""
    print("\n🧪 Executando testes...")
    
    # Determina o comando python correto
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Linux/Mac
        python_cmd = "venv/bin/python"
    
    try:
        # Testa importação dos módulos
        subprocess.run([python_cmd, "-c", "import src.config.database"], check=True)
        subprocess.run([python_cmd, "-c", "import src.models.models"], check=True)
        subprocess.run([python_cmd, "-c", "import src.services.database_service"], check=True)
        
        print("✅ Testes básicos passaram")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro nos testes: {e}")
        return False

def print_final_instructions():
    """Imprime instruções finais"""
    print("\n" + "=" * 60)
    print("🎉 Setup concluído com sucesso!")
    print("=" * 60)
    
    print("\n📋 Próximos passos:")
    print("1. Ative o ambiente virtual:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Linux/Mac
        print("   source venv/bin/activate")
    
    print("\n2. Execute o sistema:")
    print("   python src/spv_automatico.py")
    
    print("\n3. Ou execute os exemplos:")
    print("   python examples/exemplo_uso.py")
    
    print("\n4. Para usar Docker:")
    print("   docker-compose up -d")
    
    print("\n📚 Consulte o README.md para mais informações")
    print("🆘 Para suporte, abra uma issue no GitHub")

def main():
    """Função principal do setup"""
    print_header()
    
    # Verifica Python
    if not check_python_version():
        sys.exit(1)
    
    # Cria ambiente virtual
    if not create_virtual_environment():
        sys.exit(1)
    
    # Instala dependências
    if not install_dependencies():
        sys.exit(1)
    
    # Configura banco de dados
    if not setup_database():
        print("⚠️  Configure o banco manualmente e continue...")
    
    # Configura WebDriver
    if not setup_webdriver():
        print("⚠️  Configure o WebDriver manualmente e continue...")
    
    # Cria diretórios
    create_directories()
    
    # Executa testes
    run_tests()
    
    # Instruções finais
    print_final_instructions()

if __name__ == "__main__":
    main() 