#!/usr/bin/env python3
"""
Teste de dependências do Dashboard Embrapa
"""

def test_imports():
    """Testa se todas as dependências podem ser importadas"""
    print("🔍 Testando importações...")
    
    try:
        import streamlit as st
        print("✅ Streamlit importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar Streamlit: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar Pandas: {e}")
        return False
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar Plotly: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ Numpy importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar Numpy: {e}")
        return False
    
    try:
        import sqlite3
        print("✅ SQLite3 importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar SQLite3: {e}")
        return False
    
    return True

def test_database():
    """Testa a conexão com o banco de dados"""
    print("\n🗄️ Testando banco de dados...")
    
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        conn = db.get_connection()
        
        # Teste simples de consulta
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"✅ Banco de dados conectado. Usuários cadastrados: {count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False

def test_modules():
    """Testa se todos os módulos podem ser importados"""
    print("\n📦 Testando módulos...")
    
    modules = [
        'auth',
        'database',
        'modules.projects',
        'modules.admin',
        'modules.kpis',
        'modules.publications',
        'modules.experimental_data',
        'modules.alerts',
        'modules.export'
    ]
    
    success = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} importado com sucesso")
        except ImportError as e:
            print(f"❌ Erro ao importar {module}: {e}")
            success = False
    
    return success

def main():
    """Função principal de teste"""
    print("🌱 Dashboard Embrapa - Teste de Dependências")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Teste de importações
    if not test_imports():
        all_tests_passed = False
    
    # Teste de banco de dados
    if not test_database():
        all_tests_passed = False
    
    # Teste de módulos
    if not test_modules():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 Todos os testes passaram! O sistema está pronto para uso.")
    else:
        print("⚠️ Alguns testes falharam. Verifique as dependências.")
    
    return all_tests_passed

if __name__ == "__main__":
    main()