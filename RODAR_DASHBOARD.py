#!/usr/bin/env python3
"""
🌱 DASHBOARD EMBRAPA - EXECUÇÃO DIRETA
Script simplificado baseado no EXECUTAR_DASHBOARD.py que funciona

COMO USAR:
python RODAR_DASHBOARD.py
"""

import sys
import os
import subprocess

def main():
    print("🌱 DASHBOARD EMBRAPA MEIO-NORTE")
    print("🚀 Iniciando execução direta...")
    print("=" * 45)
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ necessário")
        input("Pressione Enter para sair...")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Verificar app.py
    if not os.path.exists("app.py"):
        print("❌ app.py não encontrado!")
        print("💡 Execute no diretório do projeto")
        input("Pressione Enter para sair...")
        return
    
    print("✅ app.py encontrado")
    
    # Configurar path
    sys.path.insert(0, os.getcwd())
    
    # Instalar dependências básicas
    packages = ["streamlit", "pandas", "plotly", "openpyxl"]
    print("📦 Verificando dependências...")
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"📦 Instalando {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                package, "--quiet"
            ])
    
    # Configurar banco
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        db.populate_sample_data()
        print("✅ Banco configurado")
    except Exception as e:
        print(f"⚠️ Banco: {e} (continuando...)")
    
    # Informações de acesso
    print("\n" + "=" * 45)
    print("🎯 DASHBOARD EXECUTANDO...")
    print("📱 URL: http://localhost:8501")
    print("🔑 Login: admin / admin123")
    print("⏳ Aguarde o carregamento...")
    print("🛑 Para parar: Ctrl+C")
    print("=" * 45)
    
    # Executar Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
            "--logger.level=error"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard encerrado")
        print("✅ Obrigado por usar o sistema!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("💡 Tente manualmente:")
        print("   streamlit run app.py")

if __name__ == "__main__":
    main()