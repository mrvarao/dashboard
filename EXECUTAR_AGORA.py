#!/usr/bin/env python3
"""
🌱 DASHBOARD EMBRAPA MEIO-NORTE - EXECUÇÃO OTIMIZADA
Script baseado no EXECUTAR_DASHBOARD.py que funciona corretamente

INSTRUÇÕES RÁPIDAS:
1. Execute: python EXECUTAR_AGORA.py
2. Aguarde o carregamento
3. Acesse: http://localhost:8501
4. Login: admin / admin123
"""

import sys
import os
import subprocess
import time

def print_header():
    """Cabeçalho do sistema"""
    print("=" * 65)
    print("🌱 DASHBOARD EMBRAPA MEIO-NORTE - EXECUÇÃO OTIMIZADA")
    print("   Sistema de Gestão de Pesquisa, Desenvolvimento e Inovação")
    print("=" * 65)

def verify_environment():
    """Verificação rápida e robusta do ambiente"""
    print("🔍 Verificando ambiente de execução...")
    
    # Versão do Python
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERRO: Python 3.8+ é necessário")
        print("💡 Atualize seu Python para continuar")
        return False
    
    # Verificar arquivos críticos
    critical_files = ['app.py', 'auth.py', 'database.py']
    missing_files = []
    
    for file in critical_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - AUSENTE")
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ ERRO: Arquivos ausentes: {', '.join(missing_files)}")
        print("💡 Certifique-se de estar no diretório correto do projeto")
        return False
    
    return True

def setup_dependencies():
    """Instalação automática de dependências"""
    print("\n🔧 Configurando dependências...")
    
    # Adicionar diretório atual ao path
    sys.path.insert(0, os.getcwd())
    
    # Lista de pacotes essenciais
    essential_packages = [
        "streamlit>=1.28.0",
        "pandas>=2.0.0", 
        "plotly>=5.15.0",
        "openpyxl>=3.1.0"
    ]
    
    # Instalar cada pacote
    for package in essential_packages:
        package_name = package.split('>=')[0]
        try:
            __import__(package_name)
            print(f"✅ {package_name} - já instalado")
        except ImportError:
            print(f"📦 Instalando {package_name}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    package, "--quiet", "--disable-pip-version-check"
                ])
                print(f"✅ {package_name} - instalado com sucesso")
            except subprocess.CalledProcessError:
                print(f"⚠️ {package_name} - problema na instalação (continuando...)")
    
    return True

def configure_database():
    """Configuração do banco de dados com tratamento robusto de erros"""
    print("\n🗄️ Configurando banco de dados...")
    
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        db.populate_sample_data()
        print("✅ Banco de dados configurado com sucesso")
        return True
    except Exception as e:
        print(f"⚠️ Aviso na configuração do banco: {e}")
        print("💡 O sistema pode funcionar mesmo assim")
        return True  # Não falhar por causa do banco

def show_access_info():
    """Informações de acesso ao sistema"""
    print("\n" + "=" * 65)
    print("🎯 DASHBOARD PRONTO PARA USO!")
    print("📱 URL de Acesso: http://localhost:8501")
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
    print("\n📊 MÓDULOS DISPONÍVEIS:")
    print("   🏠 Dashboard Principal - Visão geral do sistema")
    print("   📊 Projetos PD&I - Gestão de projetos de pesquisa")
    print("   👥 Administração - Gestão de funcionários")
    print("   📈 KPIs - Indicadores de performance")
    print("   📚 Publicações - Artigos e publicações científicas")
    print("   🧪 Dados Experimentais - Análises laboratoriais")
    print("   🔔 Alertas - Sistema de notificações")
    print("   📤 Exportação - Geração de relatórios")
    print("\n⏳ Aguarde alguns segundos para o carregamento completo")
    print("🛑 Para encerrar o sistema: pressione Ctrl+C")
    print("=" * 65)

def execute_dashboard():
    """Execução do dashboard com configurações otimizadas"""
    try:
        # Comando otimizado do Streamlit
        streamlit_cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
            "--logger.level=error",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false"
        ]
        
        print("\n🚀 Iniciando servidor Streamlit...")
        subprocess.run(streamlit_cmd)
        
    except KeyboardInterrupt:
        print("\n\n" + "=" * 50)
        print("👋 DASHBOARD ENCERRADO PELO USUÁRIO")
        print("✅ Obrigado por usar o Dashboard Embrapa Meio-Norte!")
        print("=" * 50)
        
    except FileNotFoundError:
        print("\n❌ ERRO: Streamlit não encontrado")
        print("💡 Solução manual:")
        print("   pip install streamlit")
        print("   streamlit run app.py")
        
    except Exception as e:
        print(f"\n❌ ERRO na execução: {e}")
        print("\n💡 EXECUÇÃO MANUAL ALTERNATIVA:")
        print("   1. pip install streamlit pandas plotly openpyxl")
        print("   2. streamlit run app.py --server.port=8501")

def main():
    """Função principal otimizada"""
    # Cabeçalho
    print_header()
    
    # Verificar ambiente
    if not verify_environment():
        print("\n❌ AMBIENTE INADEQUADO PARA EXECUÇÃO")
        print("💡 Corrija os problemas acima e tente novamente")
        input("\nPressione Enter para sair...")
        return
    
    # Configurar dependências
    if not setup_dependencies():
        print("\n❌ FALHA NA CONFIGURAÇÃO DE DEPENDÊNCIAS")
        input("\nPressione Enter para sair...")
        return
    
    # Configurar banco de dados
    configure_database()
    
    print("\n✅ SISTEMA CONFIGURADO E PRONTO!")
    
    # Mostrar informações de acesso
    show_access_info()
    
    # Pausa antes de iniciar
    time.sleep(3)
    
    # Executar dashboard
    execute_dashboard()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Execução cancelada pelo usuário")
        print("✅ Até logo!")
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        print("💡 Tente executar manualmente:")
        print("   python app.py")
        input("\nPressione Enter para sair...")