#!/usr/bin/env python3

import subprocess
import sys
import os

def run_direct_test():
    """Executa o teste direto"""
    print("🧪 Executando teste direto do sistema...")
    
    try:
        # Executar o teste
        result = subprocess.run(
            [sys.executable, 'direct_test.py'],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=os.getcwd()
        )
        
        print("📋 RESULTADO DO TESTE:")
        print("-" * 40)
        print(result.stdout)
        
        if result.stderr:
            print("\n⚠️ AVISOS/ERROS:")
            print("-" * 40)
            print(result.stderr)
        
        print(f"\n📊 Código de retorno: {result.returncode}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ Teste demorou muito para executar")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar teste: {e}")
        return False

def try_streamlit_execution():
    """Tenta executar o Streamlit"""
    print("\n🚀 Tentando executar Streamlit...")
    
    try:
        # Verificar se streamlit está instalado
        result = subprocess.run(
            [sys.executable, '-m', 'streamlit', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Streamlit está instalado")
            print(f"📦 Versão: {result.stdout.strip()}")
            
            print("\n🌱 INICIANDO DASHBOARD EMBRAPA...")
            print("📱 URL: http://localhost:8501")
            print("🔑 Login: admin / admin123")
            print("⏳ Aguarde carregar...")
            print("🛑 Ctrl+C para parar")
            print("=" * 50)
            
            # Executar streamlit
            subprocess.run([
                sys.executable, '-m', 'streamlit', 'run', 'app.py',
                '--server.port=8501',
                '--server.headless=true'
            ])
            
        else:
            print("❌ Streamlit não está instalado")
            print("📦 Instalando Streamlit...")
            
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                'streamlit', 'pandas', 'plotly', '--quiet'
            ])
            
            print("✅ Streamlit instalado, tentando executar...")
            subprocess.run([
                sys.executable, '-m', 'streamlit', 'run', 'app.py',
                '--server.port=8501'
            ])
            
    except KeyboardInterrupt:
        print("\n👋 Execução interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar Streamlit: {e}")

def main():
    """Função principal"""
    print("🌱 DASHBOARD EMBRAPA MEIO-NORTE")
    print("🔧 Sistema de Teste e Execução")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('app.py'):
        print("❌ app.py não encontrado!")
        print("📁 Certifique-se de estar no diretório correto do projeto")
        return
    
    # Executar teste
    test_success = run_direct_test()
    
    if test_success:
        print("\n🎉 TESTE PASSOU COM SUCESSO!")
        print("✅ Sistema está pronto para execução")
    else:
        print("\n⚠️ TESTE ENCONTROU PROBLEMAS")
        print("🔄 Tentando executar mesmo assim...")
    
    # Tentar executar Streamlit
    try_streamlit_execution()

if __name__ == "__main__":
    main()