
# 🌱 Dashboard Embrapa Meio-Norte

Sistema completo de gestão de PD&I (Pesquisa, Desenvolvimento e Inovação) e processos administrativos desenvolvido em Python com Streamlit.

## 🚀 COMO EXECUTAR - INÍCIO RÁPIDO

### Método 1: Execução Direta (Recomendado)
```bash
python EXECUTAR_DASHBOARD.py
```

### Método 2: Execução Otimizada
```bash
python EXECUTAR_AGORA.py
```

### Método 3: Execução Simples
```bash
python RODAR_DASHBOARD.py
```

### 📱 Acesso ao Sistema
- **URL:** http://localhost:8501
- **Login Administrador:** admin / admin123
- **Login Pesquisador:** joao.silva / pesq123
- **Login Gestor:** maria.santos / gest123

### ⚡ Requisitos Mínimos
- Python 3.8+
- Conexão com internet (para instalação automática de dependências)

> **Nota:** O sistema instala automaticamente todas as dependências necessárias (Streamlit, Pandas, Plotly, etc.)

## 📋 Funcionalidades

### 🔐 Sistema de Autenticação
- 3 tipos de usuários: Administrador, Pesquisador e Gestor
- Controle de permissões por funcionalidade
- Interface de login segura

### 📊 Gestão de Projetos PD&I
- Cadastro e acompanhamento de projetos
- Visualização com gráficos interativos
- Filtros por tipo, responsável, prazo e status
- Controle orçamentário
- Relatórios de progresso

### 👥 Gestão Administrativa
- Cadastro de funcionários
- Organograma interativo
- Gestão de eventos e treinamentos
- Relatórios administrativos

### 📈 Indicadores de Desempenho (KPIs)
- KPIs customizáveis
- Gráficos de produtividade
- Análise de metas e prazos
- Ranking de pesquisadores
- Métricas por área de pesquisa

### 📚 Publicações e Relatórios
- Cadastro de publicações científicas
- Sistema de busca avançada
- Análises bibliométricas
- Download de arquivos

### 🧪 Dados Experimentais
- Importação de dados via CSV
- Visualização interativa
- Análise estatística básica
- Detecção de outliers
- Análise de correlação

### 🔔 Alertas e Notificações
- Sistema de alertas automáticos
- Notificações de prazos
- Tarefas pendentes
- Configurações personalizáveis

### 📤 Exportação
- Exportação em CSV, Excel e PDF
- Relatórios executivos
- Relatórios por área
- Relatórios de produtividade

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone ou baixe o projeto:**
```bash
cd embrapa_dashboard
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação:**
```bash
streamlit run app.py
```

4. **Acesse o sistema:**
- Abra seu navegador
- Acesse: `http://localhost:8501`

## 👤 Usuários de Teste

O sistema vem com usuários pré-cadastrados para teste:

| Usuário | Senha | Tipo | Descrição |
|---------|-------|------|-----------|
| admin | admin123 | Administrador | Acesso completo ao sistema |
| joao.silva | pesq123 | Pesquisador | Gestão de projetos e dados |
| maria.santos | gest123 | Gestor | Visualização e relatórios |

## 📊 Dados de Exemplo

O sistema inclui dados de exemplo nas seguintes áreas:
- **Agricultura**: Desenvolvimento de variedades de soja
- **Biotecnologia**: Controle biológico de pragas
- **Sustentabilidade**: Manejo sustentável do solo
- **Agropecuária**: Melhoramento genético bovino
- **Recursos Naturais**: Conservação de recursos hídricos

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:
- `users`: Usuários do sistema
- `projects`: Projetos de PD&I
- `employees`: Funcionários
- `publications`: Publicações científicas
- `experimental_data`: Dados experimentais
- `events`: Eventos e treinamentos
- `alerts`: Alertas e notificações

## 📁 Estrutura do Projeto

```
embrapa_dashboard/
├── app.py                 # Aplicação principal
├── auth.py               # Sistema de autenticação
├── database.py           # Gerenciamento do banco de dados
├── requirements.txt      # Dependências Python
├── README.md            # Este arquivo
└── modules/             # Módulos funcionais
    ├── projects.py      # Gestão de projetos
    ├── admin.py         # Gestão administrativa
    ├── kpis.py          # Indicadores de desempenho
    ├── publications.py  # Gestão de publicações
    ├── experimental_data.py # Dados experimentais
    ├── alerts.py        # Sistema de alertas
    └── export.py        # Exportação de dados
```

## 🔧 Personalização

### Adicionando Novos KPIs
1. Edite o arquivo `modules/kpis.py`
2. Adicione novas métricas na função `show_custom_kpis()`
3. Implemente as consultas SQL necessárias

### Modificando Áreas de Pesquisa
1. Edite o arquivo `database.py`
2. Modifique a lista de áreas na função `populate_sample_data()`
3. Atualize os formulários em `modules/projects.py`

### Adicionando Novos Tipos de Usuário
1. Modifique a tabela `users` em `database.py`
2. Atualize o sistema de permissões em `auth.py`
3. Ajuste a interface conforme necessário

## 📈 KPIs Prioritários

O sistema monitora os seguintes indicadores:
- Número de publicações
- Projetos concluídos
- Orçamento utilizado
- Número de treinamentos realizados
- Produtividade por pesquisador
- Tempo médio de execução dos projetos

## 🔒 Segurança

- Senhas são armazenadas com hash SHA-256
- Controle de acesso baseado em roles
- Validação de entrada em todos os formulários
- Proteção contra SQL injection

## 🐛 Solução de Problemas

### Erro ao instalar dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Erro de banco de dados
- Delete o arquivo `embrapa_dashboard.db`
- Reinicie a aplicação para recriar o banco

### Erro de importação de módulos
- Verifique se está no diretório correto
- Certifique-se de que todos os arquivos estão presentes

## 🤝 Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Teste thoroughly
5. Submeta um pull request

## 📞 Suporte

Para suporte técnico:
- Verifique a documentação
- Consulte os logs de erro
- Entre em contato com a equipe de desenvolvimento

## 📄 Licença

Este projeto foi desenvolvido para a Embrapa Meio-Norte e está sujeito às políticas internas da instituição.

## 🔄 Atualizações

### Versão 1.0.0
- Sistema completo de gestão PD&I
- Interface responsiva
- Múltiplos formatos de exportação
- Análises estatísticas básicas
- Sistema de alertas automáticos

---

**Desenvolvido para Embrapa Meio-Norte** 🌱
Sistema de Gestão de PD&I e Processos Administrativos
