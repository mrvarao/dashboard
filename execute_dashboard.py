#!/usr/bin/env python3
"""
Execução do Dashboard Embrapa com verificações
"""

import subprocess
import sys
import os
import time

def execute_system_check():
    """Executa verificação do sistema"""
    print("🔍 Verificando sistema...")
    try:
        result = subprocess.run([sys.executable, 'check_system.py'], 
                              capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print("Avisos:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Erro na verificação: {e}")
        return False

def install_basic_deps():
    """Instala dependências básicas"""
    print("📦 Instalando dependências básicas...")
    basic_packages = ["streamlit", "pandas", "plotly", "openpyxl"]
    
    for package in basic_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            print(f"✅ {package} instalado")
        except:
            print(f"⚠️ Problema ao instalar {package}")

def setup_database():
    """Configura banco de dados"""
    print("🗄️ Configurando banco de dados...")
    try:
        subprocess.run([sys.executable, "database.py"], timeout=10)
        print("✅ Banco configurado")
        return True
    except Exception as e:
        print(f"⚠️ Problema no banco: {e}")
        return False

def start_streamlit():
    """Inicia o Streamlit"""
    print("🚀 Iniciando Dashboard Embrapa...")
    print("📱 Será executado em: http://localhost:8501")
    print("🔑 Credenciais de teste:")
    print("   admin / admin123")
    print("   joao.silva / pesq123")
    print("   maria.santos / gest123")
    print("\n⏳ Iniciando servidor...")
    
    try:
        # Executar streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.headless=true"
        ])
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado")
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    print("🌱 DASHBOARD EMBRAPA MEIO-NORTE")
    print("=" * 40)
    
    # Verificar arquivos
    if not os.path.exists("app.py"):
        print("❌ app.py não encontrado!")
        return
    
    # Instalar dependências
    install_basic_deps()
    
    # Verificar sistema
    if execute_system_check():
        print("✅ Sistema verificado com sucesso!")
    else:
        print("⚠️ Alguns problemas encontrados, mas continuando...")
    
    # Configurar banco
    setup_database()
    
    print("\n✅ PRONTO PARA EXECUTAR!")
    print("=" * 40)
    
    # Iniciar aplicação
    start_streamlit()

if __name__ == "__main__":
    main()