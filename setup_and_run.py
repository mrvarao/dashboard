#!/usr/bin/env python3
"""
Script de configuração e execução do Dashboard Embrapa
"""

import subprocess
import sys
import os
import time

def install_requirements():
    """Instala as dependências necessárias"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def test_installation():
    """Testa se a instalação foi bem-sucedida"""
    print("\n🔍 Testando instalação...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'numpy',
        'openpyxl',
        'reportlab',
        'matplotlib',
        'seaborn',
        'scipy'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} OK")
        except ImportError:
            print(f"❌ {package} não encontrado")
            return False
    
    return True

def initialize_database():
    """Inicializa o banco de dados"""
    print("\n🗄️ Inicializando banco de dados...")
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        db.populate_sample_data()
        print("✅ Banco de dados inicializado!")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        return False

def run_streamlit():
    """Executa a aplicação Streamlit"""
    print("\n🚀 Iniciando aplicação...")
    print("📱 A aplicação será aberta em: http://localhost:8501")
    print("🔑 Use as credenciais de teste:")
    print("   - Admin: admin / admin123")
    print("   - Pesquisador: joao.silva / pesq123")
    print("   - Gestor: maria.santos / gest123")
    print("\n⏳ Aguarde alguns segundos para a aplicação carregar...")
    
    try:
        # Executar streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501"])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")

def main():
    """Função principal"""
    print("🌱 Dashboard Embrapa Meio-Norte - Setup e Execução")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Arquivo app.py não encontrado!")
        print("   Certifique-se de estar no diretório correto do projeto")
        return
    
    # Instalar dependências
    if not install_requirements():
        print("❌ Falha na instalação das dependências")
        return
    
    # Testar instalação
    if not test_installation():
        print("❌ Falha nos testes de instalação")
        return
    
    # Inicializar banco de dados
    if not initialize_database():
        print("❌ Falha na inicialização do banco de dados")
        return
    
    print("\n✅ Setup concluído com sucesso!")
    print("=" * 60)
    
    # Executar aplicação
    run_streamlit()

if __name__ == "__main__":
    main()