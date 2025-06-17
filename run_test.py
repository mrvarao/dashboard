#!/usr/bin/env python3
import subprocess
import sys
import os

def run_test():
    """Executa o teste de dependências"""
    try:
        # Executar o teste
        result = subprocess.run([sys.executable, 'test_dependencies.py'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Return code: {result.returncode}")
        
    except Exception as e:
        print(f"Erro ao executar teste: {e}")

if __name__ == "__main__":
    run_test()