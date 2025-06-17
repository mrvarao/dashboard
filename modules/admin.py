
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from database import DatabaseManager

class AdminManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def show_admin_dashboard(self):
        """Dashboard administrativo"""
        st.title("👥 Gestão Administrativa")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        conn = self.db.get_connection()
        
        # Total de funcionários
        total_employees = pd.read_sql_query("SELECT COUNT(*) as count FROM employees WHERE active = 1", conn).iloc[0]['count']
        col1.metric("Funcionários Ativos", total_employees)
        
        # Total de usuários
        total_users = pd.read_sql_query("SELECT COUNT(*) as count FROM users", conn).iloc[0]['count']
        col2.metric("Usuários Sistema", total_users)
        
        # Eventos programados
        upcoming_events = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM events WHERE start_date > datetime('now')", conn
        ).iloc[0]['count']
        col3.metric("Eventos Futuros", upcoming_events)
        
        # Treinamentos realizados
        completed_trainings = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM events WHERE type = 'treinamento' AND end_date < datetime('now')", conn
        ).iloc[0]['count']
        col4.metric("Treinamentos Realizados", completed_trainings)
        
        conn.close()
        
        st.markdown("---")
        
        # Tabs para diferentes seções
        tab1, tab2, tab3, tab4 = st.tabs(["👥 Funcionários", "📅 Eventos", "🏢 Organograma", "📊 Relatórios"])
        
        with tab1:
            self.show_employees_section()
        
        with tab2:
            self.show_events_section()
        
        with tab3:
            self.show_organogram_section()
        
        with tab4:
            self.show_admin_reports()
    
    def show_employees_section(self):
        """Seção de gestão de funcionários"""
        st.subheader("Gestão de Funcionários")
        
        # Formulário para adicionar funcionário
        with st.expander("➕ Adicionar Novo Funcionário"):
            with st.form("new_employee_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Nome Completo*")
                    position = st.text_input("Cargo*")
                    department = st.selectbox("Departamento*", [
                        "Direção", "Pesquisa", "Agricultura", "Biotecnologia", 
                        "Sustentabilidade", "Recursos Naturais", "Administrativo", "TI"
                    ])
                
                with col2:
                    email = st.text_input("Email")
                    phone = st.text_input("Telefone")
                    hire_date = st.date_input("Data de Contratação", value=date.today())
                
                # Supervisor
                conn = self.db.get_connection()
                supervisors_df = pd.read_sql_query("SELECT id, name FROM employees WHERE active = 1", conn)
                conn.close()
                
                supervisor_options = ["Nenhum"] + [f"{row['name']} (ID: {row['id']})" for _, row in supervisors_df.iterrows()]
                supervisor = st.selectbox("Supervisor", supervisor_options)
                
                submitted = st.form_submit_button("Adicionar Funcionário")
                
                if submitted:
                    if name and position and department:
                        try:
                            supervisor_id = None
                            if supervisor != "Nenhum":
                                supervisor_id = int(supervisor.split("ID: ")[1].split(")")[0])
                            
                            conn = self.db.get_connection()
                            cursor = conn.cursor()
                            
                            cursor.execute('''
                                INSERT INTO employees (name, position, department, email, phone, hire_date, supervisor_id)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (name, position, department, email, phone, hire_date, supervisor_id))
                            
                            conn.commit()
                            conn.close()
                            
                            st.success("Funcionário adicionado com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao adicionar funcionário: {str(e)}")
                    else:
                        st.error("Por favor, preencha todos os campos obrigatórios!")
        
        # Lista de funcionários
        conn = self.db.get_connection()
        employees_df = pd.read_sql_query('''
            SELECT e1.*, e2.name as supervisor_name 
            FROM employees e1 
            LEFT JOIN employees e2 ON e1.supervisor_id = e2.id 
            WHERE e1.active = 1
            ORDER BY e1.department, e1.name
        ''', conn)
        conn.close()
        
        if not employees_df.empty:
            # Gráfico por departamento
            dept_counts = employees_df['department'].value_counts()
            fig_dept = px.bar(
                x=dept_counts.index,
                y=dept_counts.values,
                title="Funcionários por Departamento",
                color=dept_counts.values,
                color_continuous_scale="blues"
            )
            fig_dept.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_dept, use_container_width=True)
            
            # Tabela de funcionários
            display_df = employees_df[['name', 'position', 'department', 'email', 'phone', 'hire_date', 'supervisor_name']].copy()
            display_df.columns = ['Nome', 'Cargo', 'Departamento', 'Email', 'Telefone', 'Contratação', 'Supervisor']
            display_df['Supervisor'] = display_df['Supervisor'].fillna('N/A')
            
            st.dataframe(display_df, use_container_width=True)
            
            # Exportar
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Exportar Funcionários",
                data=csv,
                file_name=f"funcionarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Nenhum funcionário cadastrado.")
    
    def show_events_section(self):
        """Seção de gestão de eventos"""
        st.subheader("Gestão de Eventos e Treinamentos")
        
        # Formulário para adicionar evento
        with st.expander("➕ Adicionar Novo Evento"):
            with st.form("new_event_form"):
                title = st.text_input("Título do Evento*")
                description = st.text_area("Descrição")
                
                col1, col2 = st.columns(2)
                with col1:
                    event_type = st.selectbox("Tipo*", [
                        "treinamento", "workshop", "seminario", "conferencia"
                    ])
                    location = st.text_input("Local")
                
                with col2:
                    max_participants = st.number_input("Máximo de Participantes", min_value=1, value=50)
                    
                    # Organizador
                    conn = self.db.get_connection()
                    users_df = pd.read_sql_query("SELECT id, name FROM users", conn)
                    conn.close()
                    
                    organizer_options = [f"{row['name']} (ID: {row['id']})" for _, row in users_df.iterrows()]
                    organizer = st.selectbox("Organizador*", organizer_options)
                
                col3, col4 = st.columns(2)
                with col3:
                    start_date = st.date_input("Data de Início")
                    start_time = st.time_input("Hora de Início")
                
                with col4:
                    end_date = st.date_input("Data de Fim")
                    end_time = st.time_input("Hora de Fim")
                
                submitted = st.form_submit_button("Criar Evento")
                
                if submitted:
                    if title and event_type and organizer:
                        try:
                            organizer_id = int(organizer.split("ID: ")[1].split(")")[0])
                            
                            start_datetime = datetime.combine(start_date, start_time)
                            end_datetime = datetime.combine(end_date, end_time)
                            
                            conn = self.db.get_connection()
                            cursor = conn.cursor()
                            
                            cursor.execute('''
                                INSERT INTO events (title, description, type, start_date, end_date, location, max_participants, organizer_id)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (title, description, event_type, start_datetime, end_datetime, location, max_participants, organizer_id))
                            
                            conn.commit()
                            conn.close()
                            
                            st.success("Evento criado com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao criar evento: {str(e)}")
                    else:
                        st.error("Por favor, preencha todos os campos obrigatórios!")
        
        # Lista de eventos
        conn = self.db.get_connection()
        events_df = pd.read_sql_query('''
            SELECT e.*, u.name as organizer_name 
            FROM events e 
            LEFT JOIN users u ON e.organizer_id = u.id 
            ORDER BY e.start_date DESC
        ''', conn)
        conn.close()
        
        if not events_df.empty:
            # Gráfico de eventos por tipo
            type_counts = events_df['type'].value_counts()
            fig_type = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                title="Eventos por Tipo",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_type, use_container_width=True)
            
            # Tabela de eventos
            display_df = events_df[['title', 'type', 'start_date', 'end_date', 'location', 'max_participants', 'organizer_name']].copy()
            display_df.columns = ['Título', 'Tipo', 'Início', 'Fim', 'Local', 'Max. Participantes', 'Organizador']
            
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("Nenhum evento cadastrado.")
    
    def show_organogram_section(self):
        """Seção do organograma"""
        st.subheader("Organograma")
        
        conn = self.db.get_connection()
        employees_df = pd.read_sql_query('''
            SELECT e1.id, e1.name, e1.position, e1.department, e1.supervisor_id, e2.name as supervisor_name
            FROM employees e1 
            LEFT JOIN employees e2 ON e1.supervisor_id = e2.id 
            WHERE e1.active = 1
            ORDER BY e1.department, e1.position
        ''', conn)
        conn.close()
        
        if not employees_df.empty:
            # Organizar por departamento
            departments = employees_df['department'].unique()
            
            for dept in departments:
                st.subheader(f"📁 {dept}")
                dept_employees = employees_df[employees_df['department'] == dept]
                
                # Mostrar hierarquia
                for _, emp in dept_employees.iterrows():
                    if pd.isna(emp['supervisor_id']):
                        st.write(f"👑 **{emp['name']}** - {emp['position']}")
                    else:
                        st.write(f"   └── {emp['name']} - {emp['position']} (Supervisor: {emp['supervisor_name']})")
                
                st.markdown("---")
        else:
            st.info("Nenhum funcionário cadastrado para exibir organograma.")
    
    def show_admin_reports(self):
        """Relatórios administrativos"""
        st.subheader("Relatórios Administrativos")
        
        conn = self.db.get_connection()
        
        # Relatório de funcionários por departamento
        dept_report = pd.read_sql_query('''
            SELECT department, COUNT(*) as total_funcionarios,
                   AVG(julianday('now') - julianday(hire_date)) as tempo_medio_empresa
            FROM employees 
            WHERE active = 1 
            GROUP BY department
        ''', conn)
        
        if not dept_report.empty:
            st.subheader("📊 Funcionários por Departamento")
            dept_report['tempo_medio_empresa'] = dept_report['tempo_medio_empresa'].round(0).astype(int)
            dept_report.columns = ['Departamento', 'Total Funcionários', 'Tempo Médio (dias)']
            st.dataframe(dept_report, use_container_width=True)
        
        # Relatório de eventos
        events_report = pd.read_sql_query('''
            SELECT type, COUNT(*) as total_eventos,
                   AVG(max_participants) as media_participantes
            FROM events 
            GROUP BY type
        ''', conn)
        
        if not events_report.empty:
            st.subheader("📅 Relatório de Eventos")
            events_report['media_participantes'] = events_report['media_participantes'].round(0).astype(int)
            events_report.columns = ['Tipo', 'Total Eventos', 'Média Participantes']
            st.dataframe(events_report, use_container_width=True)
        
        conn.close()
