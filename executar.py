#!/usr/bin/env python3
"""
🌱 Dashboard Embrapa Meio-Norte - Executar Sistema
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Timer

def print_header():
    """Imprime cabeçalho do sistema"""
    print("=" * 60)
    print("🌱 DASHBOARD EMBRAPA MEIO-NORTE")
    print("   Sistema de Gestão de PD&I")
    print("=" * 60)

def check_python():
    """Verifica versão do Python"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro} detectado")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ É necessário Python 3.8 ou superior")
        return False
    
    print("✅ Versão do Python OK")
    return True

def install_dependencies():
    """Instala dependências básicas"""
    print("\n📦 Instalando dependências...")

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"
        ])
        print("✅ Dependências instaladas")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False
    except FileNotFoundError:
        print("❌ Arquivo requirements.txt não encontrado")
        return False

    return True

def setup_database():
    """Configura banco de dados"""
    print("\n🗄️ Configurando banco de dados...")
    
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        db.populate_sample_data()
        print("✅ Banco de dados configurado")
        return True
    except Exception as e:
        print(f"❌ Erro no banco: {e}")
        return False

def open_browser():
    """Abre navegador após delay"""
    time.sleep(4)
    try:
        webbrowser.open('http://localhost:8501')
        print("🌐 Navegador aberto automaticamente")
    except:
        print("⚠️ Não foi possível abrir o navegador automaticamente")
        print("   Acesse manualmente: http://localhost:8501")

def run_app():
    """Executa a aplicação"""
    print("\n🚀 Iniciando Dashboard...")
    print("📱 URL: http://localhost:8501")
    print("\n🔑 CREDENCIAIS DE TESTE:")
    print("   👤 Administrador: admin / admin123")
    print("   👤 Pesquisador: joao.silva / pesq123")
    print("   👤 Gestor: maria.santos / gest123")
    print("\n⏳ Aguarde o carregamento (pode demorar alguns segundos)...")
    print("🛑 Para parar o sistema: Ctrl+C")
    print("=" * 60)
    
    # Abrir navegador em background
    Timer(4.0, open_browser).start()
    
    try:
        # Executar streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
            "--logger.level=error"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário")
        print("✅ Obrigado por usar o Dashboard Embrapa!")
    except FileNotFoundError:
        print("\n❌ Streamlit não encontrado")
        print("💡 Tente executar: pip install streamlit")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

def main():
    """Função principal"""
    print_header()

    # Verificar Python
    if not check_python():
        input("\nPressione Enter para sair...")
        return

    # Criar diretórios
    for dir in ["modules", "exports", "logs", "uploads"]:
        os.makedirs(dir, exist_ok=True)
    print("✅ Diretórios criados")

    # Verificar arquivos
    required_files = [
        "app.py", "auth.py", "database.py",
        "modules/admin.py", "modules/alerts.py",
        "modules/experimental_data.py", "modules/export.py",
        "modules/kpis.py", "modules/projects.py",
        "modules/publications.py"
    ]

    missing = [f for f in required_files if not os.path.exists(f)]
    if missing:
        print("\n❌ Arquivos não encontrados:")
        for f in missing:
            print(f"   - {f}")
        input("\nPressione Enter para sair...")
        return

    print("✅ Arquivos do projeto encontrados")

    # Instalar dependências
    if not install_dependencies():
        input("\nPressione Enter para sair...")
        return
    
    # Configurar banco
    if not setup_database():
        print("\n⚠️ Problema no banco de dados, mas continuando...")
    
    print("\n✅ SISTEMA PRONTO!")
    
    # Executar aplicação
    run_app()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Execução cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        input("\nPressione Enter para sair...")