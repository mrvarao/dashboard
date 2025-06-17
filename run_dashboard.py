#!/usr/bin/env python3
"""
Script principal para executar o Dashboard Embrapa
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Timer

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detectado")
        print("⚠️ É necessário Python 3.8 ou superior")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} OK")
    return True

def install_streamlit():
    """Instala apenas o Streamlit se não estiver disponível"""
    try:
        import streamlit
        print("✅ Streamlit já instalado")
        return True
    except ImportError:
        print("📦 Instalando Streamlit...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
            print("✅ Streamlit instalado com sucesso!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erro ao instalar Streamlit")
            return False

def install_basic_requirements():
    """Instala apenas as dependências básicas necessárias"""
    basic_packages = [
        "streamlit>=1.28.0",
        "pandas>=2.0.0", 
        "plotly>=5.15.0"
    ]
    
    print("📦 Instalando dependências básicas...")
    for package in basic_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package.split('>=')[0]} instalado")
        except subprocess.CalledProcessError:
            print(f"❌ Erro ao instalar {package}")
            return False
    
    return True

def setup_database():
    """Configura o banco de dados"""
    print("🗄️ Configurando banco de dados...")
    try:
        # Importar e inicializar banco
        sys.path.append(os.getcwd())
        from database import DatabaseManager
        
        db = DatabaseManager()
        db.populate_sample_data()
        print("✅ Banco de dados configurado!")
        return True
    except Exception as e:
        print(f"❌ Erro ao configurar banco: {e}")
        return False

def open_browser_delayed():
    """Abre o navegador após alguns segundos"""
    time.sleep(3)
    try:
        webbrowser.open('http://localhost:8501')
    except:
        pass

def run_streamlit_app():
    """Executa a aplicação Streamlit"""
    print("\n🚀 Iniciando Dashboard Embrapa...")
    print("📱 URL: http://localhost:8501")
    print("\n🔑 Credenciais de teste:")
    print("   👤 Admin: admin / admin123")
    print("   👤 Pesquisador: joao.silva / pesq123") 
    print("   👤 Gestor: maria.santos / gest123")
    print("\n⏳ Aguarde o carregamento...")
    print("🌐 O navegador será aberto automaticamente")
    print("\n⚠️ Para parar: Ctrl+C")
    print("=" * 50)
    
    # Abrir navegador após delay
    Timer(3.0, open_browser_delayed).start()
    
    try:
        # Executar streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard encerrado pelo usuário")
        print("✅ Obrigado por usar o Dashboard Embrapa!")
    except FileNotFoundError:
        print("❌ Streamlit não encontrado")
        print("💡 Tente: pip install streamlit")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")

def main():
    """Função principal"""
    print("🌱 Dashboard Embrapa Meio-Norte")
    print("=" * 40)
    
    # Verificar Python
    if not check_python_version():
        input("Pressione Enter para sair...")
        return
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Arquivo app.py não encontrado!")
        print("📁 Certifique-se de estar no diretório do projeto")
        input("Pressione Enter para sair...")
        return
    
    # Instalar Streamlit
    if not install_streamlit():
        print("❌ Falha na instalação do Streamlit")
        input("Pressione Enter para sair...")
        return
    
    # Instalar dependências básicas
    if not install_basic_requirements():
        print("❌ Falha na instalação das dependências")
        input("Pressione Enter para sair...")
        return
    
    # Configurar banco de dados
    if not setup_database():
        print("❌ Falha na configuração do banco")
        input("Pressione Enter para sair...")
        return
    
    print("\n✅ Configuração concluída!")
    print("=" * 40)
    
    # Executar aplicação
    run_streamlit_app()

if __name__ == "__main__":
    main()