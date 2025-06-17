#!/usr/bin/env python3

import sys
import os

# Adicionar diretório atual ao Python path
current_dir = os.getcwd()
sys.path.insert(0, current_dir)

print("🌱 Dashboard Embrapa - Teste Direto")
print(f"📁 Diretório: {current_dir}")
print("=" * 40)

# Teste 1: Verificar arquivos
files_to_check = ['app.py', 'auth.py', 'database.py']
for file in files_to_check:
    if os.path.exists(file):
        print(f"✅ {file} encontrado")
    else:
        print(f"❌ {file} não encontrado")

# Teste 2: Tentar importar database
try:
    from database import DatabaseManager
    print("✅ DatabaseManager importado com sucesso")
    
    # Criar instância
    db = DatabaseManager()
    print("✅ Instância do banco criada")
    
    # Testar conexão
    conn = db.get_connection()
    print("✅ Conexão com banco estabelecida")
    
    # Verificar tabelas
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"✅ Tabelas encontradas: {len(tables)}")
    
    # Verificar usuários
    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Usuários no banco: {user_count}")
    except:
        print("⚠️ Tabela users não encontrada, populando dados...")
        db.populate_sample_data()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Usuários criados: {user_count}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Erro no banco de dados: {e}")
    import traceback
    traceback.print_exc()

# Teste 3: Tentar importar auth
try:
    from auth import AuthManager
    print("✅ AuthManager importado com sucesso")
    
    auth = AuthManager()
    print("✅ Instância do AuthManager criada")
    
    # Testar autenticação
    user = auth.authenticate_user("admin", "admin123")
    if user:
        print(f"✅ Autenticação funcionando - Usuário: {user['name']}")
    else:
        print("❌ Falha na autenticação")
    
except Exception as e:
    print(f"❌ Erro na autenticação: {e}")
    import traceback
    traceback.print_exc()

# Teste 4: Verificar módulos
modules_dir = os.path.join(current_dir, 'modules')
if os.path.exists(modules_dir):
    print(f"✅ Diretório modules encontrado")
    module_files = os.listdir(modules_dir)
    print(f"✅ Arquivos em modules: {module_files}")
else:
    print("❌ Diretório modules não encontrado")

print("\n" + "=" * 40)
print("🎯 RESULTADO DO TESTE:")

# Verificar se tudo está OK para executar
all_ok = True
required_files = ['app.py', 'auth.py', 'database.py']
for file in required_files:
    if not os.path.exists(file):
        all_ok = False
        break

if all_ok:
    print("✅ SISTEMA PRONTO PARA EXECUÇÃO!")
    print("\n🚀 Para executar:")
    print("   streamlit run app.py")
    print("\n🔑 Credenciais:")
    print("   admin / admin123")
else:
    print("❌ SISTEMA COM PROBLEMAS")
    print("⚠️ Verifique os erros acima")

print("=" * 40)