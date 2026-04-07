import requests
from google.adk.tools import FunctionTool
from src.platforms.base import create_platform_agent
from src.utils.config import get_config


def criar_tarefa_freedcamp(
    titulo: str, descricao: str = "", projeto_id: str = ""
) -> dict:
    """Cria uma nova tarefa no Freedcamp."""
    config = get_config()["freedcamp"]
    if not config["api_key"]:
        return {"erro": "API Key do Freedcamp não configurada"}

    url = "https://freedcamp.com/api/v1/tasks"
    headers = {"X-API-KEY": config["api_key"], "Content-Type": "application/json"}
    payload = {
        "title": titulo,
        "description": descricao,
        "project_id": projeto_id or config["default_project_id"],
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro ao criar tarefa no Freedcamp: {str(e)}"}


def listar_tarefas_freedcamp() -> list:
    """Lista as tarefas do projeto padrão do Freedcamp."""
    config = get_config()["freedcamp"]
    if not config["api_key"]:
        return [{"erro": "API Key do Freedcamp não configurada"}]

    url = f"https://freedcamp.com/api/v1/projects/{config['default_project_id']}/tasks"
    headers = {"X-API-KEY": config["api_key"]}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("tasks", [])
    except requests.exceptions.RequestException as e:
        return [{"erro": f"Erro ao listar tarefas: {str(e)}"}]


tool_criar = FunctionTool(criar_tarefa_freedcamp)
tool_listar = FunctionTool(listar_tarefas_freedcamp)

freedcamp_agent = create_platform_agent(
    name="FreedcampAgent",
    instructions="Você é um assistente especializado em gerenciar tarefas no Freedcamp. Use as ferramentas para criar ou listar tarefas.",
    tools=[tool_criar, tool_listar],
)
