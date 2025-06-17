# 🌱 Como Executar o Dashboard Embrapa

## 🚀 Execução Rápida (Recomendado)

### Método 1: Script Automático
```bash
python run_dashboard.py
```

### Método 2: Streamlit Direto
```bash
pip install streamlit pandas plotly
streamlit run app.py
```

## 📋 Pré-requisitos

- ✅ Python 3.8 ou superior
- ✅ Conexão com internet (para instalar dependências)

## 🔑 Login no Sistema

Após executar, acesse: **http://localhost:8501**

**Usuários de teste:**
- **Admin:** `admin` / `admin123`
- **Pesquisador:** `joao.silva` / `pesq123`
- **Gestor:** `maria.santos` / `gest123`

## 🛠️ Solução de Problemas

### Erro "Python não encontrado"
```bash
# Windows
python --version

# Linux/Mac
python3 --version
```

### Erro "Streamlit não encontrado"
```bash
pip install streamlit
```

### Erro "Porta em uso"
```bash
streamlit run app.py --server.port=8502
```

### Erro de dependências
```bash
pip install -r requirements.txt
```

## 📱 Funcionalidades

- 📊 **Projetos PD&I** - Gestão completa de projetos
- 👥 **Administração** - Funcionários e organograma  
- 📈 **KPIs** - Indicadores de desempenho
- 📚 **Publicações** - Gestão de artigos científicos
- 🧪 **Dados Experimentais** - Análise de experimentos
- 🔔 **Alertas** - Notificações e prazos
- 📤 **Exportação** - Relatórios em PDF/Excel

## 🆘 Suporte

Se encontrar problemas:

1. **Verifique o sistema:**
   ```bash
   python check_system.py
   ```

2. **Reinstale dependências:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

3. **Recrie o banco de dados:**
   ```bash
   python database.py
   ```

---

**🌱 Dashboard Embrapa Meio-Norte**  
*Sistema de Gestão de PD&I*