"""
Módulo de exportação simplificado para o Dashboard Embrapa
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io
from database import DatabaseManager

class ExportManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def show_export_dashboard(self):
        """Dashboard de exportação simplificado"""
        st.title("📤 Exportação de Dados")
        
        st.markdown("""
        Esta seção permite exportar dados do sistema em diferentes formatos:
        - **CSV**: Para análise em planilhas
        - **Excel**: Múltiplas abas com dados relacionados
        """)
        
        st.markdown("---")
        
        # Tabs para diferentes tipos de exportação
        tab1, tab2, tab3 = st.tabs(["📊 Projetos", "📚 Publicações", "🧪 Dados Experimentais"])
        
        with tab1:
            self.export_projects()
        
        with tab2:
            self.export_publications()
        
        with tab3:
            self.export_experimental_data()
    
    def export_projects(self):
        """Exportação de dados de projetos"""
        st.subheader("📊 Exportar Projetos")
        
        try:
            conn = self.db.get_connection()
            
            # Buscar dados de projetos
            projects_df = pd.read_sql_query('''
                SELECT 
                    p.id,
                    p.title as "Título",
                    p.description as "Descrição", 
                    p.area as "Área",
                    u.name as "Responsável",
                    p.status as "Status",
                    p.start_date as "Data Início",
                    p.end_date as "Data Fim",
                    p.budget as "Orçamento",
                    p.spent_budget as "Gasto"
                FROM projects p
                LEFT JOIN users u ON p.responsible_id = u.id
                ORDER BY p.created_at DESC
            ''', conn)
            
            conn.close()
            
            if not projects_df.empty:
                st.dataframe(projects_df.drop('id', axis=1), use_container_width=True)
                
                # Botões de download
                col1, col2 = st.columns(2)
                
                with col1:
                    csv_data = projects_df.drop('id', axis=1).to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name=f"projetos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Criar Excel em memória
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        projects_df.drop('id', axis=1).to_excel(writer, sheet_name='Projetos', index=False)
                    
                    st.download_button(
                        label="📥 Download Excel",
                        data=excel_buffer.getvalue(),
                        file_name=f"projetos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.info("Nenhum projeto encontrado para exportação")
                
        except Exception as e:
            st.error(f"Erro ao exportar projetos: {str(e)}")
    
    def export_publications(self):
        """Exportação de dados de publicações"""
        st.subheader("📚 Exportar Publicações")
        
        try:
            conn = self.db.get_connection()
            
            # Buscar dados de publicações
            publications_df = pd.read_sql_query('''
                SELECT 
                    title as "Título",
                    authors as "Autores",
                    type as "Tipo",
                    journal as "Revista/Editora",
                    year as "Ano",
                    doi as "DOI"
                FROM publications
                ORDER BY year DESC, title
            ''', conn)
            
            conn.close()
            
            if not publications_df.empty:
                st.dataframe(publications_df, use_container_width=True)
                
                # Botões de download
                col1, col2 = st.columns(2)
                
                with col1:
                    csv_data = publications_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name=f"publicacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Criar Excel em memória
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        publications_df.to_excel(writer, sheet_name='Publicações', index=False)
                    
                    st.download_button(
                        label="📥 Download Excel",
                        data=excel_buffer.getvalue(),
                        file_name=f"publicacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.info("Nenhuma publicação encontrada para exportação")
                
        except Exception as e:
            st.error(f"Erro ao exportar publicações: {str(e)}")
    
    def export_experimental_data(self):
        """Exportação de dados experimentais"""
        st.subheader("🧪 Exportar Dados Experimentais")
        
        try:
            conn = self.db.get_connection()
            
            # Buscar dados experimentais
            experimental_df = pd.read_sql_query('''
                SELECT 
                    e.experiment_name as "Experimento",
                    p.title as "Projeto",
                    e.variable_name as "Variável",
                    e.value as "Valor",
                    e.unit as "Unidade",
                    e.measurement_date as "Data Medição",
                    e.location as "Local",
                    e.notes as "Observações"
                FROM experimental_data e
                LEFT JOIN projects p ON e.project_id = p.id
                ORDER BY e.measurement_date DESC
            ''', conn)
            
            conn.close()
            
            if not experimental_df.empty:
                st.dataframe(experimental_df, use_container_width=True)
                
                # Botões de download
                col1, col2 = st.columns(2)
                
                with col1:
                    csv_data = experimental_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name=f"dados_experimentais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Criar Excel em memória
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        experimental_df.to_excel(writer, sheet_name='Dados Experimentais', index=False)
                    
                    st.download_button(
                        label="📥 Download Excel",
                        data=excel_buffer.getvalue(),
                        file_name=f"dados_experimentais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.info("Nenhum dado experimental encontrado para exportação")
                
        except Exception as e:
            st.error(f"Erro ao exportar dados experimentais: {str(e)}")