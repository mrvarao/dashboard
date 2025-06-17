#!/usr/bin/env python3
"""
Inicialização direta do Dashboard Embrapa
"""

import subprocess
import sys
import os
import time

def main():
    print("🌱 DASHBOARD EMBRAPA MEIO-NORTE")
    print("🚀 Iniciando sistema...")
    print("=" * 40)
    
    # Verificações básicas
    if not os.path.exists("app.py"):
        print("❌ app.py não encontrado!")
        return
    
    print("✅ Arquivos encontrados")
    
    # Instalar dependências se necessário
    packages = ["streamlit", "pandas", "plotly"]
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} disponível")
        except ImportError:
            print(f"📦 Instalando {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
    
    # Inicializar banco
    print("🗄️ Inicializando banco...")
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        db.populate_sample_data()
        print("✅ Banco pronto")
    except Exception as e:
        print(f"⚠️ Aviso no banco: {e}")
    
    print("\n🎯 DASHBOARD INICIANDO...")
    print("📱 Acesse: http://localhost:8501")
    print("🔑 Login: admin / admin123")
    print("⏳ Carregando...")
    print("🛑 Ctrl+C para parar")
    print("=" * 40)
    
    # Executar Streamlit
    try:
        os.system(f"{sys.executable} -m streamlit run app.py --server.port=8501")
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()