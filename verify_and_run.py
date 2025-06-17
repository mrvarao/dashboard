#!/usr/bin/env python3

import sys
import os

# Adicionar diretório atual ao path
sys.path.insert(0, os.getcwd())

def verify_system():
    """Verifica se o sistema está funcionando"""
    print("🔍 Verificando sistema...")
    
    # Verificar arquivos
    required_files = ['app.py', 'auth.py', 'database.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - AUSENTE")
            return False
    
    # Testar imports
    try:
        from database import DatabaseManager
        print("✅ DatabaseManager")
        
        from auth import AuthManager  
        print("✅ AuthManager")
        
        # Testar banco
        db = DatabaseManager()
        conn = db.get_connection()
        
        # Verificar se há usuários
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            if count == 0:
                print("📝 Populando dados...")
                db.populate_sample_data()
                cursor.execute("SELECT COUNT(*) FROM users")
                count = cursor.fetchone()[0]
            print(f"✅ Banco OK - {count} usuários")
        except:
            print("📝 Criando dados...")
            db.populate_sample_data()
            print("✅ Dados criados")
        
        conn.close()
        
        # Testar autenticação
        auth = AuthManager()
        user = auth.authenticate_user("admin", "admin123")
        if user:
            print(f"✅ Auth OK - {user['name']}")
        else:
            print("❌ Falha na autenticação")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def install_streamlit():
    """Instala Streamlit se necessário"""
    try:
        import streamlit
        print("✅ Streamlit disponível")
        return True
    except ImportError:
        print("📦 Instalando Streamlit...")
        import subprocess
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "streamlit", "pandas", "plotly", "--quiet"
            ])
            print("✅ Streamlit instalado")
            return True
        except:
            print("❌ Erro ao instalar Streamlit")
            return False

def run_dashboard():
    """Executa o dashboard"""
    print("\n🚀 INICIANDO DASHBOARD EMBRAPA...")
    print("📱 URL: http://localhost:8501")
    print("🔑 Credenciais de teste:")
    print("   👤 admin / admin123 (Administrador)")
    print("   👤 joao.silva / pesq123 (Pesquisador)")
    print("   👤 maria.santos / gest123 (Gestor)")
    print("\n⏳ Aguarde o carregamento...")
    print("🛑 Para parar: Ctrl+C")
    print("=" * 50)
    
    import subprocess
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.headless=true"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")

def main():
    """Função principal"""
    print("🌱 DASHBOARD EMBRAPA MEIO-NORTE")
    print("🔧 Verificação e Execução")
    print("=" * 50)
    
    # Verificar sistema
    if not verify_system():
        print("\n❌ SISTEMA COM PROBLEMAS")
        print("⚠️ Verifique os erros acima")
        return
    
    print("\n✅ SISTEMA VERIFICADO COM SUCESSO!")
    
    # Instalar Streamlit
    if not install_streamlit():
        print("\n❌ FALHA NA INSTALAÇÃO DO STREAMLIT")
        return
    
    # Executar dashboard
    run_dashboard()

if __name__ == "__main__":
    main()