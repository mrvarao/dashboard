
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import DatabaseManager

class KPIManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def show_kpi_dashboard(self):
        """Dashboard de indicadores de desempenho"""
        st.title("📈 Indicadores de Desempenho")
        
        # Período de análise
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Data Inicial", value=datetime.now() - timedelta(days=365))
        with col2:
            end_date = st.date_input("Data Final", value=datetime.now())
        
        st.markdown("---")
        
        # KPIs principais
        self.show_main_kpis(start_date, end_date)
        
        st.markdown("---")
        
        # Gráficos detalhados
        col1, col2 = st.columns(2)
        
        with col1:
            self.show_projects_kpi(start_date, end_date)
            self.show_budget_kpi(start_date, end_date)
        
        with col2:
            self.show_publications_kpi(start_date, end_date)
            self.show_training_kpi(start_date, end_date)
        
        # Análise de produtividade
        st.markdown("---")
        self.show_productivity_analysis(start_date, end_date)
    
    def show_main_kpis(self, start_date, end_date):
        """Exibe os KPIs principais"""
        conn = self.db.get_connection()
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        # Número de publicações
        publications_count = pd.read_sql_query(f'''
            SELECT COUNT(*) as count FROM publications 
            WHERE created_at BETWEEN '{start_date}' AND '{end_date}'
        ''', conn).iloc[0]['count']
        col1.metric("📚 Publicações", publications_count)
        
        # Projetos concluídos
        completed_projects = pd.read_sql_query(f'''
            SELECT COUNT(*) as count FROM projects 
            WHERE status = 'concluido' AND end_date BETWEEN '{start_date}' AND '{end_date}'
        ''', conn).iloc[0]['count']
        col2.metric("✅ Projetos Concluídos", completed_projects)
        
        # Orçamento utilizado
        budget_used = pd.read_sql_query(f'''
            SELECT SUM(spent_budget) as total FROM projects 
            WHERE start_date BETWEEN '{start_date}' AND '{end_date}'
        ''', conn).iloc[0]['total'] or 0
        col3.metric("💰 Orçamento Usado", f"R$ {budget_used:,.0f}")
        
        # Treinamentos realizados
        trainings_count = pd.read_sql_query(f'''
            SELECT COUNT(*) as count FROM events 
            WHERE type = 'treinamento' AND end_date BETWEEN '{start_date}' AND '{end_date}'
        ''', conn).iloc[0]['count']
        col4.metric("🎓 Treinamentos", trainings_count)
        
        # Tempo médio de execução
        avg_duration = pd.read_sql_query(f'''
            SELECT AVG(julianday(end_date) - julianday(start_date)) as avg_days 
            FROM projects 
            WHERE status = 'concluido' AND end_date BETWEEN '{start_date}' AND '{end_date}'
        ''', conn).iloc[0]['avg_days']
        avg_duration = int(avg_duration) if avg_duration else 0
        col5.metric("⏱️ Tempo Médio (dias)", avg_duration)
        
        # Pesquisadores ativos
        active_researchers = pd.read_sql_query(f'''
            SELECT COUNT(DISTINCT responsible_id) as count FROM projects 
            WHERE start_date BETWEEN '{start_date}' AND '{end_date}'
        ''', conn).iloc[0]['count']
        col6.metric("👨‍🔬 Pesquisadores Ativos", active_researchers)
        
        conn.close()
    
    def show_projects_kpi(self, start_date, end_date):
        """KPI de projetos"""
        st.subheader("📊 Projetos por Status")
        
        conn = self.db.get_connection()
        projects_status = pd.read_sql_query(f'''
            SELECT status, COUNT(*) as count 
            FROM projects 
            WHERE start_date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY status
        ''', conn)
        conn.close()
        
        if not projects_status.empty:
            fig = px.donut(
                projects_status, 
                values='count', 
                names='status',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum projeto no período selecionado.")
    
    def show_budget_kpi(self, start_date, end_date):
        """KPI de orçamento"""
        st.subheader("💰 Execução Orçamentária")
        
        conn = self.db.get_connection()
        budget_data = pd.read_sql_query(f'''
            SELECT area, SUM(budget) as total_budget, SUM(spent_budget) as total_spent
            FROM projects 
            WHERE start_date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY area
        ''', conn)
        conn.close()
        
        if not budget_data.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Orçamento Total',
                x=budget_data['area'],
                y=budget_data['total_budget'],
                marker_color='lightblue'
            ))
            fig.add_trace(go.Bar(
                name='Orçamento Gasto',
                x=budget_data['area'],
                y=budget_data['total_spent'],
                marker_color='red'
            ))
            
            fig.update_layout(
                title="Orçamento por Área",
                barmode='group',
                height=300,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum dado orçamentário no período.")
    
    def show_publications_kpi(self, start_date, end_date):
        """KPI de publicações"""
        st.subheader("📚 Publicações por Tipo")
        
        conn = self.db.get_connection()
        publications_type = pd.read_sql_query(f'''
            SELECT type, COUNT(*) as count 
            FROM publications 
            WHERE created_at BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY type
        ''', conn)
        conn.close()
        
        if not publications_type.empty:
            fig = px.bar(
                publications_type,
                x='type',
                y='count',
                color='count',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=300, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma publicação no período selecionado.")
    
    def show_training_kpi(self, start_date, end_date):
        """KPI de treinamentos"""
        st.subheader("🎓 Eventos por Mês")
        
        conn = self.db.get_connection()
        events_monthly = pd.read_sql_query(f'''
            SELECT strftime('%Y-%m', start_date) as month, COUNT(*) as count
            FROM events 
            WHERE start_date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY strftime('%Y-%m', start_date)
            ORDER BY month
        ''', conn)
        conn.close()
        
        if not events_monthly.empty:
            fig = px.line(
                events_monthly,
                x='month',
                y='count',
                markers=True,
                line_shape='spline'
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum evento no período selecionado.")
    
    def show_productivity_analysis(self, start_date, end_date):
        """Análise de produtividade por pesquisador"""
        st.subheader("👨‍🔬 Produtividade por Pesquisador")
        
        conn = self.db.get_connection()
        
        # Produtividade por pesquisador
        productivity_data = pd.read_sql_query(f'''
            SELECT u.name, 
                   COUNT(DISTINCT p.id) as total_projects,
                   COUNT(DISTINCT pub.id) as total_publications,
                   AVG(p.budget) as avg_budget
            FROM users u
            LEFT JOIN projects p ON u.id = p.responsible_id 
                AND p.start_date BETWEEN '{start_date}' AND '{end_date}'
            LEFT JOIN publications pub ON p.id = pub.project_id
            WHERE u.role IN ('pesquisador', 'gestor')
            GROUP BY u.id, u.name
            HAVING total_projects > 0
            ORDER BY total_projects DESC
        ''', conn)
        
        conn.close()
        
        if not productivity_data.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de projetos por pesquisador
                fig_projects = px.bar(
                    productivity_data.head(10),
                    x='name',
                    y='total_projects',
                    title="Top 10 - Projetos por Pesquisador",
                    color='total_projects',
                    color_continuous_scale='blues'
                )
                fig_projects.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_projects, use_container_width=True)
            
            with col2:
                # Gráfico de publicações por pesquisador
                fig_pubs = px.bar(
                    productivity_data.head(10),
                    x='name',
                    y='total_publications',
                    title="Top 10 - Publicações por Pesquisador",
                    color='total_publications',
                    color_continuous_scale='greens'
                )
                fig_pubs.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_pubs, use_container_width=True)
            
            # Tabela de produtividade
            st.subheader("📊 Ranking de Produtividade")
            display_df = productivity_data.copy()
            display_df['avg_budget'] = display_df['avg_budget'].fillna(0).round(0).astype(int)
            display_df.columns = ['Pesquisador', 'Total Projetos', 'Total Publicações', 'Orçamento Médio (R$)']
            
            # Adicionar ranking
            display_df['Ranking'] = range(1, len(display_df) + 1)
            display_df = display_df[['Ranking', 'Pesquisador', 'Total Projetos', 'Total Publicações', 'Orçamento Médio (R$)']]
            
            st.dataframe(display_df, use_container_width=True)
            
            # Exportar dados de produtividade
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Exportar Produtividade",
                data=csv,
                file_name=f"produtividade_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Nenhum dado de produtividade disponível para o período selecionado.")
    
    def show_custom_kpis(self):
        """KPIs customizáveis"""
        st.subheader("🎯 KPIs Customizados")
        
        # Permitir ao usuário criar KPIs personalizados
        with st.expander("➕ Criar KPI Personalizado"):
            kpi_name = st.text_input("Nome do KPI")
            kpi_description = st.text_area("Descrição")
            
            # Opções de métricas
            metric_type = st.selectbox("Tipo de Métrica", [
                "Contagem", "Soma", "Média", "Percentual"
            ])
            
            table_source = st.selectbox("Fonte de Dados", [
                "projects", "publications", "events", "experimental_data"
            ])
            
            if st.button("Criar KPI"):
                st.success(f"KPI '{kpi_name}' criado com sucesso!")
                st.info("Funcionalidade de KPIs customizados pode ser expandida conforme necessidade.")
