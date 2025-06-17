
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database import DatabaseManager
import io

class PublicationsManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def show_publications_dashboard(self):
        """Dashboard de publicações"""
        st.title("📚 Gestão de Publicações")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        conn = self.db.get_connection()
        
        # Total de publicações
        total_pubs = pd.read_sql_query("SELECT COUNT(*) as count FROM publications", conn).iloc[0]['count']
        col1.metric("Total Publicações", total_pubs)
        
        # Publicações este ano
        current_year = datetime.now().year
        year_pubs = pd.read_sql_query(f"SELECT COUNT(*) as count FROM publications WHERE year = {current_year}", conn).iloc[0]['count']
        col2.metric(f"Publicações {current_year}", year_pubs)
        
        # Artigos científicos
        articles = pd.read_sql_query("SELECT COUNT(*) as count FROM publications WHERE type = 'artigo'", conn).iloc[0]['count']
        col3.metric("Artigos Científicos", articles)
        
        # Livros e capítulos
        books = pd.read_sql_query("SELECT COUNT(*) as count FROM publications WHERE type IN ('livro', 'capitulo')", conn).iloc[0]['count']
        col4.metric("Livros/Capítulos", books)
        
        conn.close()
        
        st.markdown("---")
        
        # Tabs para diferentes funcionalidades
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualização", "➕ Nova Publicação", "🔍 Busca", "📈 Análises"])
        
        with tab1:
            self.show_publications_overview()
        
        with tab2:
            self.add_publication_form()
        
        with tab3:
            self.search_publications()
        
        with tab4:
            self.show_publications_analysis()
    
    def show_publications_overview(self):
        """Visão geral das publicações"""
        st.subheader("Visão Geral das Publicações")
        
        conn = self.db.get_connection()
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            years = pd.read_sql_query("SELECT DISTINCT year FROM publications ORDER BY year DESC", conn)['year'].tolist()
            selected_year = st.selectbox("Ano", ["Todos"] + [str(y) for y in years if y])
        
        with col2:
            types = pd.read_sql_query("SELECT DISTINCT type FROM publications", conn)['type'].tolist()
            selected_type = st.selectbox("Tipo", ["Todos"] + types)
        
        with col3:
            # Busca por projeto
            projects = pd.read_sql_query("SELECT id, title FROM projects", conn)
            project_options = ["Todos"] + [f"{row['title']} (ID: {row['id']})" for _, row in projects.iterrows()]
            selected_project = st.selectbox("Projeto", project_options)
        
        # Construir query com filtros
        query = """
            SELECT p.*, pr.title as project_title 
            FROM publications p 
            LEFT JOIN projects pr ON p.project_id = pr.id 
            WHERE 1=1
        """
        params = []
        
        if selected_year != "Todos":
            query += " AND p.year = ?"
            params.append(int(selected_year))
        
        if selected_type != "Todos":
            query += " AND p.type = ?"
            params.append(selected_type)
        
        if selected_project != "Todos":
            project_id = selected_project.split("ID: ")[1].split(")")[0]
            query += " AND p.project_id = ?"
            params.append(int(project_id))
        
        query += " ORDER BY p.year DESC, p.created_at DESC"
        
        # Executar query
        if params:
            publications_df = pd.read_sql_query(query, conn, params=params)
        else:
            publications_df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        if not publications_df.empty:
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                # Publicações por tipo
                type_counts = publications_df['type'].value_counts()
                fig_type = px.pie(
                    values=type_counts.values,
                    names=type_counts.index,
                    title="Distribuição por Tipo",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_type.update_layout(height=400)
                st.plotly_chart(fig_type, use_container_width=True)
            
            with col2:
                # Publicações por ano
                if 'year' in publications_df.columns:
                    year_counts = publications_df['year'].value_counts().sort_index()
                    fig_year = px.bar(
                        x=year_counts.index,
                        y=year_counts.values,
                        title="Publicações por Ano",
                        color=year_counts.values,
                        color_continuous_scale="viridis"
                    )
                    fig_year.update_layout(height=400)
                    st.plotly_chart(fig_year, use_container_width=True)
            
            # Tabela de publicações
            st.subheader("Lista de Publicações")
            display_df = publications_df[['title', 'authors', 'type', 'journal', 'year', 'doi', 'project_title']].copy()
            display_df.columns = ['Título', 'Autores', 'Tipo', 'Revista/Editora', 'Ano', 'DOI', 'Projeto']
            display_df['Projeto'] = display_df['Projeto'].fillna('N/A')
            display_df['DOI'] = display_df['DOI'].fillna('N/A')
            
            st.dataframe(display_df, use_container_width=True)
            
            # Exportação
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Exportar CSV",
                data=csv,
                file_name=f"publicacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Nenhuma publicação encontrada com os filtros selecionados.")
    
    def add_publication_form(self):
        """Formulário para adicionar nova publicação"""
        st.subheader("➕ Nova Publicação")
        
        with st.form("new_publication_form"):
            title = st.text_input("Título*")
            authors = st.text_input("Autores*", help="Separar múltiplos autores por ponto e vírgula")
            
            col1, col2 = st.columns(2)
            with col1:
                pub_type = st.selectbox("Tipo*", [
                    "artigo", "livro", "capitulo", "relatorio", "tese"
                ])
                year = st.number_input("Ano*", min_value=1900, max_value=datetime.now().year + 1, value=datetime.now().year)
            
            with col2:
                journal = st.text_input("Revista/Editora")
                doi = st.text_input("DOI")
            
            # Projeto associado
            conn = self.db.get_connection()
            projects_df = pd.read_sql_query("SELECT id, title FROM projects", conn)
            conn.close()
            
            project_options = ["Nenhum"] + [f"{row['title']} (ID: {row['id']})" for _, row in projects_df.iterrows()]
            associated_project = st.selectbox("Projeto Associado", project_options)
            
            # Upload de arquivo
            uploaded_file = st.file_uploader("Arquivo da Publicação", type=['pdf', 'doc', 'docx'])
            
            submitted = st.form_submit_button("Adicionar Publicação")
            
            if submitted:
                if title and authors and pub_type:
                    try:
                        project_id = None
                        if associated_project != "Nenhum":
                            project_id = int(associated_project.split("ID: ")[1].split(")")[0])
                        
                        file_path = None
                        if uploaded_file is not None:
                            # Salvar arquivo (simulação)
                            file_path = f"uploads/{uploaded_file.name}"
                        
                        conn = self.db.get_connection()
                        cursor = conn.cursor()
                        
                        cursor.execute('''
                            INSERT INTO publications (title, authors, type, journal, year, doi, file_path, project_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (title, authors, pub_type, journal, year, doi, file_path, project_id))
                        
                        conn.commit()
                        conn.close()
                        
                        st.success("Publicação adicionada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao adicionar publicação: {str(e)}")
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios!")
    
    def search_publications(self):
        """Busca avançada de publicações"""
        st.subheader("🔍 Busca Avançada")
        
        # Campos de busca
        col1, col2 = st.columns(2)
        
        with col1:
            search_title = st.text_input("Buscar no título")
            search_authors = st.text_input("Buscar nos autores")
        
        with col2:
            search_journal = st.text_input("Buscar na revista/editora")
            search_doi = st.text_input("Buscar por DOI")
        
        if st.button("🔍 Buscar"):
            conn = self.db.get_connection()
            
            # Construir query de busca
            query = "SELECT * FROM publications WHERE 1=1"
            params = []
            
            if search_title:
                query += " AND title LIKE ?"
                params.append(f"%{search_title}%")
            
            if search_authors:
                query += " AND authors LIKE ?"
                params.append(f"%{search_authors}%")
            
            if search_journal:
                query += " AND journal LIKE ?"
                params.append(f"%{search_journal}%")
            
            if search_doi:
                query += " AND doi LIKE ?"
                params.append(f"%{search_doi}%")
            
            query += " ORDER BY year DESC, created_at DESC"
            
            if params:
                results_df = pd.read_sql_query(query, conn, params=params)
            else:
                results_df = pd.read_sql_query("SELECT * FROM publications ORDER BY year DESC", conn)
            
            conn.close()
            
            if not results_df.empty:
                st.success(f"Encontradas {len(results_df)} publicações")
                
                display_df = results_df[['title', 'authors', 'type', 'journal', 'year', 'doi']].copy()
                display_df.columns = ['Título', 'Autores', 'Tipo', 'Revista/Editora', 'Ano', 'DOI']
                display_df['DOI'] = display_df['DOI'].fillna('N/A')
                
                st.dataframe(display_df, use_container_width=True)
            else:
                st.info("Nenhuma publicação encontrada com os critérios de busca.")
    
    def show_publications_analysis(self):
        """Análises avançadas de publicações"""
        st.subheader("📈 Análises de Publicações")
        
        conn = self.db.get_connection()
        
        # Análise temporal
        temporal_data = pd.read_sql_query('''
            SELECT year, type, COUNT(*) as count
            FROM publications 
            WHERE year IS NOT NULL
            GROUP BY year, type
            ORDER BY year
        ''', conn)
        
        if not temporal_data.empty:
            st.subheader("📊 Evolução Temporal por Tipo")
            fig_temporal = px.line(
                temporal_data,
                x='year',
                y='count',
                color='type',
                title="Publicações por Ano e Tipo",
                markers=True
            )
            fig_temporal.update_layout(height=500)
            st.plotly_chart(fig_temporal, use_container_width=True)
        
        # Análise de produtividade por projeto
        project_analysis = pd.read_sql_query('''
            SELECT pr.title as project_title, pr.area, COUNT(p.id) as publications_count
            FROM projects pr
            LEFT JOIN publications p ON pr.id = p.project_id
            GROUP BY pr.id, pr.title, pr.area
            HAVING publications_count > 0
            ORDER BY publications_count DESC
        ''', conn)
        
        if not project_analysis.empty:
            st.subheader("🎯 Publicações por Projeto")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top projetos com mais publicações
                top_projects = project_analysis.head(10)
                fig_projects = px.bar(
                    top_projects,
                    x='publications_count',
                    y='project_title',
                    orientation='h',
                    title="Top 10 Projetos - Publicações",
                    color='publications_count',
                    color_continuous_scale='blues'
                )
                fig_projects.update_layout(height=500)
                st.plotly_chart(fig_projects, use_container_width=True)
            
            with col2:
                # Publicações por área
                area_analysis = project_analysis.groupby('area')['publications_count'].sum().reset_index()
                fig_areas = px.pie(
                    area_analysis,
                    values='publications_count',
                    names='area',
                    title="Publicações por Área de Pesquisa",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_areas.update_layout(height=500)
                st.plotly_chart(fig_areas, use_container_width=True)
        
        # Estatísticas gerais
        st.subheader("📊 Estatísticas Gerais")
        
        stats_data = pd.read_sql_query('''
            SELECT 
                COUNT(*) as total_publications,
                COUNT(DISTINCT authors) as unique_author_combinations,
                AVG(CASE WHEN year IS NOT NULL THEN year END) as avg_year,
                MIN(year) as oldest_year,
                MAX(year) as newest_year
            FROM publications
        ''', conn)
        
        if not stats_data.empty:
            col1, col2, col3, col4, col5 = st.columns(5)
            
            stats = stats_data.iloc[0]
            col1.metric("Total", int(stats['total_publications']))
            col2.metric("Combinações de Autores", int(stats['unique_author_combinations']))
            col3.metric("Ano Médio", f"{stats['avg_year']:.0f}" if stats['avg_year'] else "N/A")
            col4.metric("Mais Antiga", int(stats['oldest_year']) if stats['oldest_year'] else "N/A")
            col5.metric("Mais Recente", int(stats['newest_year']) if stats['newest_year'] else "N/A")
        
        conn.close()
