# 🌱 Dashboard Embrapa - Como Executar

## 🚀 EXECUÇÃO RÁPIDA

### Opção 1: Script Automático (Recomendado)
```bash
python executar.py
```

### Opção 2: Comando Direto
```bash
pip install streamlit pandas plotly openpyxl
streamlit run app.py
```

## 📋 O que você precisa

- ✅ Python 3.8+ instalado
- ✅ Conexão com internet
- ✅ Navegador web

## 🔑 Como usar após executar

1. **Aguarde** o sistema carregar (pode demorar alguns segundos)
2. **Acesse** http://localhost:8501 (abre automaticamente)
3. **Faça login** com uma das contas de teste:

| Usuário | Senha | Tipo |
|---------|-------|------|
| `admin` | `admin123` | Administrador |
| `joao.silva` | `pesq123` | Pesquisador |
| `maria.santos` | `gest123` | Gestor |

## 📊 Funcionalidades Disponíveis

- **🏠 Dashboard** - Visão geral do sistema
- **📊 Projetos PD&I** - Gestão de projetos de pesquisa
- **👥 Gestão Administrativa** - Funcionários e organograma
- **📈 Indicadores (KPIs)** - Métricas de desempenho
- **📚 Publicações** - Artigos e documentos científicos
- **🧪 Dados Experimentais** - Análise de experimentos
- **🔔 Alertas** - Notificações e lembretes
- **📤 Exportação** - Relatórios em Excel/CSV

## 🛠️ Problemas Comuns

### "Python não é reconhecido"
- **Windows**: Instale Python do site oficial
- **Linux/Mac**: Use `python3` ao invés de `python`

### "Erro ao instalar dependências"
```bash
pip install --upgrade pip
pip install streamlit pandas plotly openpyxl --force-reinstall
```

### "Porta já está em uso"
```bash
streamlit run app.py --server.port=8502
```

### "Módulo não encontrado"
- Certifique-se de estar na pasta correta do projeto
- Verifique se todos os arquivos estão presentes

## 🔄 Reiniciar Sistema

Para reiniciar completamente:

1. **Pare** o sistema (Ctrl+C)
2. **Delete** o arquivo `embrapa_dashboard.db` (se existir)
3. **Execute** novamente: `python executar.py`

## 📞 Suporte

Se ainda tiver problemas:

1. **Verifique** se tem Python 3.8+ instalado
2. **Confirme** que está na pasta correta do projeto
3. **Tente** executar: `python check_system.py`

---

**🌱 Dashboard Embrapa Meio-Norte**  
*Sistema de Gestão de Pesquisa, Desenvolvimento e Inovação*

**Desenvolvido para facilitar a gestão de projetos de PD&I, acompanhamento de indicadores e administração de recursos na Embrapa Meio-Norte.**