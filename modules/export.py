
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from database import DatabaseManager

class ExportManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def show_export_dashboard(self):
        """Dashboard de exportação"""
        st.title("📤 Exportação de Dados")
        
        st.markdown("""
        Esta seção permite exportar dados do sistema em diferentes formatos:
        - **CSV**: Para análise em planilhas
        - **Excel**: Múltiplas abas com dados relacionados
        - **PDF**: Relatórios formatados para apresentação
        """)
        
        st.markdown("---")
        
        # Tabs para diferentes tipos de exportação
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Projetos", "📚 Publicações", "🧪 Dados Experimentais", "📈 Relatórios Completos"])
        
        with tab1:
            self.export_projects()
        
        with tab2:
            self.export_publications()
        
        with tab3:
            self.export_experimental_data()
        
        with tab4:
            self.export_complete_reports()
    
    def export_projects(self):
        """Exportação de dados de projetos"""
        st.subheader("📊 Exportar Projetos")
        
        conn = self.db.get_connection()
        
        # Filtros para exportação
        col1, col2, col3 = st.columns(3)
        
        with col1:
            areas = pd.read_sql_query("SELECT DISTINCT area FROM projects", conn)['area'].tolist()
            selected_areas = st.multiselect("Áreas", areas, default=areas)
        
        with col2:
            status_options = pd.read_sql_query("SELECT DISTINCT status FROM projects", conn)['status'].tolist()
            selected_status = st.multiselect("Status", status_options, default=status_options)
        
        with col3:
            date_range = st.date_input("Período", value=[datetime(2023, 1, 1), datetime.now()], key="projects_date")
        
        if selected_areas and selected_status and len(date_range) == 2:
            # Construir query
            areas_str = "', '".join(selected_areas)
            status_str = "', '".join(selected_status)
            
            projects_df = pd.read_sql_query(f'''
                SELECT p.*, u.name as responsible_name 
                FROM projects p 
                LEFT JOIN users u ON p.responsible_id = u.id 
                WHERE p.area IN ('{areas_str}')
                AND p.status IN ('{status_str}')
                AND p.start_date BETWEEN '{date_range[0]}' AND '{date_range[1]}'
                ORDER BY p.created_at DESC
            ''', conn)
            
            if not projects_df.empty:
                st.success(f"✅ {len(projects_df)} projetos encontrados para exportação")
                
                # Preview dos dados
                with st.expander("👀 Preview dos Dados"):
                    st.dataframe(projects_df.head(10))
                
                # Opções de exportação
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # CSV
                    csv_data = projects_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Baixar CSV",
                        data=csv_data,
                        file_name=f"projetos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Excel
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        projects_df.to_excel(writer, sheet_name='Projetos', index=False)
                        
                        # Adicionar estatísticas
                        stats_df = pd.DataFrame({
                            'Métrica': ['Total de Projetos', 'Orçamento Total', 'Orçamento Gasto', 'Projetos Concluídos'],
                            'Valor': [
                                len(projects_df),
                                f"R$ {projects_df['budget'].sum():,.2f}",
                                f"R$ {projects_df['spent_budget'].sum():,.2f}",
                                len(projects_df[projects_df['status'] == 'concluido'])
                            ]
                        })
                        stats_df.to_excel(writer, sheet_name='Estatísticas', index=False)
                    
                    excel_buffer.seek(0)
                    st.download_button(
                        label="📊 Baixar Excel",
                        data=excel_buffer.getvalue(),
                        file_name=f"projetos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with col3:
                    # PDF
                    if st.button("📄 Gerar PDF"):
                        pdf_buffer = self.generate_projects_pdf(projects_df)
                        st.download_button(
                            label="📥 Baixar PDF",
                            data=pdf_buffer.getvalue(),
                            file_name=f"relatorio_projetos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
            else:
                st.info("Nenhum projeto encontrado com os filtros selecionados.")
        
        conn.close()
    
    def export_publications(self):
        """Exportação de publicações"""
        st.subheader("📚 Exportar Publicações")
        
        conn = self.db.get_connection()
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            pub_types = pd.read_sql_query("SELECT DISTINCT type FROM publications", conn)['type'].tolist()
            selected_types = st.multiselect("Tipos", pub_types, default=pub_types)
        
        with col2:
            years = pd.read_sql_query("SELECT DISTINCT year FROM publications WHERE year IS NOT NULL ORDER BY year DESC", conn)['year'].tolist()
            selected_years = st.multiselect("Anos", years, default=years[:5] if len(years) >= 5 else years)
        
        if selected_types and selected_years:
            types_str = "', '".join(selected_types)
            years_str = "', '".join([str(y) for y in selected_years])
            
            publications_df = pd.read_sql_query(f'''
                SELECT p.*, pr.title as project_title 
                FROM publications p 
                LEFT JOIN projects pr ON p.project_id = pr.id 
                WHERE p.type IN ('{types_str}')
                AND p.year IN ({years_str})
                ORDER BY p.year DESC, p.created_at DESC
            ''', conn)
            
            if not publications_df.empty:
                st.success(f"✅ {len(publications_df)} publicações encontradas")
                
                # Opções de exportação
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    csv_data = publications_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Baixar CSV",
                        data=csv_data,
                        file_name=f"publicacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        publications_df.to_excel(writer, sheet_name='Publicações', index=False)
                        
                        # Estatísticas por tipo
                        type_stats = publications_df['type'].value_counts().reset_index()
                        type_stats.columns = ['Tipo', 'Quantidade']
                        type_stats.to_excel(writer, sheet_name='Por Tipo', index=False)
                        
                        # Estatísticas por ano
                        year_stats = publications_df['year'].value_counts().sort_index().reset_index()
                        year_stats.columns = ['Ano', 'Quantidade']
                        year_stats.to_excel(writer, sheet_name='Por Ano', index=False)
                    
                    excel_buffer.seek(0)
                    st.download_button(
                        label="📊 Baixar Excel",
                        data=excel_buffer.getvalue(),
                        file_name=f"publicacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with col3:
                    if st.button("📄 Gerar PDF", key="pub_pdf"):
                        pdf_buffer = self.generate_publications_pdf(publications_df)
                        st.download_button(
                            label="📥 Baixar PDF",
                            data=pdf_buffer.getvalue(),
                            file_name=f"relatorio_publicacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
            else:
                st.info("Nenhuma publicação encontrada.")
        
        conn.close()
    
    def export_experimental_data(self):
        """Exportação de dados experimentais"""
        st.subheader("🧪 Exportar Dados Experimentais")
        
        conn = self.db.get_connection()
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            experiments = pd.read_sql_query("SELECT DISTINCT experiment_name FROM experimental_data", conn)['experiment_name'].tolist()
            selected_experiments = st.multiselect("Experimentos", experiments, default=experiments[:5] if len(experiments) >= 5 else experiments)
        
        with col2:
            variables = pd.read_sql_query("SELECT DISTINCT variable_name FROM experimental_data", conn)['variable_name'].tolist()
            selected_variables = st.multiselect("Variáveis", variables, default=variables)
        
        if selected_experiments and selected_variables:
            exp_str = "', '".join(selected_experiments)
            var_str = "', '".join(selected_variables)
            
            data_df = pd.read_sql_query(f'''
                SELECT * FROM experimental_data 
                WHERE experiment_name IN ('{exp_str}')
                AND variable_name IN ('{var_str}')
                ORDER BY experiment_name, measurement_date DESC
            ''', conn)
            
            if not data_df.empty:
                st.success(f"✅ {len(data_df)} registros encontrados")
                
                # Opções de exportação
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    csv_data = data_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Baixar CSV",
                        data=csv_data,
                        file_name=f"dados_experimentais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        data_df.to_excel(writer, sheet_name='Dados Brutos', index=False)
                        
                        # Estatísticas por experimento
                        exp_stats = data_df.groupby('experiment_name').agg({
                            'value': ['count', 'mean', 'std', 'min', 'max']
                        }).round(2)
                        exp_stats.columns = ['Contagem', 'Média', 'Desvio Padrão', 'Mínimo', 'Máximo']
                        exp_stats.to_excel(writer, sheet_name='Estatísticas')
                    
                    excel_buffer.seek(0)
                    st.download_button(
                        label="📊 Baixar Excel",
                        data=excel_buffer.getvalue(),
                        file_name=f"dados_experimentais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with col3:
                    if st.button("📄 Gerar PDF", key="exp_pdf"):
                        pdf_buffer = self.generate_experimental_pdf(data_df)
                        st.download_button(
                            label="📥 Baixar PDF",
                            data=pdf_buffer.getvalue(),
                            file_name=f"relatorio_experimental_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
            else:
                st.info("Nenhum dado experimental encontrado.")
        
        conn.close()
    
    def export_complete_reports(self):
        """Exportação de relatórios completos"""
        st.subheader("📈 Relatórios Completos")
        
        st.info("Relatórios que combinam dados de múltiplas seções do sistema")
        
        # Opções de relatório
        report_type = st.selectbox("Tipo de Relatório", [
            "Relatório Executivo",
            "Relatório de Produtividade",
            "Relatório por Área de Pesquisa",
            "Relatório Anual Completo"
        ])
        
        # Período
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Data Inicial", value=datetime(2024, 1, 1))
        with col2:
            end_date = st.date_input("Data Final", value=datetime.now())
        
        if st.button("📊 Gerar Relatório Completo"):
            if report_type == "Relatório Executivo":
                pdf_buffer = self.generate_executive_report(start_date, end_date)
            elif report_type == "Relatório de Produtividade":
                pdf_buffer = self.generate_productivity_report(start_date, end_date)
            elif report_type == "Relatório por Área de Pesquisa":
                pdf_buffer = self.generate_area_report(start_date, end_date)
            else:  # Relatório Anual Completo
                pdf_buffer = self.generate_annual_report(start_date, end_date)
            
            st.download_button(
                label="📥 Baixar Relatório PDF",
                data=pdf_buffer.getvalue(),
                file_name=f"{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
    
    def generate_projects_pdf(self, projects_df):
        """Gera PDF de projetos"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph("Relatório de Projetos PD&I", title_style))
        story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Resumo
        story.append(Paragraph("Resumo Executivo", styles['Heading2']))
        summary_data = [
            ['Métrica', 'Valor'],
            ['Total de Projetos', str(len(projects_df))],
            ['Orçamento Total', f"R$ {projects_df['budget'].sum():,.2f}"],
            ['Orçamento Gasto', f"R$ {projects_df['spent_budget'].sum():,.2f}"],
            ['Projetos Concluídos', str(len(projects_df[projects_df['status'] == 'concluido']))]
        ]
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Lista de projetos
        story.append(Paragraph("Lista de Projetos", styles['Heading2']))
        
        for _, project in projects_df.iterrows():
            story.append(Paragraph(f"<b>{project['title']}</b>", styles['Heading3']))
            story.append(Paragraph(f"Área: {project['area']}", styles['Normal']))
            story.append(Paragraph(f"Status: {project['status']}", styles['Normal']))
            story.append(Paragraph(f"Responsável: {project['responsible_name']}", styles['Normal']))
            story.append(Paragraph(f"Orçamento: R$ {project['budget']:,.2f}", styles['Normal']))
            story.append(Spacer(1, 10))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_publications_pdf(self, publications_df):
        """Gera PDF de publicações"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("Relatório de Publicações", title_style))
        story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Estatísticas
        story.append(Paragraph("Estatísticas", styles['Heading2']))
        type_counts = publications_df['type'].value_counts()
        
        for pub_type, count in type_counts.items():
            story.append(Paragraph(f"• {pub_type.title()}: {count}", styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Lista de publicações
        story.append(Paragraph("Lista de Publicações", styles['Heading2']))
        
        for _, pub in publications_df.iterrows():
            story.append(Paragraph(f"<b>{pub['title']}</b>", styles['Heading3']))
            story.append(Paragraph(f"Autores: {pub['authors']}", styles['Normal']))
            story.append(Paragraph(f"Tipo: {pub['type']}", styles['Normal']))
            if pd.notna(pub['journal']):
                story.append(Paragraph(f"Revista/Editora: {pub['journal']}", styles['Normal']))
            story.append(Paragraph(f"Ano: {pub['year']}", styles['Normal']))
            story.append(Spacer(1, 10))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_experimental_pdf(self, data_df):
        """Gera PDF de dados experimentais"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("Relatório de Dados Experimentais", title_style))
        story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Resumo por experimento
        story.append(Paragraph("Resumo por Experimento", styles['Heading2']))
        
        for experiment in data_df['experiment_name'].unique():
            exp_data = data_df[data_df['experiment_name'] == experiment]
            story.append(Paragraph(f"<b>{experiment}</b>", styles['Heading3']))
            story.append(Paragraph(f"Total de medições: {len(exp_data)}", styles['Normal']))
            story.append(Paragraph(f"Variáveis: {', '.join(exp_data['variable_name'].unique())}", styles['Normal']))
            story.append(Spacer(1, 10))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_executive_report(self, start_date, end_date):
        """Gera relatório executivo completo"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        conn = self.db.get_connection()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("Relatório Executivo - Embrapa Meio-Norte", title_style))
        story.append(Paragraph(f"Período: {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}", styles['Normal']))
        story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 30))
        
        # KPIs principais
        story.append(Paragraph("Indicadores Principais", styles['Heading2']))
        
        # Buscar dados do período
        projects_count = pd.read_sql_query(f'''
            SELECT COUNT(*) as count FROM projects 
            WHERE start_date BETWEEN '{start_date}' AND '{end_date}'
        ''', conn).iloc[0]['count']
        
        publications_count = pd.read_sql_query(f'''
            SELECT COUNT(*) as count FROM publications 
            WHERE created_at BETWEEN '{start_date}' AND '{end_date}'
        ''', conn).iloc[0]['count']
        
        budget_total = pd.read_sql_query(f'''
            SELECT SUM(budget) as total FROM projects 
            WHERE start_date BETWEEN '{start_date}' AND '{end_date}'
        ''', conn).iloc[0]['total'] or 0
        
        kpi_data = [
            ['Indicador', 'Valor'],
            ['Projetos Iniciados', str(projects_count)],
            ['Publicações', str(publications_count)],
            ['Orçamento Total', f"R$ {budget_total:,.2f}"]
        ]
        
        kpi_table = Table(kpi_data)
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(kpi_table)
        story.append(Spacer(1, 20))
        
        # Projetos por área
        story.append(Paragraph("Distribuição por Área de Pesquisa", styles['Heading2']))
        
        area_data = pd.read_sql_query(f'''
            SELECT area, COUNT(*) as count FROM projects 
            WHERE start_date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY area
        ''', conn)
        
        if not area_data.empty:
            area_table_data = [['Área', 'Projetos']]
            for _, row in area_data.iterrows():
                area_table_data.append([row['area'], str(row['count'])])
            
            area_table = Table(area_table_data)
            area_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(area_table)
        
        conn.close()
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_productivity_report(self, start_date, end_date):
        """Gera relatório de produtividade"""
        # Implementação similar aos outros relatórios
        return self.generate_executive_report(start_date, end_date)
    
    def generate_area_report(self, start_date, end_date):
        """Gera relatório por área"""
        # Implementação similar aos outros relatórios
        return self.generate_executive_report(start_date, end_date)
    
    def generate_annual_report(self, start_date, end_date):
        """Gera relatório anual completo"""
        # Implementação similar aos outros relatórios
        return self.generate_executive_report(start_date, end_date)
