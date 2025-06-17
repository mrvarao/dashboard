#!/usr/bin/env python3
"""
Teste de execução do Dashboard
"""

import sys
import os

def test_basic_functionality():
    """Testa funcionalidades básicas"""
    print("🧪 Testando funcionalidades básicas...")
    
    # Teste 1: Verificar arquivos
    required_files = ['app.py', 'auth.py', 'database.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - AUSENTE")
            return False
    
    # Teste 2: Importar módulos principais
    try:
        sys.path.append(os.getcwd())
        from database import DatabaseManager
        print("✅ DatabaseManager importado")
        
        from auth import AuthManager
        print("✅ AuthManager importado")
        
        # Teste 3: Criar banco
        db = DatabaseManager()
        print("✅ Banco de dados criado")
        
        # Teste 4: Testar conexão
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"✅ Banco conectado - {count} usuários")
        
        # Teste 5: Testar autenticação
        auth = AuthManager()
        user = auth.authenticate_user("admin", "admin123")
        if user:
            print(f"✅ Autenticação OK - {user['name']}")
        else:
            print("❌ Falha na autenticação")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🌱 Dashboard Embrapa - Teste de Funcionalidade")
    print("=" * 50)
    
    if test_basic_functionality():
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema está funcionando corretamente")
        print("\n🚀 Para executar o dashboard:")
        print("   python quick_start.py")
        print("   ou")
        print("   streamlit run app.py")
        return True
    else:
        print("\n❌ ALGUNS TESTES FALHARAM")
        print("⚠️ Verifique os erros acima")
        return False

if __name__ == "__main__":
    success = main()
    print("=" * 50)