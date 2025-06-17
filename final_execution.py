#!/usr/bin/env python3

import sys
import os
import subprocess

# Configurar path
current_dir = os.getcwd()
sys.path.insert(0, current_dir)

print("🌱 DASHBOARD EMBRAPA MEIO-NORTE")
print("🚀 Execução Final")
print("=" * 50)

# Verificação rápida
print("📁 Diretório:", current_dir)
print("🐍 Python:", sys.version.split()[0])

# Verificar arquivos essenciais
essential_files = ['app.py', 'auth.py', 'database.py']
missing_files = []

for file in essential_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file}")
        missing_files.append(file)

if missing_files:
    print(f"\n❌ ARQUIVOS AUSENTES: {missing_files}")
    print("⚠️ Certifique-se de estar no diretório correto")
    exit(1)

# Testar imports básicos
print("\n🧪 Testando imports...")
try:
    from database import DatabaseManager
    print("✅ DatabaseManager importado")
    
    # Inicializar banco
    db = DatabaseManager()
    db.populate_sample_data()
    print("✅ Banco inicializado")
    
    from auth import AuthManager
    print("✅ AuthManager importado")
    
    # Testar login
    auth = AuthManager()
    user = auth.authenticate_user("admin", "admin123")
    if user:
        print(f"✅ Login funcionando - {user['name']}")
    else:
        print("❌ Problema no login")
    
except Exception as e:
    print(f"❌ Erro nos imports: {e}")
    print("⚠️ Continuando mesmo assim...")

# Verificar/instalar Streamlit
print("\n📦 Verificando Streamlit...")
try:
    import streamlit
    print("✅ Streamlit disponível")
except ImportError:
    print("📦 Instalando Streamlit...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "streamlit", "pandas", "plotly", "--quiet"
        ])
        print("✅ Streamlit instalado")
    except Exception as e:
        print(f"❌ Erro ao instalar: {e}")
        exit(1)

# Executar dashboard
print("\n" + "=" * 50)
print("🎯 EXECUTANDO DASHBOARD EMBRAPA")
print("📱 Acesse: http://localhost:8501")
print("🔑 Login: admin / admin123")
print("⏳ Carregando sistema...")
print("🛑 Ctrl+C para parar")
print("=" * 50)

try:
    # Comando para executar Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port=8501",
        "--server.headless=true",
        "--browser.gatherUsageStats=false"
    ]
    
    # Executar
    subprocess.run(cmd, cwd=current_dir)
    
except KeyboardInterrupt:
    print("\n\n👋 Dashboard encerrado pelo usuário")
    print("✅ Obrigado por usar o Dashboard Embrapa!")
    
except FileNotFoundError:
    print("\n❌ Streamlit não encontrado após instalação")
    print("💡 Tente executar manualmente:")
    print("   pip install streamlit")
    print("   streamlit run app.py")
    
except Exception as e:
    print(f"\n❌ Erro inesperado: {e}")
    print("💡 Tente executar manualmente:")
    print("   streamlit run app.py")