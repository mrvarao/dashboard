
#!/usr/bin/env python3
"""
Script de instalação e inicialização do Dashboard Embrapa Meio-Norte
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário!")
        print(f"Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def install_requirements():
    """Instala as dependências do requirements.txt"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def initialize_database():
    """Inicializa o banco de dados"""
    print("🗄️ Inicializando banco de dados...")
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        db.populate_sample_data()
        print("✅ Banco de dados inicializado com dados de exemplo!")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        return False

def create_directories():
    """Cria diretórios necessários"""
    print("📁 Criando diretórios...")
    directories = ['uploads', 'exports', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Diretório '{directory}' criado/verificado")

def run_tests():
    """Executa testes básicos do sistema"""
    print("🧪 Executando testes básicos...")
    try:
        # Teste de importação dos módulos
        from auth import AuthManager
        from database import DatabaseManager
        from modules.projects import ProjectsManager
        from modules.admin import AdminManager
        from modules.kpis import KPIManager
        from modules.publications import PublicationsManager
        from modules.experimental_data import ExperimentalDataManager
        from modules.alerts import AlertsManager
        from modules.export import ExportManager
        
        print("✅ Todos os módulos importados com sucesso!")
        
        # Teste de conexão com banco
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        conn.close()
        
        print(f"✅ Banco de dados conectado - {user_count} usuários encontrados")
        return True
        
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        return False

def show_usage_info():
    """Mostra informações de uso"""
    print("\n" + "="*60)
    print("🌱 DASHBOARD EMBRAPA MEIO-NORTE - INSTALAÇÃO CONCLUÍDA!")
    print("="*60)
    print("\n📋 COMO USAR:")
    print("1. Execute o comando: streamlit run app.py")
    print("2. Acesse: http://localhost:8501")
    print("\n👤 USUÁRIOS DE TESTE:")
    print("• Administrador: admin / admin123")
    print("• Pesquisador: joao.silva / pesq123")
    print("• Gestor: maria.santos / gest123")
    print("\n📚 FUNCIONALIDADES:")
    print("• Gestão de Projetos PD&I")
    print("• Gestão Administrativa")
    print("• Indicadores de Desempenho (KPIs)")
    print("• Publicações e Relatórios")
    print("• Dados Experimentais")
    print("• Sistema de Alertas")
    print("• Exportação (CSV, Excel, PDF)")
    print("\n📖 Para mais informações, consulte o README.md")
    print("="*60)

def main():
    """Função principal de instalação"""
    print("🌱 INSTALADOR - Dashboard Embrapa Meio-Norte")
    print("="*50)
    
    # Verificar versão do Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependências
    if not install_requirements():
        print("❌ Falha na instalação. Tente executar manualmente:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Criar diretórios
    create_directories()
    
    # Inicializar banco de dados
    if not initialize_database():
        print("❌ Falha na inicialização do banco de dados")
        sys.exit(1)
    
    # Executar testes
    if not run_tests():
        print("⚠️ Alguns testes falharam, mas a instalação pode estar funcional")
    
    # Mostrar informações de uso
    show_usage_info()
    
    # Perguntar se deseja executar o sistema
    response = input("\n🚀 Deseja executar o sistema agora? (s/n): ").lower().strip()
    if response in ['s', 'sim', 'y', 'yes']:
        print("\n🚀 Iniciando o Dashboard...")
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        except KeyboardInterrupt:
            print("\n👋 Sistema encerrado pelo usuário")
        except Exception as e:
            print(f"\n❌ Erro ao executar: {e}")
            print("Execute manualmente: streamlit run app.py")

if __name__ == "__main__":
    main()
