#!/usr/bin/env python3
"""
🌱 DASHBOARD EMBRAPA - INÍCIO RÁPIDO
Execute este arquivo para iniciar o sistema
"""

import os
import sys
import subprocess

# Banner
print("🌱 DASHBOARD EMBRAPA MEIO-NORTE")
print("🚀 Iniciando sistema...")
print("=" * 40)

# Verificar Python
if sys.version_info < (3, 8):
    print("❌ Python 3.8+ necessário")
    exit(1)

# Verificar arquivos
if not os.path.exists("app.py"):
    print("❌ app.py não encontrado")
    exit(1)

print("✅ Ambiente OK")

# Instalar Streamlit se necessário
try:
    import streamlit
except ImportError:
    print("📦 Instalando Streamlit...")
    subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "pandas", "plotly", "--quiet"])

# Configurar banco
try:
    sys.path.insert(0, os.getcwd())
    from database import DatabaseManager
    DatabaseManager().populate_sample_data()
    print("✅ Banco configurado")
except:
    print("⚠️ Problema no banco")

# Executar
print("\n🎯 DASHBOARD EXECUTANDO...")
print("📱 http://localhost:8501")
print("🔑 admin / admin123")
print("=" * 40)

os.system(f"{sys.executable} -m streamlit run app.py --server.port=8501")