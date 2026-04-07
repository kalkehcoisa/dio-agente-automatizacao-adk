# 🤖 Automação de Tarefas com Google ADK

Este projeto demonstra o desenvolvimento de um **sistema multiagente** utilizando o **Google Agent Development Kit (ADK)** para automatizar fluxos de trabalho e integrar-se com quatro plataformas de gestão de tarefas **100% gratuitas e SaaS**: **ClickUp**, **Trello**, **Asana** e **Freedcamp**.

O sistema é composto por agentes especializados (um por plataforma) e um **agente orquestrador** que delega tarefas usando `AgentTool`. Esta arquitetura explora os conceitos de composição hierárquica, ferramentas (tools) e integração com APIs externas.

## 🎯 Objetivos do Projeto

- Demonstrar o uso do Google ADK para criar agentes de IA modulares.
- Integrar agentes com APIs REST de ferramentas reais e gratuitas.
- Utilizar `AgentTool` para compor um agente orquestrador.
- Aplicar padrões de automação para aumentar produtividade.

## 🧠 Arquitetura

```
Usuário
   │
   ▼
OrchestratorAgent (com AgentTools)
   │
   ├── ClickUpAgent   → Tools: criar/ler tarefas
   ├── TrelloAgent    → Tools: criar/ler cards
   ├── AsanaAgent     → Tools: criar/ler tarefas
   └── FreedcampAgent → Tools: criar/ler tarefas
```

- **OrchestratorAgent**: interpreta o pedido do usuário e decide qual plataforma usar.
- **Platform Agents**: cada um possui tools específicas que chamam APIs reais.
- **AgentTool**: encapsula um agente completo dentro de outro, permitindo reuso e especialização.

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- Google ADK (Agents, Tools, AgentTool)
- Requests (para chamadas HTTP)
- python-dotenv (configuração)
- pytest (testes unitários)

## 📦 Estrutura do Projeto

```
automacao_tarefas/
├── .env                     # Credenciais (não versionado)
├── requirements.txt         # Dependências principais
├── requirements-dev.txt     # Dependências de desenvolvimento
├── main.py                  # Ponto de entrada (CLI)
├── src/
│   ├── orchestrator.py      # Orquestrador + AgentTools
│   ├── platforms/
│   │   ├── base.py          # Factory para criação de agentes
│   │   ├── clickup.py       # Agente e tools do ClickUp
│   │   ├── trello.py        # Agente e tools do Trello
│   │   ├── asana.py         # Agente e tools do Asana
│   │   └── freedcamp.py     # Agente e tools do Freedcamp
│   └── utils/
│       └── config.py        # Carrega variáveis de ambiente
└── tests/                   # Testes unitários
```

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/automacao-tarefas-adk.git
cd automacao-tarefas-adk
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # para testes
```

### 4. Configure as credenciais

Copie o arquivo `.env.example` para `.env` e preencha com suas chaves de API:

```env
# ClickUp
CLICKUP_API_TOKEN=seu_token
CLICKUP_LIST_ID=lista_id

# Trello
TRELLO_API_KEY=sua_api_key
TRELLO_TOKEN=seu_token
TRELLO_BOARD_ID=id_do_quadro
TRELLO_DEFAULT_LIST_ID=id_da_lista_padrao

# Asana
ASANA_TOKEN=seu_token_pessoal
ASANA_DEFAULT_PROJECT_ID=id_do_projeto

# Freedcamp
FREEDCAMP_API_KEY=sua_api_key
FREEDCAMP_DEFAULT_PROJECT_ID=id_do_projeto
```

### 5. Execute o orquestrador

```bash
python main.py
```

Exemplos de interação:

```
Você: Crie uma tarefa "Revisar documentação" no ClickUp
Assistente: Tarefa criada com ID 12345

Você: No Trello, adicione um card "Corrigir bug" à lista "To Do"
Assistente: Card criado com sucesso

