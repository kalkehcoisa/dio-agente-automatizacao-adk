import requests
from google.adk.tools import FunctionTool
from src.platforms.base import create_platform_agent
from src.utils.config import get_config


def criar_tarefa_asana(nome: str, descricao: str = "", projeto_id: str = "") -> dict:
    """Cria uma nova tarefa no Asana."""
    config = get_config()["asana"]
    if not config["token"]:
        return {"erro": "Token do Asana não configurado"}

    url = "https://app.asana.com/api/1.0/tasks"
    headers = {
        "Authorization": f"Bearer {config['token']}",
        "Content-Type": "application/json",
    }
    payload = {
        "data": {
            "name": nome,
            "notes": descricao,
            "projects": [projeto_id or config["default_project_id"]],
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro ao criar tarefa no Asana: {str(e)}"}


def listar_tarefas_asana() -> list:
    """Lista as tarefas do projeto padrão do Asana."""
    config = get_config()["asana"]
    if not config["token"]:
        return [{"erro": "Token do Asana não configurado"}]

    url = f"https://app.asana.com/api/1.0/projects/{config['default_project_id']}/tasks"
    headers = {"Authorization": f"Bearer {config['token']}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except requests.exceptions.RequestException as e:
        return [{"erro": f"Erro ao listar tarefas: {str(e)}"}]


tool_criar = FunctionTool(criar_tarefa_asana)
tool_listar = FunctionTool(listar_tarefas_asana)

asana_agent = create_platform_agent(
    name="AsanaAgent",
    instructions="Você é um assistente especializado em gerenciar tarefas no Asana. Use as ferramentas para criar ou listar tarefas.",
    tools=[tool_criar, tool_listar],
)
