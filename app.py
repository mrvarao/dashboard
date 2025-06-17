
import streamlit as st
import sys
import os

# Adicionar o diretório atual ao path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth import AuthManager
from database import DatabaseManager
from modules.projects import ProjectsManager
from modules.admin import AdminManager
from modules.kpis import KPIManager
from modules.publications import PublicationsManager
from modules.experimental_data import ExperimentalDataManager
from modules.alerts import AlertsManager
try:
    from modules.export import ExportManager
except ImportError:
    from modules.export_simple import ExportManager

# Configuração da página
st.set_page_config(
    page_title="Dashboard Embrapa Meio-Norte",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E8B57, #228B22);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2E8B57;
    }
    
    .sidebar-logo {
        text-align: center;
        padding: 1rem;
        background: #f0f8f0;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .alert-high {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 10px;
        margin: 5px 0;
    }
    
    .alert-medium {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 10px;
        margin: 5px 0;
    }
    
    .alert-low {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 10px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Inicializa o estado da sessão"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None

def show_sidebar():
    """Exibe a barra lateral com navegação"""
    with st.sidebar:
        # Logo e título
        st.markdown("""
        <div class="sidebar-logo">
            <h2>🌱 Embrapa</h2>
            <p>Meio-Norte</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Informações do usuário
        if st.session_state.authenticated:
            user = st.session_state.user
            st.markdown(f"""
            **👤 {user['name']}**  
            📧 {user['email']}  
            🏢 {user['department']}  
            🔑 {user['role'].title()}
            """)
            
            st.markdown("---")
            
            # Menu de navegação
            st.subheader("📋 Menu Principal")
            
            # Verificar permissões para cada seção
            auth = AuthManager()
            
            menu_options = []
            
            # Dashboard sempre disponível
            menu_options.append("🏠 Dashboard")
            
            # Projetos PD&I
            menu_options.append("📊 Projetos PD&I")
            
            # Gestão Administrativa (apenas admin e gestor)
            if auth.check_permission('gestor'):
                menu_options.append("👥 Gestão Administrativa")
            
            # KPIs (todos podem ver)
            menu_options.append("📈 Indicadores (KPIs)")
            
            # Publicações
            menu_options.append("📚 Publicações")
            
            # Dados Experimentais
            menu_options.append("🧪 Dados Experimentais")
            
            # Alertas
            menu_options.append("🔔 Alertas")
            
            # Exportação
            menu_options.append("📤 Exportação")
            
            # Seleção do menu
            selected_page = st.selectbox("Selecione uma seção:", menu_options)
            
            st.markdown("---")
            
            # Alertas rápidos na sidebar
            alerts_manager = AlertsManager()
            show_sidebar_alerts(user['id'])
            
            st.markdown("---")
            
            # Botão de logout
            if st.button("🚪 Sair", use_container_width=True):
                auth.logout()
            
            return selected_page
        
        return None

def show_sidebar_alerts(user_id):
    """Exibe alertas rápidos na sidebar"""
    st.subheader("🔔 Alertas Recentes")
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        # Buscar alertas não lidos do usuário
        import pandas as pd
        recent_alerts = pd.read_sql_query(f'''
            SELECT title, priority, created_at 
            FROM alerts 
            WHERE user_id = {user_id} AND read = 0 
            ORDER BY created_at DESC 
            LIMIT 3
        ''', conn)
        
        conn.close()
        
        if not recent_alerts.empty:
            for _, alert in recent_alerts.iterrows():
                priority_icon = "🔴" if alert['priority'] == 'alta' else "🟡" if alert['priority'] == 'media' else "🟢"
                st.markdown(f"{priority_icon} {alert['title'][:30]}...")
        else:
            st.info("Nenhum alerta pendente")
    
    except Exception as e:
        st.error(f"Erro ao carregar alertas: {str(e)}")

def show_dashboard_home():
    """Exibe o dashboard principal"""
    st.markdown("""
    <div class="main-header">
        <h1>🌱 Dashboard Embrapa Meio-Norte</h1>
        <p>Sistema de Gestão de PD&I e Processos Administrativos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        import pandas as pd
        
        # Total de projetos
        total_projects = pd.read_sql_query("SELECT COUNT(*) as count FROM projects", conn).iloc[0]['count']
        col1.metric("📊 Total de Projetos", total_projects)
        
        # Projetos em andamento
        active_projects = pd.read_sql_query("SELECT COUNT(*) as count FROM projects WHERE status = 'em_andamento'", conn).iloc[0]['count']
        col2.metric("🔄 Em Andamento", active_projects)
        
        # Total de publicações
        total_publications = pd.read_sql_query("SELECT COUNT(*) as count FROM publications", conn).iloc[0]['count']
        col3.metric("📚 Publicações", total_publications)
        
        # Funcionários ativos
        active_employees = pd.read_sql_query("SELECT COUNT(*) as count FROM employees WHERE active = 1", conn).iloc[0]['count']
        col4.metric("👥 Funcionários", active_employees)
        
        conn.close()
        
    except Exception as e:
        st.error(f"Erro ao carregar métricas: {str(e)}")
    
    st.markdown("---")
    
    # Gráficos resumo
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Projetos por Status")
        try:
            db = DatabaseManager()
            conn = db.get_connection()
            
            status_data = pd.read_sql_query("SELECT status, COUNT(*) as count FROM projects GROUP BY status", conn)
            
            if not status_data.empty:
                import plotly.express as px
                fig = px.pie(status_data, values='count', names='status', 
                           title="Distribuição de Projetos por Status")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhum projeto cadastrado")
            
            conn.close()
        except Exception as e:
            st.error(f"Erro ao carregar gráfico: {str(e)}")
    
    with col2:
        st.subheader("📈 Publicações por Tipo")
        try:
            db = DatabaseManager()
            conn = db.get_connection()
            
            pub_data = pd.read_sql_query("SELECT type, COUNT(*) as count FROM publications GROUP BY type", conn)
            
            if not pub_data.empty:
                import plotly.express as px
                fig = px.bar(pub_data, x='type', y='count', 
                           title="Publicações por Tipo")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhuma publicação cadastrada")
            
            conn.close()
        except Exception as e:
            st.error(f"Erro ao carregar gráfico: {str(e)}")
    
    # Informações do sistema
    st.markdown("---")
    st.subheader("ℹ️ Sobre o Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **📊 Gestão de Projetos**
        - Cadastro e acompanhamento
        - Controle orçamentário
        - Relatórios de progresso
        """)
    
    with col2:
        st.info("""
        **👥 Gestão Administrativa**
        - Cadastro de funcionários
        - Organograma
        - Eventos e treinamentos
        """)
    
    with col3:
        st.info("""
        **📈 Análises e Relatórios**
        - KPIs customizáveis
        - Dados experimentais
        - Exportação em múltiplos formatos
        """)

def main():
    """Função principal da aplicação"""
    initialize_session_state()
    
    # Inicializar banco de dados
    try:
        db = DatabaseManager()
        db.populate_sample_data()  # Popula dados apenas se não existirem
    except Exception as e:
        st.error(f"Erro ao inicializar banco de dados: {str(e)}")
        return
    
    # Verificar autenticação
    if not st.session_state.authenticated:
        auth = AuthManager()
        auth.login_form()
        return
    
    # Mostrar sidebar e obter página selecionada
    selected_page = show_sidebar()
    
    if selected_page is None:
        return
    
    # Roteamento de páginas
    try:
        if selected_page == "🏠 Dashboard":
            show_dashboard_home()
        
        elif selected_page == "📊 Projetos PD&I":
            projects_manager = ProjectsManager()
            
            # Sub-tabs para projetos
            tab1, tab2 = st.tabs(["📊 Dashboard", "➕ Novo Projeto"])
            
            with tab1:
                projects_manager.show_projects_dashboard()
            
            with tab2:
                # Verificar permissão para criar projetos
                auth = AuthManager()
                if auth.check_permission('pesquisador'):
                    projects_manager.add_project_form()
                else:
                    st.error("❌ Você não tem permissão para criar projetos.")
        
        elif selected_page == "👥 Gestão Administrativa":
            admin_manager = AdminManager()
            admin_manager.show_admin_dashboard()
        
        elif selected_page == "📈 Indicadores (KPIs)":
            kpi_manager = KPIManager()
            kpi_manager.show_kpi_dashboard()
        
        elif selected_page == "📚 Publicações":
            publications_manager = PublicationsManager()
            publications_manager.show_publications_dashboard()
        
        elif selected_page == "🧪 Dados Experimentais":
            experimental_manager = ExperimentalDataManager()
            experimental_manager.show_experimental_dashboard()
        
        elif selected_page == "🔔 Alertas":
            alerts_manager = AlertsManager()
            alerts_manager.show_alerts_dashboard()
        
        elif selected_page == "📤 Exportação":
            export_manager = ExportManager()
            export_manager.show_export_dashboard()
    
    except Exception as e:
        st.error(f"Erro ao carregar página: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
