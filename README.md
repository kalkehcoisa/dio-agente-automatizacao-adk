# 🤖 Automação de Tarefas com Google ADK

Este projeto demonstra o desenvolvimento de um **sistema multiagente** utilizando o **Google Agent Development Kit (ADK)** para automatizar fluxos de trabalho e integrar-se com quatro plataformas de gestão de tarefas: **ClickUp**, **Plane**, **Wekan** e **Kanboard**.

O sistema é composto por agentes especializados (um por plataforma) e um **agente orquestrador** que delega tarefas usando `AgentTool`. Esta arquitetura explora os conceitos de composição hierárquica, ferramentas (tools) e integração com APIs externas.

## 🎯 Objetivos do Projeto

- Demonstrar o uso do Google ADK para criar agentes de IA modulares.
- Integrar agentes com APIs REST de ferramentas reais.
- Utilizar `AgentTool` para compor um agente orquestrador.
- Aplicar padrões de automação para aumentar produtividade.

## 🧠 Arquitetura

```
Usuário
   │
   ▼
OrchestratorAgent (com AgentTools)
   │
   ├── ClickUpAgent → Tools: criar/ler tarefas
   ├── PlaneAgent   → Tools: criar issues
   ├── WekanAgent   → Tools: criar cards
   └── KanboardAgent→ Tools: criar tarefas
```

- **OrchestratorAgent**: interpreta o pedido do usuário e decide qual plataforma usar.
- **Platform Agents**: cada um possui tools específicas que chamam APIs reais ou simuladas.
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
│   │   ├── plane.py
│   │   ├── wekan.py
│   │   └── kanboard.py
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

### 4. Configure as credenciais (opcional)

Copie o arquivo `.env.example` para `.env` e preencha com suas chaves de API.  
Se não fornecer credenciais, as tools retornarão mensagens de erro ou você pode usar as versões mock.

### 5. Execute o orquestrador

```bash
python main.py
```

Exemplos de interação:

```
Você: Crie uma tarefa "Revisar documentação" no ClickUp
Assistente: [Agente ClickUp] Tarefa criada com ID 12345

Você: No Plane, adicione uma issue "Corrigir bug de login" ao projeto "MeuProjeto"
Assistente: [Agente Plane] Issue criada com sucesso
```

## 🧪 Testes

Execute a suíte de testes unitários com:

```bash
pytest tests/ -v --cov=src
```

Os testes utilizam mocks para evitar chamadas reais às APIs e garantir isolamento.

## 🔌 Integração com Plataformas Reais

### ClickUp
- **Tool**: `criar_tarefa_clickup(nome, descricao)`
- **Autenticação**: Token de API (Bearer)
- **Documentação**: [ClickUp API](https://clickup.com/api)

### Plane (open-source)
- **Tool**: `criar_tarefa_plane(projeto_id, titulo, conteudo)`
- **Autenticação**: Bearer token
- **Documentação**: [Plane API](https://docs.plane.so/)

### Wekan (open-source)
- **Tool**: `criar_card_wekan(board_id, list_id, titulo)`
- **Autenticação**: Bearer token ou userId + token
- **Documentação**: [Wekan API](https://wekan.github.io/api/)

### Kanboard (open-source)
- **Tool**: `criar_tarefa_kanboard(projeto_id, titulo)`
- **Autenticação**: HTTP Basic Auth ou token
- **Documentação**: [Kanboard API (JSON-RPC)](https://docs.kanboard.org/en/latest/api/json_rpc.html)

## 🧩 Extensibilidade

Para adicionar uma nova plataforma:

1. Crie um arquivo em `src/platforms/nova_plataforma.py`.
2. Defina funções decoradas com `@tool` (ou usando `FunctionTool`).
3. Use `create_platform_agent` para instanciar o agente.
4. No `orchestrator.py`, importe o agente e envolva-o com `AgentTool`.
5. Adicione o novo `AgentTool` à lista de tools do orquestrador.

## 📝 Personalização do Modelo

Por padrão, o projeto usa `gemini-1.5-flash` (requer chave da Google configurada no ambiente). Você pode trocar para qualquer modelo suportado pelo ADK alterando o parâmetro `model` na criação dos agentes.

## 📚 Referências

- [Google ADK Python Docs](https://google.github.io/adk-docs/)
- [AgentTool no ADK](https://google.github.io/adk-docs/agents/agent-tool/)
- [Pytest Documentation](https://docs.pytest.org/)

## 📄 Licença

Este projeto é apenas para fins educacionais, como parte de um trabalho acadêmico. Sinta-se à vontade para usá-lo como base para seus estudos.

---