Você: Liste as tarefas do Asana
Assistente: Tarefas: 1. Revisão, 2. Testes
```

## 🔑 Obtendo Credenciais das Plataformas

### ClickUp (gratuito)
1. Acesse: https://clickup.com/
2. Crie uma conta gratuita
3. Vá em Settings → Apps → API Token
4. Copie o token e o ID da lista desejada

### Trello (gratuito)
1. Acesse: https://trello.com/
2. Crie uma conta gratuita
3. Acesse: https://trello.com/power-ups/admin
4. Clique em "Create new Power-Up" ou vá para https://trello.com/app-key
5. Copie a **API Key** e gere o **Token**
6. O Board ID está na URL do quadro: `https://trello.com/b/ID_DO_QUADRO/nome`

### Asana (gratuito)
1. Acesse: https://asana.com/
2. Crie uma conta gratuita
3. Acesse: https://app.asana.com/0/developer-console
4. Clique em "Create new token"
5. Copie o **Personal Access Token**
6. O Project ID está na URL do projeto

### Freedcamp (gratuito)
1. Acesse: https://freedcamp.com/
2. Crie uma conta gratuita
3. Acesse: https://freedcamp.com/api_keys
4. Clique em "Generate New API Key"
5. Copie a **API Key**
6. O Project ID está na URL do projeto

## 🧪 Testes

Execute a suíte de testes unitários com:

```bash
pytest tests/ -v --cov=src
```

Os testes utilizam mocks para evitar chamadas reais às APIs e garantir isolamento.

### Testes específicos por plataforma

```bash
pytest tests/platforms/test_clickup.py -v
pytest tests/platforms/test_trello.py -v
pytest tests/platforms/test_asana.py -v
pytest tests/platforms/test_freedcamp.py -v
```

## 🔌 Integração com as Plataformas

### ClickUp
- **Tool**: `criar_tarefa_clickup(nome, descricao)`
- **Tool**: `listar_tarefas_clickup()`
- **Autenticação**: Token de API (Bearer)
- **Plano**: Freemium (tasks ilimitadas)

### Trello
- **Tool**: `criar_card_trello(nome, descricao, lista_id)`
- **Tool**: `listar_cards_trello()`
- **Autenticação**: API Key + Token
- **Plano**: Freemium (cards ilimitados)

### Asana
- **Tool**: `criar_tarefa_asana(nome, descricao, projeto_id)`
- **Tool**: `listar_tarefas_asana()`
- **Autenticação**: Personal Access Token (Bearer)
- **Plano**: Freemium (tarefas ilimitadas)

### Freedcamp
- **Tool**: `criar_tarefa_freedcamp(titulo, descricao, projeto_id)`
- **Tool**: `listar_tarefas_freedcamp()`
- **Autenticação**: API Key (X-API-KEY)
- **Plano**: Freemium (projetos ilimitados)

## 🧩 Extensibilidade

Para adicionar uma nova plataforma:

1. Crie um arquivo em `src/platforms/nova_plataforma.py`.
2. Defina funções com `FunctionTool` (não use decoradores).
3. Use `create_platform_agent` para instanciar o agente.
4. No `orchestrator.py`, importe o agente e envolva-o com `AgentTool`.
5. Adicione o novo `AgentTool` à lista de tools do orquestrador.
6. Adicione as variáveis de ambiente no `.env`.

## 📝 Personalização do Modelo

Por padrão, o projeto usa `gemini-1.5-flash` (requer chave da Google configurada no ambiente). Você pode trocar para qualquer modelo suportado pelo ADK alterando o parâmetro `model` na criação dos agentes em `src/platforms/base.py`.

## 📚 Referências

- [Google ADK Python Docs](https://google.github.io/adk-docs/)
- [AgentTool no ADK](https://google.github.io/adk-docs/agents/agent-tool/)
- [ClickUp API](https://clickup.com/api)
- [Trello API](https://developer.atlassian.com/cloud/trello/rest)
- [Asana API](https://developers.asana.com/docs)
- [Freedcamp API](https://freedcamp.com/api_docs)
- [Pytest Documentation](https://docs.pytest.org/)

## 📄 Licença

Este projeto é apenas para fins educacionais, como parte de um trabalho acadêmico. Sinta-se à vontade para usá-lo como base para seus estudos.

---
