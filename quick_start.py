#!/usr/bin/env python3
"""
Início rápido do Dashboard Embrapa
"""

import os
import sys
import subprocess

def main():
    print("🌱 Dashboard Embrapa - Início Rápido")
    print("=" * 40)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Arquivo app.py não encontrado!")
        print("Certifique-se de estar no diretório correto")
        return False
    
    print("✅ Arquivos encontrados")
    
    # Verificar Python
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ necessário")
        return False
    
    print("✅ Versão Python OK")
    
    # Tentar importar módulos básicos
    try:
        import sqlite3
        print("✅ SQLite disponível")
    except ImportError:
        print("❌ SQLite não disponível")
        return False
    
    # Verificar/instalar Streamlit
    try:
        import streamlit
        print("✅ Streamlit disponível")
    except ImportError:
        print("📦 Instalando Streamlit...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "--quiet"])
            print("✅ Streamlit instalado")
        except:
            print("❌ Erro ao instalar Streamlit")
            return False
    
    # Verificar/instalar Pandas
    try:
        import pandas
        print("✅ Pandas disponível")
    except ImportError:
        print("📦 Instalando Pandas...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "--quiet"])
            print("✅ Pandas instalado")
        except:
            print("❌ Erro ao instalar Pandas")
            return False
    
    # Verificar/instalar Plotly
    try:
        import plotly
        print("✅ Plotly disponível")
    except ImportError:
        print("📦 Instalando Plotly...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly", "--quiet"])
            print("✅ Plotly instalado")
        except:
            print("❌ Erro ao instalar Plotly")
            return False
    
    # Inicializar banco de dados
    print("🗄️ Inicializando banco...")
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        db.populate_sample_data()
        print("✅ Banco inicializado")
    except Exception as e:
        print(f"⚠️ Problema no banco: {e}")
    
    print("\n🚀 INICIANDO DASHBOARD...")
    print("📱 URL: http://localhost:8501")
    print("🔑 Login: admin / admin123")
    print("⏳ Aguarde carregar...")
    print("🛑 Para parar: Ctrl+C")
    print("=" * 40)
    
    # Executar Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard encerrado")
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        input("\nPressione Enter para sair...")