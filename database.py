
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random
import hashlib

class DatabaseManager:
    def __init__(self, db_path="embrapa_dashboard.db"):
        self.db_path = db_path
        self.init_database()
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inicializa o banco de dados com todas as tabelas necessárias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                role TEXT NOT NULL CHECK (role IN ('administrador', 'pesquisador', 'gestor')),
                department TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de projetos PD&I
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                area TEXT NOT NULL,
                responsible_id INTEGER,
                status TEXT NOT NULL CHECK (status IN ('planejamento', 'em_andamento', 'concluido', 'cancelado')),
                start_date DATE,
                end_date DATE,
                budget REAL,
                spent_budget REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (responsible_id) REFERENCES users (id)
            )
        ''')
        
        # Tabela de funcionários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                department TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                hire_date DATE,
                supervisor_id INTEGER,
                active BOOLEAN DEFAULT 1,
                FOREIGN KEY (supervisor_id) REFERENCES employees (id)
            )
        ''')
        
        # Tabela de publicações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS publications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                authors TEXT NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('artigo', 'livro', 'capitulo', 'relatorio', 'tese')),
                journal TEXT,
                year INTEGER,
                doi TEXT,
                file_path TEXT,
                project_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        
        # Tabela de dados experimentais
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experimental_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_name TEXT NOT NULL,
                project_id INTEGER,
                variable_name TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT,
                measurement_date DATE,
                location TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        
        # Tabela de eventos e treinamentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                type TEXT NOT NULL CHECK (type IN ('treinamento', 'workshop', 'seminario', 'conferencia')),
                start_date DATETIME,
                end_date DATETIME,
                location TEXT,
                max_participants INTEGER,
                organizer_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (organizer_id) REFERENCES users (id)
            )
        ''')
        
        # Tabela de participação em eventos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS event_participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                user_id INTEGER,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                attended BOOLEAN DEFAULT 0,
                FOREIGN KEY (event_id) REFERENCES events (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Tabela de alertas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('prazo', 'tarefa', 'notificacao')),
                priority TEXT NOT NULL CHECK (priority IN ('baixa', 'media', 'alta')),
                read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Gera hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def populate_sample_data(self):
        """Popula o banco com dados de exemplo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar se já existem dados
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Usuários de exemplo
        users_data = [
            ('admin', self.hash_password('admin123'), 'Administrador Sistema', 'admin@embrapa.br', 'administrador', 'TI'),
            ('joao.silva', self.hash_password('pesq123'), 'João Silva', 'joao.silva@embrapa.br', 'pesquisador', 'Agricultura'),
            ('maria.santos', self.hash_password('gest123'), 'Maria Santos', 'maria.santos@embrapa.br', 'gestor', 'Biotecnologia'),
            ('carlos.oliveira', self.hash_password('pesq123'), 'Carlos Oliveira', 'carlos.oliveira@embrapa.br', 'pesquisador', 'Sustentabilidade'),
            ('ana.costa', self.hash_password('gest123'), 'Ana Costa', 'ana.costa@embrapa.br', 'gestor', 'Recursos Naturais')
        ]
        
        cursor.executemany('''
            INSERT INTO users (username, password, name, email, role, department)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', users_data)
        
        # Projetos de exemplo
        projects_data = [
            ('Desenvolvimento de novas variedades de soja resistentes à seca', 
             'Projeto focado no desenvolvimento de cultivares de soja com maior tolerância ao estresse hídrico',
             'agricultura', 2, 'em_andamento', '2024-01-15', '2025-12-31', 250000.0, 75000.0),
            ('Uso de biotecnologia para controle biológico de pragas',
             'Desenvolvimento de agentes de controle biológico para pragas agrícolas',
             'biotecnologia', 3, 'em_andamento', '2024-03-01', '2025-08-30', 180000.0, 45000.0),
            ('Manejo sustentável do solo em sistemas agropecuários',
             'Estudo de práticas sustentáveis para conservação e melhoria da qualidade do solo',
             'sustentabilidade', 4, 'planejamento', '2024-06-01', '2026-05-31', 320000.0, 0.0),
            ('Melhoramento genético de bovinos para clima tropical',
             'Programa de melhoramento genético focado em adaptação ao clima tropical',
             'agropecuaria', 2, 'concluido', '2023-01-01', '2024-01-31', 200000.0, 195000.0),
            ('Conservação de recursos hídricos em bacias hidrográficas',
             'Projeto de conservação e manejo sustentável de recursos hídricos',
             'recursos_naturais', 5, 'em_andamento', '2024-02-15', '2025-12-15', 280000.0, 120000.0)
        ]
        
        cursor.executemany('''
            INSERT INTO projects (title, description, area, responsible_id, status, start_date, end_date, budget, spent_budget)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', projects_data)
        
        # Funcionários de exemplo
        employees_data = [
            ('Dr. Roberto Mendes', 'Diretor Geral', 'Direção', 'roberto.mendes@embrapa.br', '(85) 3391-7000', '2020-01-15', None, 1),
            ('Dra. Fernanda Lima', 'Coordenadora de Pesquisa', 'Pesquisa', 'fernanda.lima@embrapa.br', '(85) 3391-7001', '2021-03-10', 1, 1),
            ('Dr. Paulo Rodrigues', 'Pesquisador Sênior', 'Agricultura', 'paulo.rodrigues@embrapa.br', '(85) 3391-7002', '2019-08-20', 2, 1),
            ('Dra. Luciana Ferreira', 'Pesquisadora', 'Biotecnologia', 'luciana.ferreira@embrapa.br', '(85) 3391-7003', '2022-01-05', 2, 1),
            ('MSc. Ricardo Alves', 'Assistente de Pesquisa', 'Sustentabilidade', 'ricardo.alves@embrapa.br', '(85) 3391-7004', '2023-06-15', 4, 1)
        ]
        
        cursor.executemany('''
            INSERT INTO employees (name, position, department, email, phone, hire_date, supervisor_id, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', employees_data)
        
        # Publicações de exemplo
        publications_data = [
            ('Tolerância à seca em cultivares de soja: uma revisão', 'Silva, J.; Santos, M.', 'artigo', 
             'Revista Brasileira de Agricultura', 2024, '10.1234/rba.2024.001', None, 1),
            ('Controle biológico: alternativa sustentável', 'Santos, M.; Oliveira, C.', 'livro',
             'Editora Embrapa', 2023, '10.1234/embrapa.2023.bio', None, 2),
            ('Práticas de manejo sustentável do solo', 'Oliveira, C.; Costa, A.', 'relatorio',
             'Embrapa Meio-Norte', 2024, None, 'relatorio_solo_2024.pdf', 3),
            ('Melhoramento genético bovino no semiárido', 'Silva, J.; Rodrigues, P.', 'artigo',
             'Revista de Zootecnia Tropical', 2024, '10.1234/rzt.2024.002', None, 4),
            ('Recursos hídricos e agricultura sustentável', 'Costa, A.; Lima, F.', 'capitulo',
             'Sustentabilidade no Semiárido', 2023, '10.1234/sus.2023.cap5', None, 5)
        ]
        
        cursor.executemany('''
            INSERT INTO publications (title, authors, type, journal, year, doi, file_path, project_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', publications_data)
        
        # Dados experimentais de exemplo
        experimental_data = []
        for project_id in range(1, 6):
            for i in range(20):
                date = datetime.now() - timedelta(days=random.randint(1, 365))
                experimental_data.append((
                    f'Experimento_{project_id}_{i+1}',
                    project_id,
                    random.choice(['Produtividade', 'Altura', 'Peso', 'Resistência', 'pH']),
                    round(random.uniform(10, 100), 2),
                    random.choice(['kg/ha', 'cm', 'kg', 'escala', 'unidade']),
                    date.strftime('%Y-%m-%d'),
                    random.choice(['Campo A', 'Campo B', 'Laboratório', 'Estufa']),
                    f'Observação do experimento {i+1}'
                ))
        
        cursor.executemany('''
            INSERT INTO experimental_data (experiment_name, project_id, variable_name, value, unit, measurement_date, location, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', experimental_data)
        
        # Eventos de exemplo
        events_data = [
            ('Workshop de Biotecnologia Agrícola', 'Workshop sobre aplicações da biotecnologia na agricultura',
             'workshop', '2024-07-15 09:00:00', '2024-07-15 17:00:00', 'Auditório Principal', 50, 3),
            ('Treinamento em Análise Estatística', 'Curso de análise estatística para pesquisadores',
             'treinamento', '2024-08-20 08:00:00', '2024-08-22 17:00:00', 'Sala de Treinamento', 25, 2),
            ('Seminário de Sustentabilidade', 'Apresentação de resultados de projetos sustentáveis',
             'seminario', '2024-09-10 14:00:00', '2024-09-10 18:00:00', 'Auditório Principal', 100, 4),
            ('Conferência de Recursos Naturais', 'Conferência sobre conservação de recursos naturais',
             'conferencia', '2024-10-05 08:00:00', '2024-10-07 17:00:00', 'Centro de Convenções', 200, 5)
        ]
        
        cursor.executemany('''
            INSERT INTO events (title, description, type, start_date, end_date, location, max_participants, organizer_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', events_data)
        
        # Alertas de exemplo
        alerts_data = [
            (2, 'Prazo do projeto se aproximando', 'O projeto de soja tem prazo até dezembro de 2025', 'prazo', 'media', 0),
            (3, 'Relatório pendente', 'Relatório mensal do projeto de biotecnologia está pendente', 'tarefa', 'alta', 0),
            (4, 'Nova publicação disponível', 'Artigo sobre manejo sustentável foi publicado', 'notificacao', 'baixa', 0),
            (5, 'Orçamento próximo do limite', 'Projeto de recursos hídricos utilizou 43% do orçamento', 'prazo', 'media', 0)
        ]
        
        cursor.executemany('''
            INSERT INTO alerts (user_id, title, message, type, priority, read)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', alerts_data)
        
        conn.commit()
        conn.close()
        print("Dados de exemplo inseridos com sucesso!")

# Inicializar banco de dados
if __name__ == "__main__":
    db = DatabaseManager()
    db.populate_sample_data()
