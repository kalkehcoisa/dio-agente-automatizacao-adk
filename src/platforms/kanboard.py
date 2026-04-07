import requests
from google.adk.tools import FunctionTool
from src.platforms.base import create_platform_agent
from src.utils.config import get_config


def criar_tarefa_kanboard(projeto_id: int, titulo: str) -> dict:
    """Cria tarefa no Kanboard via JSON-RPC."""
    config = get_config()["kanboard"]
    if not config["api_url"]:
        return {"erro": "Kanboard não configurado"}
    payload = {
        "jsonrpc": "2.0",
        "method": "createTask",
        "params": {"title": titulo, "project_id": projeto_id},
        "id": 1,
    }
    auth = (config["username"], config["password"])
    try:
        response = requests.post(config["api_url"], json=payload, auth=auth)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro na requisição: {str(e)}"}


tools_kanboard = [FunctionTool(criar_tarefa_kanboard)]

kanboard_agent = create_platform_agent(
    name="KanboardAgent",
    instructions="Agente para Kanboard, ferramenta minimalista de Kanban.",
    tools=tools_kanboard,
)
