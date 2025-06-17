# 🚀 Como Criar Repositório GitHub para o Dashboard Embrapa

## 📋 Passo a Passo

### 1. Criar Repositório no GitHub
1. Acesse [GitHub.com](https://github.com)
2. Clique em "New repository" (botão verde)
3. Configure o repositório:
   - **Repository name:** `dashboard-embrapa-meio-norte`
   - **Description:** `Sistema de gestão de PD&I da Embrapa Meio-Norte desenvolvido em Python/Streamlit`
   - **Visibility:** Public ✅
   - **Initialize:** Não marque nenhuma opção (README, .gitignore, license)
4. Clique em "Create repository"

### 2. Comandos Git para Upload

Execute os comandos abaixo no terminal, dentro da pasta do projeto:

```bash
# Inicializar repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer o primeiro commit
git commit -m "🌱 Dashboard Embrapa Meio-Norte - Sistema completo de gestão PD&I

- Sistema de autenticação com 3 tipos de usuários
- Gestão de projetos de pesquisa e desenvolvimento
- Administração de funcionários e eventos
- KPIs e indicadores de desempenho
- Publicações científicas e dados experimentais
- Sistema de alertas e exportação de relatórios
- Interface web responsiva com Streamlit"

# Adicionar origem remota (substitua SEU_USUARIO pelo seu username do GitHub)
git remote add origin https://github.com/SEU_USUARIO/dashboard-embrapa-meio-norte.git

# Definir branch principal
git branch -M main

# Enviar para o GitHub
git push -u origin main
```

### 3. Exemplo de URL Final
Substitua `SEU_USUARIO` pelo seu username do GitHub:
```
https://github.com/SEU_USUARIO/dashboard-embrapa-meio-norte
```

### 4. Configurar Repositório (Opcional)

Após criar o repositório, você pode:

1. **Adicionar Topics/Tags:**
   - `python`
   - `streamlit`
   - `dashboard`
   - `embrapa`
   - `research`
   - `data-visualization`
   - `web-app`

2. **Editar About:**
   - Description: "Sistema de gestão de PD&I da Embrapa Meio-Norte"
   - Website: Deixe em branco ou adicione uma demo se hospedar
   - Topics: Adicione as tags acima

3. **Configurar GitHub Pages (se desejar):**
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: main / (root)

## 🔧 Comandos Git Úteis

### Para atualizações futuras:
```bash
# Adicionar mudanças
git add .

# Commit com mensagem
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push
```

### Para clonar em outro local:
```bash
git clone https://github.com/SEU_USUARIO/dashboard-embrapa-meio-norte.git
```

## 📝 Estrutura do Repositório

O repositório conterá:
```
dashboard-embrapa-meio-norte/
├── README.md                    # Documentação principal
├── EXECUTAR_DASHBOARD.py        # Script principal de execução
├── EXECUTAR_AGORA.py           # Script otimizado
├── RODAR_DASHBOARD.py          # Script simplificado
├── app.py                      # Aplicação Streamlit principal
├── auth.py                     # Sistema de autenticação
├── database.py                 # Gerenciamento do banco de dados
├── modules/                    # Módulos do sistema
│   ├── projects.py
│   ├── admin.py
│   ├── kpis.py
│   └── ...
├── requirements.txt            # Dependências Python
├── .gitignore                 # Arquivos ignorados pelo Git
└── docs/                      # Documentação adicional
```

## ✅ Verificação Final

Após executar os comandos, verifique:
1. ✅ Repositório criado no GitHub
2. ✅ Todos os arquivos enviados
3. ✅ README.md sendo exibido na página principal
4. ✅ Repositório público e acessível

## 🎯 Próximos Passos

1. Compartilhe o link do repositório
2. Considere adicionar uma licença (MIT recomendada)
3. Crie releases para versões estáveis
4. Adicione screenshots no README
5. Configure GitHub Actions para CI/CD (opcional)