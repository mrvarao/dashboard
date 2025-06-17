
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from database import DatabaseManager

class ProjectsManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def show_projects_dashboard(self):
        """Dashboard principal de projetos"""
        st.title("📊 Gestão de Projetos PD&I")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        conn = self.db.get_connection()
        
        # Total de projetos
        total_projects = pd.read_sql_query("SELECT COUNT(*) as count FROM projects", conn).iloc[0]['count']
        col1.metric("Total de Projetos", total_projects)
        
        # Projetos em andamento
        active_projects = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM projects WHERE status = 'em_andamento'", conn
        ).iloc[0]['count']
        col2.metric("Em Andamento", active_projects)
        
        # Projetos concluídos
        completed_projects = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM projects WHERE status = 'concluido'", conn
        ).iloc[0]['count']
        col3.metric("Concluídos", completed_projects)
        
        # Orçamento total
        total_budget = pd.read_sql_query(
            "SELECT SUM(budget) as total FROM projects", conn
        ).iloc[0]['total'] or 0
        col4.metric("Orçamento Total", f"R$ {total_budget:,.2f}")
        
        st.markdown("---")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        # Buscar dados para filtros
        areas_df = pd.read_sql_query("SELECT DISTINCT area FROM projects", conn)
        status_df = pd.read_sql_query("SELECT DISTINCT status FROM projects", conn)
        users_df = pd.read_sql_query("SELECT id, name FROM users WHERE role IN ('pesquisador', 'gestor')", conn)
        
        with col1:
            selected_area = st.selectbox("Área", ["Todas"] + areas_df['area'].tolist())
        
        with col2:
            selected_status = st.selectbox("Status", ["Todos"] + status_df['status'].tolist())
        
        with col3:
            selected_responsible = st.selectbox(
                "Responsável", 
                ["Todos"] + [f"{row['name']} (ID: {row['id']})" for _, row in users_df.iterrows()]
            )
        
        # Construir query com filtros
        query = """
            SELECT p.*, u.name as responsible_name 
            FROM projects p 
            LEFT JOIN users u ON p.responsible_id = u.id 
            WHERE 1=1
        """
        params = []
        
        if selected_area != "Todas":
            query += " AND p.area = ?"
            params.append(selected_area)
        
        if selected_status != "Todos":
            query += " AND p.status = ?"
            params.append(selected_status)
        
        if selected_responsible != "Todos":
            responsible_id = selected_responsible.split("ID: ")[1].split(")")[0]
            query += " AND p.responsible_id = ?"
            params.append(int(responsible_id))
        
        # Executar query
        if params:
            projects_df = pd.read_sql_query(query, conn, params=params)
        else:
            projects_df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        # Gráficos
        if not projects_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de status
                status_counts = projects_df['status'].value_counts()
                fig_status = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Distribuição por Status",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_status.update_layout(height=400)
                st.plotly_chart(fig_status, use_container_width=True)
            
            with col2:
                # Gráfico de áreas
                area_counts = projects_df['area'].value_counts()
                fig_area = px.bar(
                    x=area_counts.index,
                    y=area_counts.values,
                    title="Projetos por Área",
                    color=area_counts.values,
                    color_continuous_scale="viridis"
                )
                fig_area.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_area, use_container_width=True)
            
            # Gráfico de orçamento
            if 'budget' in projects_df.columns and 'spent_budget' in projects_df.columns:
                budget_data = projects_df[['title', 'budget', 'spent_budget']].copy()
                budget_data['remaining_budget'] = budget_data['budget'] - budget_data['spent_budget']
                
                fig_budget = go.Figure()
                fig_budget.add_trace(go.Bar(
                    name='Orçamento Total',
                    x=budget_data['title'],
                    y=budget_data['budget'],
                    marker_color='lightblue'
                ))
                fig_budget.add_trace(go.Bar(
                    name='Orçamento Gasto',
                    x=budget_data['title'],
                    y=budget_data['spent_budget'],
                    marker_color='red'
                ))
                
                fig_budget.update_layout(
                    title="Orçamento por Projeto",
                    xaxis_title="Projetos",
                    yaxis_title="Valor (R$)",
                    barmode='group',
                    height=500,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_budget, use_container_width=True)
        
        # Tabela de projetos
        st.subheader("Lista de Projetos")
        if not projects_df.empty:
            # Preparar dados para exibição
            display_df = projects_df[['title', 'area', 'status', 'responsible_name', 'start_date', 'end_date', 'budget', 'spent_budget']].copy()
            display_df.columns = ['Título', 'Área', 'Status', 'Responsável', 'Início', 'Fim', 'Orçamento', 'Gasto']
            
            # Formatar valores monetários
            display_df['Orçamento'] = display_df['Orçamento'].apply(lambda x: f"R$ {x:,.2f}" if pd.notna(x) else "N/A")
            display_df['Gasto'] = display_df['Gasto'].apply(lambda x: f"R$ {x:,.2f}" if pd.notna(x) else "R$ 0,00")
            
            st.dataframe(display_df, use_container_width=True)
            
            # Botão de exportação
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Exportar CSV",
                data=csv,
                file_name=f"projetos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Nenhum projeto encontrado com os filtros selecionados.")
    
    def add_project_form(self):
        """Formulário para adicionar novo projeto"""
        st.subheader("➕ Novo Projeto")
        
        with st.form("new_project_form"):
            title = st.text_input("Título do Projeto*")
            description = st.text_area("Descrição")
            
            col1, col2 = st.columns(2)
            with col1:
                area = st.selectbox("Área*", [
                    "agricultura", "biotecnologia", "sustentabilidade", 
                    "agropecuaria", "recursos_naturais"
                ])
                status = st.selectbox("Status*", [
                    "planejamento", "em_andamento", "concluido", "cancelado"
                ])
            
            with col2:
                # Buscar pesquisadores
                conn = self.db.get_connection()
                users_df = pd.read_sql_query(
                    "SELECT id, name FROM users WHERE role IN ('pesquisador', 'gestor')", conn
                )
                conn.close()
                
                responsible_options = [f"{row['name']} (ID: {row['id']})" for _, row in users_df.iterrows()]
                responsible = st.selectbox("Responsável*", responsible_options)
                
                budget = st.number_input("Orçamento (R$)", min_value=0.0, step=1000.0)
            
            col3, col4 = st.columns(2)
            with col3:
                start_date = st.date_input("Data de Início")
            with col4:
                end_date = st.date_input("Data de Fim")
            
            submitted = st.form_submit_button("Criar Projeto")
            
            if submitted:
                if title and area and responsible:
                    try:
                        responsible_id = int(responsible.split("ID: ")[1].split(")")[0])
                        
                        conn = self.db.get_connection()
                        cursor = conn.cursor()
                        
                        cursor.execute('''
                            INSERT INTO projects (title, description, area, responsible_id, status, start_date, end_date, budget)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (title, description, area, responsible_id, status, start_date, end_date, budget))
                        
                        conn.commit()
                        conn.close()
                        
                        st.success("Projeto criado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao criar projeto: {str(e)}")
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios!")
