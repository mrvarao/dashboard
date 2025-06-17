
import streamlit as st
import sqlite3
import hashlib
from database import DatabaseManager

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def hash_password(self, password):
        """Gera hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username, password):
        """Autentica usuário"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        hashed_password = self.hash_password(password)
        cursor.execute('''
            SELECT id, username, name, email, role, department 
            FROM users 
            WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'name': user[2],
                'email': user[3],
                'role': user[4],
                'department': user[5]
            }
        return None
    
    def login_form(self):
        """Formulário de login"""
        st.title("🌱 Dashboard Embrapa Meio-Norte")
        st.markdown("---")
        
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submit_button = st.form_submit_button("Entrar")
            
            if submit_button:
                if username and password:
                    user = self.authenticate_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.authenticated = True
                        st.success(f"Bem-vindo, {user['name']}!")
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos!")
                else:
                    st.error("Por favor, preencha todos os campos!")
        
        # Informações de login para teste
        st.markdown("---")
        st.info("""
        **Usuários de teste:**
        - **Administrador:** admin / admin123
        - **Pesquisador:** joao.silva / pesq123
        - **Gestor:** maria.santos / gest123
        """)
    
    def logout(self):
        """Logout do usuário"""
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()
    
    def check_permission(self, required_role=None):
        """Verifica permissões do usuário"""
        if not st.session_state.get('authenticated', False):
            return False
        
        if required_role is None:
            return True
        
        user_role = st.session_state.user['role']
        
        # Hierarquia de permissões
        role_hierarchy = {
            'administrador': 3,
            'gestor': 2,
            'pesquisador': 1
        }
        
        return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)
