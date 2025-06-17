#!/usr/bin/env python3
"""
Verificação rápida do sistema Dashboard Embrapa
"""

import sys
import os

def check_files():
    """Verifica se todos os arquivos necessários existem"""
    print("📁 Verificando arquivos...")
    
    required_files = [
        'app.py',
        'auth.py', 
        'database.py',
        'requirements.txt',
        'modules/projects.py',
        'modules/admin.py',
        'modules/kpis.py',
        'modules/publications.py',
        'modules/experimental_data.py',
        'modules/alerts.py',
        'modules/export.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - AUSENTE")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_basic_imports():
    """Verifica imports básicos"""
    print("\n📦 Verificando imports básicos...")
    
    try:
        import sqlite3
        print("✅ sqlite3")
    except ImportError:
        print("❌ sqlite3")
        return False
    
    try:
        import hashlib
        print("✅ hashlib")
    except ImportError:
        print("❌ hashlib")
        return False
    
    try:
        from datetime import datetime
        print("✅ datetime")
    except ImportError:
        print("❌ datetime")
        return False
    
    return True

def check_database_creation():
    """Verifica se o banco pode ser criado"""
    print("\n🗄️ Verificando criação do banco...")
    
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        print("✅ DatabaseManager criado")
        
        conn = db.get_connection()
        print("✅ Conexão estabelecida")
        
        conn.close()
        print("✅ Conexão fechada")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def check_auth_system():
    """Verifica sistema de autenticação"""
    print("\n🔐 Verificando sistema de autenticação...")
    
    try:
        from auth import AuthManager
        auth = AuthManager()
        print("✅ AuthManager criado")
        
        # Teste de hash
        test_hash = auth.hash_password("test123")
        print("✅ Hash de senha funcionando")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Função principal"""
    print("🌱 Dashboard Embrapa - Verificação do Sistema")
    print("=" * 50)
    
    all_ok = True
    
    # Verificar arquivos
    if not check_files():
        all_ok = False
    
    # Verificar imports básicos
    if not check_basic_imports():
        all_ok = False
    
    # Verificar banco de dados
    if not check_database_creation():
        all_ok = False
    
    # Verificar autenticação
    if not check_auth_system():
        all_ok = False
    
    print("\n" + "=" * 50)
    if all_ok:
        print("🎉 Sistema verificado com sucesso!")
        print("✅ Todos os componentes estão funcionando")
        print("\n🚀 Para executar o sistema:")
        print("   python setup_and_run.py")
        print("   ou")
        print("   streamlit run app.py")
    else:
        print("⚠️ Problemas encontrados no sistema")
        print("❌ Verifique os erros acima")
    
    return all_ok

if __name__ == "__main__":
    main()