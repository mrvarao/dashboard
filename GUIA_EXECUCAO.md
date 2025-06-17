# 🌱 Dashboard Embrapa Meio-Norte - Guia de Execução

## 📋 Pré-requisitos

Antes de executar o sistema, certifique-se de ter:

1. **Python 3.8 ou superior** instalado
2. **pip** (gerenciador de pacotes Python)
3. **Conexão com a internet** (para instalar dependências)

### Verificar Python
```bash
python --version
# ou
python3 --version
```

### Verificar pip
```bash
pip --version
# ou
pip3 --version
```

## 🚀 Execução Automática (Recomendado)

### Opção 1: Script Automático
```bash
python setup_and_run.py
```

Este script irá:
- ✅ Instalar todas as dependências automaticamente
- ✅ Inicializar o banco de dados com dados de exemplo
- ✅ Executar a aplicação
- ✅ Abrir automaticamente no navegador

## 🔧 Execução Manual (Passo a Passo)

### Passo 1: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 2: Inicializar Banco de Dados
```bash
python database.py
```

### Passo 3: Executar Aplicação
```bash
streamlit run app.py
```

### Passo 4: Acessar Sistema
- Abra seu navegador
- Acesse: `http://localhost:8501`

## 👤 Usuários de Teste

O sistema vem com usuários pré-cadastrados:

| Usuário | Senha | Tipo | Permissões |
|---------|-------|------|------------|
| `admin` | `admin123` | Administrador | Acesso completo |
| `joao.silva` | `pesq123` | Pesquisador | Projetos e dados |
| `maria.santos` | `gest123` | Gestor | Visualização e relatórios |

## 🔍 Verificação de Problemas

### Teste de Dependências
```bash
python test_dependencies.py
```

### Problemas Comuns

#### 1. Erro de Importação
```bash
# Atualizar pip
pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --no-cache-dir
```

#### 2. Erro de Banco de Dados
```bash
# Deletar banco existente
rm embrapa_dashboard.db

# Recriar banco
python database.py
```

#### 3. Porta em Uso
```bash
# Usar porta diferente
streamlit run app.py --server.port=8502
```

#### 4. Problemas com Virtual Environment
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## 📱 Funcionalidades Disponíveis

### 🏠 Dashboard Principal
- Métricas gerais do sistema
- Gráficos de resumo
- Visão geral dos projetos

### 📊 Projetos PD&I
- Cadastro de novos projetos
- Acompanhamento de progresso
- Controle orçamentário
- Filtros e visualizações

### 👥 Gestão Administrativa
- Cadastro de funcionários
- Organograma interativo
- Gestão de eventos
- Relatórios administrativos

### 📈 Indicadores (KPIs)
- KPIs customizáveis
- Gráficos de produtividade
- Análise de metas
- Ranking de pesquisadores

### 📚 Publicações
- Cadastro de publicações científicas
- Sistema de busca
- Análises bibliométricas
- Download de arquivos

### 🧪 Dados Experimentais
- Importação via CSV
- Visualização interativa
- Análise estatística
- Detecção de outliers

### 🔔 Alertas
- Sistema de notificações
- Alertas de prazos
- Tarefas pendentes
- Configurações personalizáveis

### 📤 Exportação
- Relatórios em PDF
- Exportação em Excel
- Dados em CSV
- Relatórios executivos

## 🛠️ Personalização

### Adicionar Novos Usuários
1. Acesse a seção administrativa
2. Use as credenciais de administrador
3. Cadastre novos usuários com diferentes permissões

### Modificar Dados de Exemplo
1. Edite o arquivo `database.py`
2. Modifique a função `populate_sample_data()`
3. Delete o arquivo `embrapa_dashboard.db`
4. Execute novamente o sistema

### Customizar Interface
1. Edite o arquivo `app.py`
2. Modifique o CSS na seção de estilos
3. Ajuste cores, fontes e layout

## 📞 Suporte

### Logs do Sistema
- Verifique o arquivo `streamlit.log` para erros
- Use o console do navegador para erros de interface

### Comandos Úteis
```bash
# Ver logs em tempo real
tail -f streamlit.log

# Verificar processos Streamlit
ps aux | grep streamlit

# Parar todos os processos Streamlit
pkill -f streamlit
```

### Backup dos Dados
```bash
# Fazer backup do banco
cp embrapa_dashboard.db backup_$(date +%Y%m%d).db

# Restaurar backup
cp backup_YYYYMMDD.db embrapa_dashboard.db
```

## 🎯 Próximos Passos

Após executar o sistema:

1. **Faça login** com um dos usuários de teste
2. **Explore as funcionalidades** disponíveis
3. **Cadastre novos dados** conforme necessário
4. **Configure alertas** para suas necessidades
5. **Exporte relatórios** para análise

## 📊 Estrutura do Projeto

```
embrapa_dashboard/
├── app.py                 # Aplicação principal
├── auth.py               # Sistema de autenticação
├── database.py           # Gerenciamento do banco
├── requirements.txt      # Dependências
├── setup_and_run.py     # Script de execução automática
├── test_dependencies.py # Teste de dependências
└── modules/             # Módulos funcionais
    ├── projects.py      # Gestão de projetos
    ├── admin.py         # Gestão administrativa
    ├── kpis.py          # Indicadores
    ├── publications.py  # Publicações
    ├── experimental_data.py # Dados experimentais
    ├── alerts.py        # Sistema de alertas
    └── export.py        # Exportação
```

---

**🌱 Dashboard Embrapa Meio-Norte**  
*Sistema de Gestão de PD&I e Processos Administrativos*