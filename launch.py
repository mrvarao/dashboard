#!/usr/bin/env python3

import os
import sys

# Adicionar diretório atual ao path
sys.path.insert(0, os.getcwd())

print("🌱 Dashboard Embrapa - Executando...")

# Verificar se streamlit está disponível
try:
    import streamlit
    print("✅ Streamlit encontrado")
except ImportError:
    print("📦 Instalando Streamlit...")
    os.system(f"{sys.executable} -m pip install streamlit pandas plotly --quiet")

# Verificar banco de dados
try:
    from database import DatabaseManager
    db = DatabaseManager()
    db.populate_sample_data()
    print("✅ Banco de dados pronto")
except Exception as e:
    print(f"⚠️ Banco: {e}")

print("\n🚀 Iniciando Dashboard...")
print("📱 URL: http://localhost:8501")
print("🔑 Login: admin / admin123")

# Executar streamlit
os.system(f"{sys.executable} -m streamlit run app.py --server.port=8501")