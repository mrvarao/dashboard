
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import DatabaseManager

class AlertsManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def show_alerts_dashboard(self):
        """Dashboard de alertas e notificações"""
        st.title("🔔 Alertas e Notificações")
        
        # Verificar alertas do usuário atual
        user_id = st.session_state.user['id']
        
        conn = self.db.get_connection()
        
        # Métricas de alertas
        col1, col2, col3, col4 = st.columns(4)
        
        # Total de alertas
        total_alerts = pd.read_sql_query(f"SELECT COUNT(*) as count FROM alerts WHERE user_id = {user_id}", conn).iloc[0]['count']
        col1.metric("Total Alertas", total_alerts)
        
        # Alertas não lidos
        unread_alerts = pd.read_sql_query(f"SELECT COUNT(*) as count FROM alerts WHERE user_id = {user_id} AND read = 0", conn).iloc[0]['count']
        col2.metric("Não Lidos", unread_alerts)
        
        # Alertas de alta prioridade
        high_priority = pd.read_sql_query(f"SELECT COUNT(*) as count FROM alerts WHERE user_id = {user_id} AND priority = 'alta' AND read = 0", conn).iloc[0]['count']
        col3.metric("Alta Prioridade", high_priority)
        
        # Alertas de hoje
        today_alerts = pd.read_sql_query(f"SELECT COUNT(*) as count FROM alerts WHERE user_id = {user_id} AND date(created_at) = date('now')", conn).iloc[0]['count']
        col4.metric("Hoje", today_alerts)
        
        st.markdown("---")
        
        # Tabs para diferentes tipos de alertas
        tab1, tab2, tab3, tab4 = st.tabs(["🔔 Meus Alertas", "⏰ Prazos", "📋 Tarefas", "⚙️ Configurações"])
        
        with tab1:
            self.show_user_alerts(user_id)
        
        with tab2:
            self.show_deadline_alerts()
        
        with tab3:
            self.show_task_alerts()
        
        with tab4:
            self.show_alert_settings()
        
        conn.close()
    
    def show_user_alerts(self, user_id):
        """Exibe alertas do usuário"""
        st.subheader("🔔 Meus Alertas")
        
        conn = self.db.get_connection()
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_status = st.selectbox("Status", ["Todos", "Não Lidos", "Lidos"])
        
        with col2:
            filter_priority = st.selectbox("Prioridade", ["Todas", "alta", "media", "baixa"])
        
        with col3:
            filter_type = st.selectbox("Tipo", ["Todos", "prazo", "tarefa", "notificacao"])
        
        # Construir query com filtros
        query = f"SELECT * FROM alerts WHERE user_id = {user_id}"
        
        if filter_status == "Não Lidos":
            query += " AND read = 0"
        elif filter_status == "Lidos":
            query += " AND read = 1"
        
        if filter_priority != "Todas":
            query += f" AND priority = '{filter_priority}'"
        
        if filter_type != "Todos":
            query += f" AND type = '{filter_type}'"
        
        query += " ORDER BY created_at DESC"
        
        alerts_df = pd.read_sql_query(query, conn)
        
        if not alerts_df.empty:
            # Exibir alertas
            for _, alert in alerts_df.iterrows():
                # Definir cor baseada na prioridade
                if alert['priority'] == 'alta':
                    priority_color = "🔴"
                elif alert['priority'] == 'media':
                    priority_color = "🟡"
                else:
                    priority_color = "🟢"
                
                # Definir ícone baseado no tipo
                if alert['type'] == 'prazo':
                    type_icon = "⏰"
                elif alert['type'] == 'tarefa':
                    type_icon = "📋"
                else:
                    type_icon = "📢"
                
                # Status de leitura
                read_status = "✅" if alert['read'] else "🔵"
                
                # Container do alerta
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.write(f"{read_status} {type_icon} {priority_color} **{alert['title']}**")
                        st.write(alert['message'])
                        st.caption(f"📅 {alert['created_at']}")
                    
                    with col2:
                        if not alert['read']:
                            if st.button("Marcar como Lido", key=f"read_{alert['id']}"):
                                cursor = conn.cursor()
                                cursor.execute("UPDATE alerts SET read = 1 WHERE id = ?", (alert['id'],))
                                conn.commit()
                                st.rerun()
                        
                        if st.button("🗑️ Excluir", key=f"delete_{alert['id']}"):
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM alerts WHERE id = ?", (alert['id'],))
                            conn.commit()
                            st.rerun()
                
                st.markdown("---")
            
            # Ações em lote
            st.subheader("⚡ Ações em Lote")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Marcar Todos como Lidos"):
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE alerts SET read = 1 WHERE user_id = {user_id} AND read = 0")
                    conn.commit()
                    st.success("Todos os alertas foram marcados como lidos!")
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Excluir Alertas Lidos"):
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM alerts WHERE user_id = {user_id} AND read = 1")
                    conn.commit()
                    st.success("Alertas lidos foram excluídos!")
                    st.rerun()
        else:
            st.info("Nenhum alerta encontrado com os filtros selecionados.")
        
        conn.close()
    
    def show_deadline_alerts(self):
        """Alertas de prazos"""
        st.subheader("⏰ Monitoramento de Prazos")
        
        conn = self.db.get_connection()
        
        # Projetos próximos do prazo
        upcoming_deadlines = pd.read_sql_query('''
            SELECT p.*, u.name as responsible_name,
                   julianday(p.end_date) - julianday('now') as days_remaining
            FROM projects p
            LEFT JOIN users u ON p.responsible_id = u.id
            WHERE p.status IN ('planejamento', 'em_andamento')
            AND p.end_date IS NOT NULL
            AND julianday(p.end_date) - julianday('now') <= 30
            ORDER BY days_remaining ASC
        ''', conn)
        
        if not upcoming_deadlines.empty:
            st.warning(f"⚠️ {len(upcoming_deadlines)} projetos com prazo próximo (30 dias)")
            
            for _, project in upcoming_deadlines.iterrows():
                days_remaining = int(project['days_remaining'])
                
                if days_remaining < 0:
                    status_color = "🔴"
                    status_text = f"Atrasado há {abs(days_remaining)} dias"
                elif days_remaining <= 7:
                    status_color = "🟠"
                    status_text = f"{days_remaining} dias restantes"
                else:
                    status_color = "🟡"
                    status_text = f"{days_remaining} dias restantes"
                
                with st.expander(f"{status_color} {project['title']} - {status_text}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Responsável:** {project['responsible_name']}")
                        st.write(f"**Área:** {project['area']}")
                        st.write(f"**Status:** {project['status']}")
                    
                    with col2:
                        st.write(f"**Data de Fim:** {project['end_date']}")
                        st.write(f"**Orçamento:** R$ {project['budget']:,.2f}")
                        st.write(f"**Gasto:** R$ {project['spent_budget']:,.2f}")
                    
                    # Botão para criar alerta
                    if st.button(f"🔔 Criar Alerta", key=f"alert_{project['id']}"):
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO alerts (user_id, title, message, type, priority)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (
                            project['responsible_id'],
                            f"Prazo do projeto: {project['title']}",
                            f"O projeto '{project['title']}' tem prazo até {project['end_date']} ({status_text})",
                            'prazo',
                            'alta' if days_remaining <= 7 else 'media'
                        ))
                        conn.commit()
                        st.success("Alerta criado com sucesso!")
        else:
            st.success("✅ Nenhum projeto com prazo próximo!")
        
        # Eventos próximos
        st.subheader("📅 Eventos Próximos")
        
        upcoming_events = pd.read_sql_query('''
            SELECT e.*, u.name as organizer_name,
                   julianday(e.start_date) - julianday('now') as days_until_event
            FROM events e
            LEFT JOIN users u ON e.organizer_id = u.id
            WHERE julianday(e.start_date) - julianday('now') BETWEEN 0 AND 7
            ORDER BY e.start_date ASC
        ''', conn)
        
        if not upcoming_events.empty:
            st.info(f"📅 {len(upcoming_events)} eventos nos próximos 7 dias")
            
            for _, event in upcoming_events.iterrows():
                days_until = int(event['days_until_event'])
                
                if days_until == 0:
                    time_text = "Hoje"
                elif days_until == 1:
                    time_text = "Amanhã"
                else:
                    time_text = f"Em {days_until} dias"
                
                st.write(f"🎯 **{event['title']}** - {time_text}")
                st.write(f"   📍 {event['location']} | 👤 {event['organizer_name']}")
        else:
            st.info("Nenhum evento próximo.")
        
        conn.close()
    
    def show_task_alerts(self):
        """Alertas de tarefas"""
        st.subheader("📋 Tarefas Pendentes")
        
        # Simulação de tarefas baseadas em dados do sistema
        conn = self.db.get_connection()
        
        # Relatórios pendentes (projetos sem publicações recentes)
        pending_reports = pd.read_sql_query('''
            SELECT p.*, u.name as responsible_name
            FROM projects p
            LEFT JOIN users u ON p.responsible_id = u.id
            LEFT JOIN publications pub ON p.id = pub.project_id
            WHERE p.status = 'em_andamento'
            AND (pub.id IS NULL OR pub.created_at < date('now', '-90 days'))
            GROUP BY p.id
        ''', conn)
        
        if not pending_reports.empty:
            st.warning(f"📝 {len(pending_reports)} projetos sem relatórios/publicações recentes")
            
            for _, project in pending_reports.iterrows():
                with st.expander(f"📝 Relatório pendente: {project['title']}"):
                    st.write(f"**Responsável:** {project['responsible_name']}")
                    st.write(f"**Área:** {project['area']}")
                    st.write("**Ação:** Projeto em andamento há mais de 90 dias sem publicações")
                    
                    if st.button(f"🔔 Notificar Responsável", key=f"notify_{project['id']}"):
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO alerts (user_id, title, message, type, priority)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (
                            project['responsible_id'],
                            f"Relatório pendente: {project['title']}",
                            f"O projeto '{project['title']}' está há mais de 90 dias sem publicações. Considere enviar um relatório de progresso.",
                            'tarefa',
                            'media'
                        ))
                        conn.commit()
                        st.success("Notificação enviada!")
        
        # Dados experimentais não analisados
        unanalyzed_data = pd.read_sql_query('''
            SELECT experiment_name, COUNT(*) as data_count, MAX(created_at) as last_entry
            FROM experimental_data
            WHERE created_at > date('now', '-30 days')
            GROUP BY experiment_name
            HAVING data_count > 10
        ''', conn)
        
        if not unanalyzed_data.empty:
            st.info(f"🧪 {len(unanalyzed_data)} experimentos com dados recentes para análise")
            
            for _, exp in unanalyzed_data.iterrows():
                st.write(f"🔬 **{exp['experiment_name']}** - {exp['data_count']} registros (último: {exp['last_entry']})")
        
        conn.close()
    
    def show_alert_settings(self):
        """Configurações de alertas"""
        st.subheader("⚙️ Configurações de Alertas")
        
        # Preferências de notificação
        st.write("**Preferências de Notificação:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            email_alerts = st.checkbox("Alertas por Email", value=True)
            deadline_alerts = st.checkbox("Alertas de Prazo", value=True)
            task_alerts = st.checkbox("Alertas de Tarefas", value=True)
        
        with col2:
            high_priority_only = st.checkbox("Apenas Alta Prioridade", value=False)
            daily_summary = st.checkbox("Resumo Diário", value=False)
            weekly_report = st.checkbox("Relatório Semanal", value=True)
        
        # Configurações de prazo
        st.write("**Configurações de Prazo:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            deadline_warning_days = st.number_input("Avisar com quantos dias de antecedência", min_value=1, max_value=90, value=30)
        
        with col2:
            critical_deadline_days = st.number_input("Prazo crítico (dias)", min_value=1, max_value=30, value=7)
        
        # Salvar configurações
        if st.button("💾 Salvar Configurações"):
            st.success("Configurações salvas com sucesso!")
            st.info("Funcionalidade de configurações pode ser expandida para persistir no banco de dados.")
        
        # Criar alerta manual
        st.markdown("---")
        st.subheader("➕ Criar Alerta Manual")
        
        with st.form("manual_alert_form"):
            alert_title = st.text_input("Título do Alerta")
            alert_message = st.text_area("Mensagem")
            
            col1, col2 = st.columns(2)
            
            with col1:
                alert_type = st.selectbox("Tipo", ["notificacao", "prazo", "tarefa"])
            
            with col2:
                alert_priority = st.selectbox("Prioridade", ["baixa", "media", "alta"])
            
            # Destinatário
            conn = self.db.get_connection()
            users_df = pd.read_sql_query("SELECT id, name FROM users", conn)
            conn.close()
            
            recipient_options = ["Eu mesmo"] + [f"{row['name']} (ID: {row['id']})" for _, row in users_df.iterrows()]
            recipient = st.selectbox("Destinatário", recipient_options)
            
            submitted = st.form_submit_button("🔔 Criar Alerta")
            
            if submitted:
                if alert_title and alert_message:
                    try:
                        if recipient == "Eu mesmo":
                            recipient_id = st.session_state.user['id']
                        else:
                            recipient_id = int(recipient.split("ID: ")[1].split(")")[0])
                        
                        conn = self.db.get_connection()
                        cursor = conn.cursor()
                        
                        cursor.execute('''
                            INSERT INTO alerts (user_id, title, message, type, priority)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (recipient_id, alert_title, alert_message, alert_type, alert_priority))
                        
                        conn.commit()
                        conn.close()
                        
                        st.success("Alerta criado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao criar alerta: {str(e)}")
                else:
                    st.error("Por favor, preencha título e mensagem!")
    
    def check_automatic_alerts(self):
        """Verifica e cria alertas automáticos"""
        conn = self.db.get_connection()
        
        # Verificar projetos próximos do prazo
        upcoming_projects = pd.read_sql_query('''
            SELECT p.*, u.name as responsible_name
            FROM projects p
            LEFT JOIN users u ON p.responsible_id = u.id
            WHERE p.status IN ('planejamento', 'em_andamento')
            AND p.end_date IS NOT NULL
            AND julianday(p.end_date) - julianday('now') <= 7
            AND julianday(p.end_date) - julianday('now') > 0
        ''', conn)
        
        cursor = conn.cursor()
        
        for _, project in upcoming_projects.iterrows():
            # Verificar se já existe alerta para este projeto
            existing_alert = pd.read_sql_query(f'''
                SELECT id FROM alerts 
                WHERE user_id = {project['responsible_id']} 
                AND title LIKE '%{project['title']}%' 
                AND created_at > date('now', '-7 days')
            ''', conn)
            
            if existing_alert.empty:
                days_remaining = int((pd.to_datetime(project['end_date']) - pd.Timestamp.now()).days)
                
                cursor.execute('''
                    INSERT INTO alerts (user_id, title, message, type, priority)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    project['responsible_id'],
                    f"Prazo próximo: {project['title']}",
                    f"O projeto '{project['title']}' tem prazo até {project['end_date']} ({days_remaining} dias restantes)",
                    'prazo',
                    'alta'
                ))
        
        conn.commit()
        conn.close()
