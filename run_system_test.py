#!/usr/bin/env python3

import subprocess
import sys
import os

# Executar teste
print("Executando teste do sistema...")
try:
    result = subprocess.run([sys.executable, 'test_run.py'], 
                          capture_output=True, text=True, timeout=30)
    print("RESULTADO DO TESTE:")
    print(result.stdout)
    if result.stderr:
        print("ERROS/AVISOS:")
        print(result.stderr)
    
    if result.returncode == 0:
        print("\n✅ SISTEMA TESTADO COM SUCESSO!")
        print("🚀 Iniciando dashboard...")
        
        # Executar dashboard
        subprocess.run([sys.executable, 'quick_start.py'])
    else:
        print("\n❌ Problemas encontrados no teste")
        
except Exception as e:
    print(f"Erro ao executar teste: {e}")
    
    # Tentar execução direta
    print("\n🔄 Tentando execução direta...")
    try:
        subprocess.run([sys.executable, 'quick_start.py'])
    except Exception as e2:
        print(f"Erro na execução direta: {e2}")