#!/usr/bin/env python3

import os
import sys
import subprocess

print("🌱 Dashboard Embrapa - Execução Simples")
print("=" * 40)

# Verificar Python
print(f"🐍 Python: {sys.version}")

# Verificar arquivos
if os.path.exists('app.py'):
    print("✅ app.py encontrado")
else:
    print("❌ app.py não encontrado")
    exit(1)

# Tentar importar e configurar banco
try:
    sys.path.insert(0, os.getcwd())
    from database import DatabaseManager
    db = DatabaseManager()
    db.populate_sample_data()
    print("✅ Banco configurado")
except Exception as e:
    print(f"⚠️ Banco: {e}")

# Instalar streamlit se necessário
try:
    import streamlit
    print("✅ Streamlit disponível")
except ImportError:
    print("📦 Instalando Streamlit...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "pandas", "plotly", "--quiet"])
    print("✅ Streamlit instalado")

print("\n🚀 EXECUTANDO DASHBOARD...")
print("📱 Acesse: http://localhost:8501")
print("🔑 Login: admin / admin123")
print("=" * 40)

# Executar
try:
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501"])
except KeyboardInterrupt:
    print("\n👋 Encerrado")
except Exception as e:
    print(f"❌ Erro: {e}")