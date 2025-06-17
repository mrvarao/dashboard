#!/usr/bin/env python3
"""
🌱 DASHBOARD EMBRAPA MEIO-NORTE
Script de Execução Automática

INSTRUÇÕES:
1. Execute este arquivo: python EXECUTAR_DASHBOARD.py
2. Aguarde o carregamento
3. Acesse http://localhost:8501
4. Use login: admin / admin123
"""

import sys
import os
import subprocess
import time

def print_banner():
    """Imprime banner do sistema"""
    print("=" * 60)
    print("🌱 DASHBOARD EMBRAPA MEIO-NORTE")
    print("   Sistema de Gestão de PD&I")
    print("   Pesquisa, Desenvolvimento e Inovação")
    print("=" * 60)

def check_environment():
    """Verifica ambiente de execução"""
    print("🔍 Verificando ambiente...")
    
    # Python version
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ necessário")
        return False
    
    # Arquivos essenciais
    files = ['app.py', 'auth.py', 'database.py']
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - AUSENTE")
            return False
    
    return True

def setup_system():
    """Configura o sistema"""
    print("\n🔧 Configurando sistema...")
    
    # Adicionar ao path
    sys.path.insert(0, os.getcwd())
    
    # Instalar dependências
    packages = ["streamlit", "pandas", "plotly", "openpyxl"]
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"📦 Instalando {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package, "--quiet"
            ])
    
    # Configurar banco de dados
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        db.populate_sample_data()
        print("✅ Banco de dados configurado")
    except Exception as e:
        print(f"⚠️ Aviso no banco: {e}")
    
    return True

def show_instructions():
    """Mostra instruções de uso"""
    print("\n" + "=" * 60)
    print("🎯 DASHBOARD INICIANDO...")
    print("📱 URL: http://localhost:8501")
    print("\n🔑 CREDENCIAIS DE TESTE:")
    print("   👤 Administrador:")
    print("      Usuário: admin")
    print("      Senha: admin123")
    print("   👤 Pesquisador:")
    print("      Usuário: joao.silva") 
    print("      Senha: pesq123")
    print("   👤 Gestor:")
    print("      Usuário: maria.santos")
    print("      Senha: gest123")
    print("\n📊 FUNCIONALIDADES:")
    print("   🏠 Dashboard - Visão geral")
    print("   📊 Projetos PD&I - Gestão de projetos")
    print("   👥 Administração - Funcionários")
    print("   📈 KPIs - Indicadores")
    print("   📚 Publicações - Artigos científicos")
    print("   🧪 Dados Experimentais - Análises")
    print("   🔔 Alertas - Notificações")
    print("   📤 Exportação - Relatórios")
    print("\n⏳ Aguarde o carregamento (pode demorar alguns segundos)")
    print("🛑 Para parar o sistema: Ctrl+C")
    print("=" * 60)

def run_dashboard():
    """Executa o dashboard"""
    try:
        # Comando Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
            "--logger.level=error"
        ]
        
        # Executar
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n👋 DASHBOARD ENCERRADO")
        print("✅ Obrigado por usar o Dashboard Embrapa!")
        
    except Exception as e:
        print(f"\n❌ Erro na execução: {e}")
        print("\n💡 EXECUÇÃO MANUAL:")
        print("   pip install streamlit pandas plotly")
        print("   streamlit run app.py")

def main():
    """Função principal"""
    print_banner()
    
    # Verificar ambiente
    if not check_environment():
        print("\n❌ AMBIENTE INADEQUADO")
        input("Pressione Enter para sair...")
        return
    
    # Configurar sistema
    if not setup_system():
        print("\n❌ FALHA NA CONFIGURAÇÃO")
        input("Pressione Enter para sair...")
        return
    
    print("\n✅ SISTEMA CONFIGURADO COM SUCESSO!")
    
    # Mostrar instruções
    show_instructions()
    
    # Pequena pausa
    time.sleep(2)
    
    # Executar dashboard
    run_dashboard()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Execução cancelada")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        input("Pressione Enter para sair...")