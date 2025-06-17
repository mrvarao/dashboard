import streamlit as st
import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuração da página
st.set_page_config(
    page_title="Dashboard Embrapa Meio-Norte",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estado da sessão
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None

# Se não autenticado, mostrar login
if not st.session_state.authenticated:
    st.title("🌱 Dashboard Embrapa Meio-Norte")
    st.markdown("---")
    
    with st.form("login_form"):
        st.subheader("Login")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit_button = st.form_submit_button("Entrar")
        
        if submit_button:
            # Verificação simples de login
            if username == "admin" and password == "admin123":
                st.session_state.authenticated = True
                st.session_state.user = {
                    'name': 'Administrador',
                    'role': 'administrador',
                    'email': 'admin@embrapa.br'
                }
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos!")
    
    # Informações de login
    st.markdown("---")
    st.info("""
    **Usuários de teste:**
    - **Administrador:** admin / admin123
    """)

else:
    # Dashboard principal
    st.title("🌱 Dashboard Embrapa Meio-Norte")
    st.success(f"Bem-vindo, {st.session_state.user['name']}!")
    
    # Sidebar
    with st.sidebar:
        st.subheader("Menu")
        if st.button("🚪 Sair"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    # Conteúdo principal
    st.subheader("Sistema de Gestão de PD&I")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Projetos", "5")
    
    with col2:
        st.metric("📚 Publicações", "12")
    
    with col3:
        st.metric("👥 Funcionários", "25")
    
    with col4:
        st.metric("🧪 Experimentos", "8")
    
    st.markdown("---")
    st.info("Dashboard simplificado funcionando corretamente! ✅")
    st.success("Todas as funcionalidades principais estão disponíveis no sistema completo.")
