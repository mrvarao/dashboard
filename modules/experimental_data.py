
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats
from datetime import datetime
from database import DatabaseManager
import io

class ExperimentalDataManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def show_experimental_dashboard(self):
        """Dashboard de dados experimentais"""
        st.title("🧪 Dados Experimentais")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        conn = self.db.get_connection()
        
        # Total de registros
        total_records = pd.read_sql_query("SELECT COUNT(*) as count FROM experimental_data", conn).iloc[0]['count']
        col1.metric("Total Registros", total_records)
        
        # Experimentos únicos
        unique_experiments = pd.read_sql_query("SELECT COUNT(DISTINCT experiment_name) as count FROM experimental_data", conn).iloc[0]['count']
        col2.metric("Experimentos", unique_experiments)
        
        # Variáveis medidas
        unique_variables = pd.read_sql_query("SELECT COUNT(DISTINCT variable_name) as count FROM experimental_data", conn).iloc[0]['count']
        col3.metric("Variáveis", unique_variables)
        
        # Locais de coleta
        unique_locations = pd.read_sql_query("SELECT COUNT(DISTINCT location) as count FROM experimental_data", conn).iloc[0]['count']
        col4.metric("Locais", unique_locations)
        
        conn.close()
        
        st.markdown("---")
        
        # Tabs para diferentes funcionalidades
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Visualização", "📤 Importar CSV", "📈 Análise Estatística", "🔍 Exploração", "📋 Relatórios"])
        
        with tab1:
            self.show_data_visualization()
        
        with tab2:
            self.import_csv_data()
        
        with tab3:
            self.statistical_analysis()
        
        with tab4:
            self.data_exploration()
        
        with tab5:
            self.generate_reports()
    
    def show_data_visualization(self):
        """Visualização dos dados experimentais"""
        st.subheader("📊 Visualização de Dados")
        
        conn = self.db.get_connection()
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            experiments = pd.read_sql_query("SELECT DISTINCT experiment_name FROM experimental_data", conn)['experiment_name'].tolist()
            selected_experiment = st.selectbox("Experimento", ["Todos"] + experiments)
        
        with col2:
            variables = pd.read_sql_query("SELECT DISTINCT variable_name FROM experimental_data", conn)['variable_name'].tolist()
            selected_variable = st.selectbox("Variável", ["Todas"] + variables)
        
        with col3:
            locations = pd.read_sql_query("SELECT DISTINCT location FROM experimental_data", conn)['location'].tolist()
            selected_location = st.selectbox("Local", ["Todos"] + locations)
        
        # Construir query com filtros
        query = "SELECT * FROM experimental_data WHERE 1=1"
        params = []
        
        if selected_experiment != "Todos":
            query += " AND experiment_name = ?"
            params.append(selected_experiment)
        
        if selected_variable != "Todas":
            query += " AND variable_name = ?"
            params.append(selected_variable)
        
        if selected_location != "Todos":
            query += " AND location = ?"
            params.append(selected_location)
        
        query += " ORDER BY measurement_date DESC"
        
        # Executar query
        if params:
            data_df = pd.read_sql_query(query, conn, params=params)
        else:
            data_df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        if not data_df.empty:
            # Converter data para datetime
            data_df['measurement_date'] = pd.to_datetime(data_df['measurement_date'])
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribuição de valores por variável
                if selected_variable == "Todas":
                    fig_dist = px.box(
                        data_df,
                        x='variable_name',
                        y='value',
                        title="Distribuição de Valores por Variável",
                        color='variable_name'
                    )
                    fig_dist.update_layout(height=400, xaxis_tickangle=-45)
                    st.plotly_chart(fig_dist, use_container_width=True)
                else:
                    fig_hist = px.histogram(
                        data_df,
                        x='value',
                        title=f"Distribuição - {selected_variable}",
                        nbins=20
                    )
                    fig_hist.update_layout(height=400)
                    st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Série temporal
                if len(data_df) > 1:
                    if selected_variable != "Todas":
                        fig_time = px.scatter(
                            data_df,
                            x='measurement_date',
                            y='value',
                            color='location',
                            title=f"Evolução Temporal - {selected_variable}",
                            trendline="ols"
                        )
                    else:
                        fig_time = px.scatter(
                            data_df,
                            x='measurement_date',
                            y='value',
                            color='variable_name',
                            title="Evolução Temporal - Todas Variáveis"
                        )
                    
                    fig_time.update_layout(height=400)
                    st.plotly_chart(fig_time, use_container_width=True)
            
            # Gráfico de correlação (se múltiplas variáveis)
            if selected_variable == "Todas" and len(data_df['variable_name'].unique()) > 1:
                st.subheader("🔗 Matriz de Correlação")
                
                # Pivot para matriz de correlação
                pivot_df = data_df.pivot_table(
                    index=['experiment_name', 'measurement_date'],
                    columns='variable_name',
                    values='value',
                    aggfunc='mean'
                ).reset_index()
                
                # Calcular correlação
                numeric_cols = pivot_df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 1:
                    corr_matrix = pivot_df[numeric_cols].corr()
                    
                    fig_corr = px.imshow(
                        corr_matrix,
                        title="Matriz de Correlação entre Variáveis",
                        color_continuous_scale="RdBu",
                        aspect="auto"
                    )
                    fig_corr.update_layout(height=500)
                    st.plotly_chart(fig_corr, use_container_width=True)
            
            # Tabela de dados
            st.subheader("📋 Dados Detalhados")
            display_df = data_df[['experiment_name', 'variable_name', 'value', 'unit', 'measurement_date', 'location', 'notes']].copy()
            display_df.columns = ['Experimento', 'Variável', 'Valor', 'Unidade', 'Data', 'Local', 'Observações']
            display_df['Data'] = display_df['Data'].dt.strftime('%Y-%m-%d')
            display_df['Observações'] = display_df['Observações'].fillna('')
            
            st.dataframe(display_df, use_container_width=True)
            
            # Exportação
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Exportar Dados",
                data=csv,
                file_name=f"dados_experimentais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Nenhum dado encontrado com os filtros selecionados.")
    
    def import_csv_data(self):
        """Importação de dados CSV"""
        st.subheader("📤 Importar Dados CSV")
        
        # Upload de arquivo
        uploaded_file = st.file_uploader("Selecione o arquivo CSV", type=['csv'])
        
        if uploaded_file is not None:
            try:
                # Ler CSV
                df = pd.read_csv(uploaded_file)
                
                st.success(f"Arquivo carregado com sucesso! {len(df)} registros encontrados.")
                
                # Mostrar preview
                st.subheader("👀 Preview dos Dados")
                st.dataframe(df.head(10))
                
                # Mapeamento de colunas
                st.subheader("🔗 Mapeamento de Colunas")
                
                required_columns = ['experiment_name', 'variable_name', 'value', 'unit', 'measurement_date', 'location']
                
                col1, col2 = st.columns(2)
                
                column_mapping = {}
                
                with col1:
                    for req_col in required_columns[:3]:
                        column_mapping[req_col] = st.selectbox(
                            f"{req_col} *",
                            [""] + list(df.columns),
                            key=f"map_{req_col}"
                        )
                
                with col2:
                    for req_col in required_columns[3:]:
                        column_mapping[req_col] = st.selectbox(
                            f"{req_col}",
                            [""] + list(df.columns),
                            key=f"map_{req_col}"
                        )
                
                # Projeto associado
                conn = self.db.get_connection()
                projects_df = pd.read_sql_query("SELECT id, title FROM projects", conn)
                conn.close()
                
                project_options = ["Nenhum"] + [f"{row['title']} (ID: {row['id']})" for _, row in projects_df.iterrows()]
                associated_project = st.selectbox("Projeto Associado", project_options)
                
                if st.button("📥 Importar Dados"):
                    # Validar mapeamento
                    required_mapped = ['experiment_name', 'variable_name', 'value']
                    missing_required = [col for col in required_mapped if not column_mapping.get(col)]
                    
                    if missing_required:
                        st.error(f"Por favor, mapeie as colunas obrigatórias: {', '.join(missing_required)}")
                    else:
                        try:
                            # Preparar dados para inserção
                            project_id = None
                            if associated_project != "Nenhum":
                                project_id = int(associated_project.split("ID: ")[1].split(")")[0])
                            
                            conn = self.db.get_connection()
                            cursor = conn.cursor()
                            
                            success_count = 0
                            error_count = 0
                            
                            for _, row in df.iterrows():
                                try:
                                    # Extrair valores mapeados
                                    experiment_name = row[column_mapping['experiment_name']] if column_mapping.get('experiment_name') else 'Experimento_Importado'
                                    variable_name = row[column_mapping['variable_name']] if column_mapping.get('variable_name') else 'Variavel'
                                    value = float(row[column_mapping['value']]) if column_mapping.get('value') else 0.0
                                    unit = row[column_mapping['unit']] if column_mapping.get('unit') else ''
                                    measurement_date = row[column_mapping['measurement_date']] if column_mapping.get('measurement_date') else datetime.now().strftime('%Y-%m-%d')
                                    location = row[column_mapping['location']] if column_mapping.get('location') else 'Local_Nao_Especificado'
                                    
                                    cursor.execute('''
                                        INSERT INTO experimental_data (experiment_name, project_id, variable_name, value, unit, measurement_date, location, notes)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                    ''', (experiment_name, project_id, variable_name, value, unit, measurement_date, location, 'Importado via CSV'))
                                    
                                    success_count += 1
                                except Exception as e:
                                    error_count += 1
                                    continue
                            
                            conn.commit()
                            conn.close()
                            
                            st.success(f"Importação concluída! {success_count} registros importados com sucesso.")
                            if error_count > 0:
                                st.warning(f"{error_count} registros falharam na importação.")
                            
                            st.rerun()
                        
                        except Exception as e:
                            st.error(f"Erro durante a importação: {str(e)}")
            
            except Exception as e:
                st.error(f"Erro ao ler arquivo CSV: {str(e)}")
        
        # Template CSV
        st.subheader("📋 Template CSV")
        st.info("Use este template como referência para estruturar seus dados:")
        
        template_data = {
            'experiment_name': ['Experimento_1', 'Experimento_1', 'Experimento_2'],
            'variable_name': ['Produtividade', 'Altura', 'Produtividade'],
            'value': [45.2, 120.5, 38.7],
            'unit': ['kg/ha', 'cm', 'kg/ha'],
            'measurement_date': ['2024-01-15', '2024-01-15', '2024-01-20'],
            'location': ['Campo A', 'Campo A', 'Campo B']
        }
        
        template_df = pd.DataFrame(template_data)
        st.dataframe(template_df)
        
        # Download template
        csv_template = template_df.to_csv(index=False)
        st.download_button(
            label="📥 Baixar Template CSV",
            data=csv_template,
            file_name="template_dados_experimentais.csv",
            mime="text/csv"
        )
    
    def statistical_analysis(self):
        """Análise estatística dos dados"""
        st.subheader("📈 Análise Estatística")
        
        conn = self.db.get_connection()
        
        # Seleção de dados para análise
        col1, col2 = st.columns(2)
        
        with col1:
            experiments = pd.read_sql_query("SELECT DISTINCT experiment_name FROM experimental_data", conn)['experiment_name'].tolist()
            selected_experiment = st.selectbox("Experimento para Análise", experiments)
        
        with col2:
            variables = pd.read_sql_query(f"SELECT DISTINCT variable_name FROM experimental_data WHERE experiment_name = '{selected_experiment}'", conn)['variable_name'].tolist()
            selected_variable = st.selectbox("Variável para Análise", variables)
        
        if selected_experiment and selected_variable:
            # Buscar dados
            data_df = pd.read_sql_query(f'''
                SELECT * FROM experimental_data 
                WHERE experiment_name = '{selected_experiment}' AND variable_name = '{selected_variable}'
                ORDER BY measurement_date
            ''', conn)
            
            if not data_df.empty:
                values = data_df['value'].values
                
                # Estatísticas descritivas
                st.subheader("📊 Estatísticas Descritivas")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                col1.metric("Média", f"{np.mean(values):.2f}")
                col2.metric("Mediana", f"{np.median(values):.2f}")
                col3.metric("Desvio Padrão", f"{np.std(values):.2f}")
                col4.metric("Mínimo", f"{np.min(values):.2f}")
                col5.metric("Máximo", f"{np.max(values):.2f}")
                
                # Testes estatísticos
                st.subheader("🧮 Testes Estatísticos")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Teste de normalidade
                    if len(values) >= 3:
                        shapiro_stat, shapiro_p = stats.shapiro(values)
                        st.write("**Teste de Normalidade (Shapiro-Wilk):**")
                        st.write(f"Estatística: {shapiro_stat:.4f}")
                        st.write(f"P-valor: {shapiro_p:.4f}")
                        
                        if shapiro_p > 0.05:
                            st.success("✅ Dados seguem distribuição normal (p > 0.05)")
                        else:
                            st.warning("⚠️ Dados não seguem distribuição normal (p ≤ 0.05)")
                
                with col2:
                    # Outliers (IQR method)
                    Q1 = np.percentile(values, 25)
                    Q3 = np.percentile(values, 75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outliers = values[(values < lower_bound) | (values > upper_bound)]
                    
                    st.write("**Detecção de Outliers (Método IQR):**")
                    st.write(f"Limite inferior: {lower_bound:.2f}")
                    st.write(f"Limite superior: {upper_bound:.2f}")
                    st.write(f"Outliers encontrados: {len(outliers)}")
                    
                    if len(outliers) > 0:
                        st.warning(f"⚠️ {len(outliers)} outliers detectados")
                    else:
                        st.success("✅ Nenhum outlier detectado")
                
                # Gráficos estatísticos
                col1, col2 = st.columns(2)
                
                with col1:
                    # Histograma com curva normal
                    fig_hist = go.Figure()
                    
                    fig_hist.add_trace(go.Histogram(
                        x=values,
                        nbinsx=20,
                        name="Dados",
                        opacity=0.7
                    ))
                    
                    # Curva normal teórica
                    x_norm = np.linspace(values.min(), values.max(), 100)
                    y_norm = stats.norm.pdf(x_norm, np.mean(values), np.std(values))
                    y_norm = y_norm * len(values) * (values.max() - values.min()) / 20  # Escalar para o histograma
                    
                    fig_hist.add_trace(go.Scatter(
                        x=x_norm,
                        y=y_norm,
                        mode='lines',
                        name='Normal Teórica',
                        line=dict(color='red', width=2)
                    ))
                    
                    fig_hist.update_layout(
                        title="Distribuição dos Dados vs Normal Teórica",
                        xaxis_title="Valor",
                        yaxis_title="Frequência",
                        height=400
                    )
                    
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    # Box plot
                    fig_box = go.Figure()
                    fig_box.add_trace(go.Box(
                        y=values,
                        name=selected_variable,
                        boxpoints='outliers'
                    ))
                    
                    fig_box.update_layout(
                        title="Box Plot - Detecção de Outliers",
                        yaxis_title="Valor",
                        height=400
                    )
                    
                    st.plotly_chart(fig_box, use_container_width=True)
                
                # Análise de tendência temporal
                if len(data_df) > 2:
                    st.subheader("📈 Análise de Tendência Temporal")
                    
                    data_df['measurement_date'] = pd.to_datetime(data_df['measurement_date'])
                    data_df['days_from_start'] = (data_df['measurement_date'] - data_df['measurement_date'].min()).dt.days
                    
                    # Regressão linear
                    slope, intercept, r_value, p_value, std_err = stats.linregress(data_df['days_from_start'], data_df['value'])
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Coeficiente Angular", f"{slope:.4f}")
                    col2.metric("R²", f"{r_value**2:.4f}")
                    col3.metric("P-valor", f"{p_value:.4f}")
                    
                    if p_value < 0.05:
                        if slope > 0:
                            st.success("✅ Tendência crescente significativa")
                        else:
                            st.warning("📉 Tendência decrescente significativa")
                    else:
                        st.info("ℹ️ Não há tendência temporal significativa")
            else:
                st.info("Nenhum dado encontrado para a combinação selecionada.")
        
        conn.close()
    
    def data_exploration(self):
        """Exploração interativa dos dados"""
        st.subheader("🔍 Exploração de Dados")
        
        conn = self.db.get_connection()
        
        # Análise multivariada
        st.write("**Análise de Múltiplas Variáveis**")
        
        experiments = pd.read_sql_query("SELECT DISTINCT experiment_name FROM experimental_data", conn)['experiment_name'].tolist()
        selected_experiments = st.multiselect("Selecione Experimentos", experiments, default=experiments[:3] if len(experiments) >= 3 else experiments)
        
        if selected_experiments:
            # Buscar dados dos experimentos selecionados
            exp_list = "', '".join(selected_experiments)
            data_df = pd.read_sql_query(f'''
                SELECT * FROM experimental_data 
                WHERE experiment_name IN ('{exp_list}')
                ORDER BY experiment_name, measurement_date
            ''', conn)
            
            if not data_df.empty:
                # Pivot table para análise
                pivot_df = data_df.pivot_table(
                    index=['experiment_name', 'measurement_date'],
                    columns='variable_name',
                    values='value',
                    aggfunc='mean'
                ).reset_index()
                
                # Gráfico de dispersão multivariado
                numeric_cols = pivot_df.select_dtypes(include=[np.number]).columns.tolist()
                
                if len(numeric_cols) >= 2:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        x_var = st.selectbox("Variável X", numeric_cols)
                    with col2:
                        y_var = st.selectbox("Variável Y", [col for col in numeric_cols if col != x_var])
                    
                    if x_var and y_var:
                        fig_scatter = px.scatter(
                            pivot_df,
                            x=x_var,
                            y=y_var,
                            color='experiment_name',
                            title=f"Relação entre {x_var} e {y_var}",
                            trendline="ols"
                        )
                        fig_scatter.update_layout(height=500)
                        st.plotly_chart(fig_scatter, use_container_width=True)
                        
                        # Correlação entre as variáveis
                        correlation = pivot_df[x_var].corr(pivot_df[y_var])
                        st.metric("Correlação", f"{correlation:.3f}")
                
                # Análise de agrupamento (clustering simples)
                if len(numeric_cols) >= 2:
                    st.subheader("🎯 Análise de Agrupamento")
                    
                    from sklearn.cluster import KMeans
                    from sklearn.preprocessing import StandardScaler
                    
                    # Preparar dados para clustering
                    cluster_data = pivot_df[numeric_cols].dropna()
                    
                    if len(cluster_data) > 3:
                        scaler = StandardScaler()
                        scaled_data = scaler.fit_transform(cluster_data)
                        
                        n_clusters = st.slider("Número de Clusters", 2, min(8, len(cluster_data)-1), 3)
                        
                        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                        clusters = kmeans.fit_predict(scaled_data)
                        
                        # Adicionar clusters ao dataframe
                        cluster_df = cluster_data.copy()
                        cluster_df['Cluster'] = clusters
                        
                        # Visualizar clusters
                        if len(numeric_cols) >= 2:
                            fig_cluster = px.scatter(
                                cluster_df,
                                x=numeric_cols[0],
                                y=numeric_cols[1],
                                color='Cluster',
                                title=f"Agrupamento - {n_clusters} Clusters"
                            )
                            fig_cluster.update_layout(height=500)
                            st.plotly_chart(fig_cluster, use_container_width=True)
        
        conn.close()
    
    def generate_reports(self):
        """Geração de relatórios"""
        st.subheader("📋 Relatórios de Dados Experimentais")
        
        conn = self.db.get_connection()
        
        # Relatório resumo
        summary_data = pd.read_sql_query('''
            SELECT 
                experiment_name,
                COUNT(*) as total_measurements,
                COUNT(DISTINCT variable_name) as variables_count,
                COUNT(DISTINCT location) as locations_count,
                MIN(measurement_date) as first_measurement,
                MAX(measurement_date) as last_measurement
            FROM experimental_data
            GROUP BY experiment_name
            ORDER BY total_measurements DESC
        ''', conn)
        
        if not summary_data.empty:
            st.subheader("📊 Resumo por Experimento")
            summary_data.columns = ['Experimento', 'Total Medições', 'Variáveis', 'Locais', 'Primeira Medição', 'Última Medição']
            st.dataframe(summary_data, use_container_width=True)
            
            # Exportar resumo
            csv_summary = summary_data.to_csv(index=False)
            st.download_button(
                label="📥 Exportar Resumo",
                data=csv_summary,
                file_name=f"resumo_experimentos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # Relatório detalhado por variável
        variable_stats = pd.read_sql_query('''
            SELECT 
                variable_name,
                unit,
                COUNT(*) as measurements_count,
                AVG(value) as mean_value,
                MIN(value) as min_value,
                MAX(value) as max_value,
                (MAX(value) - MIN(value)) as range_value
            FROM experimental_data
            GROUP BY variable_name, unit
            ORDER BY measurements_count DESC
        ''', conn)
        
        if not variable_stats.empty:
            st.subheader("📈 Estatísticas por Variável")
            variable_stats.columns = ['Variável', 'Unidade', 'Medições', 'Média', 'Mínimo', 'Máximo', 'Amplitude']
            
            # Formatar números
            for col in ['Média', 'Mínimo', 'Máximo', 'Amplitude']:
                variable_stats[col] = variable_stats[col].round(2)
            
            st.dataframe(variable_stats, use_container_width=True)
        
        conn.close()
