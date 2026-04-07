import requests
from google.adk.tools import FunctionTool
from src.platforms.base import create_platform_agent
from src.utils.config import get_config


def criar_tarefa_clickup(nome: str, descricao: str = "") -> dict:
    """Cria uma nova tarefa no ClickUp."""
    config = get_config()["clickup"]  # lê a configuração a cada chamada
    if not config["token"]:
        return {"erro": "Token do ClickUp não configurado"}
    url = f"https://api.clickup.com/api/v2/list/{config['list_id']}/task"
    headers = {"Authorization": config["token"], "Content-Type": "application/json"}
    payload = {"name": nome, "description": descricao}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro na requisição: {str(e)}"}


def listar_tarefas_clickup() -> list:
    """Lista todas as tarefas do quadro padrão (lista configurada)."""
    config = get_config()["clickup"]
    if not config["token"]:
        return [{"erro": "Token do ClickUp não configurado"}]
    url = f"https://api.clickup.com/api/v2/list/{config['list_id']}/task"
    headers = {"Authorization": config["token"]}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # A API do ClickUp retorna as tarefas dentro da chave "tasks"
        return data.get("tasks", [])
    except requests.exceptions.RequestException as e:
        return [{"erro": f"Falha ao listar tarefas: {str(e)}"}]


criar_tarefa_tool = FunctionTool(criar_tarefa_clickup)
listar_tarefas_tool = FunctionTool(listar_tarefas_clickup)
tools_clickup = [criar_tarefa_tool, listar_tarefas_tool]

clickup_agent = create_platform_agent(
    name="ClickUpAgent",
    instructions="Você é um assistente especializado em gerenciar tarefas no ClickUp. Use as ferramentas para criar ou listar tarefas.",
    tools=tools_clickup,
)
