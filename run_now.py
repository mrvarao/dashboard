#!/usr/bin/env python3

import subprocess
import sys
import os

# Configurar ambiente
os.environ['PYTHONPATH'] = os.getcwd()

print("🌱 DASHBOARD EMBRAPA MEIO-NORTE")
print("🚀 Executando agora...")
print("=" * 40)

# Executar comando direto
cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501"]

print("📱 URL: http://localhost:8501")
print("🔑 Login: admin / admin123")
print("⏳ Iniciando...")
print("🛑 Ctrl+C para parar")
print("=" * 40)

try:
    subprocess.run(cmd, cwd=os.getcwd())
except KeyboardInterrupt:
    print("\n👋 Dashboard encerrado")
except FileNotFoundError:
    print("❌ Streamlit não encontrado")
    print("📦 Instalando...")
    subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "pandas", "plotly"])
    print("✅ Instalado, executando...")
    subprocess.run(cmd, cwd=os.getcwd())
except Exception as e:
    print(f"❌ Erro: {e}")