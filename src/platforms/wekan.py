import requests
from google.adk.tools import FunctionTool
from src.platforms.base import create_platform_agent
from src.utils.config import get_config


def criar_card_wekan(board_id: str, list_id: str, titulo: str) -> dict:
    """Cria um card no Wekan."""
    config = get_config()["wekan"]
    if not all([config["api_url"], config["user_id"], config["token"]]):
        return {"erro": "Configuração do Wekan incompleta"}
    url = f"{config['api_url']}/boards/{board_id}/lists/{list_id}/cards"
    headers = {"Authorization": f"Bearer {config['token']}"}
    payload = {"title": titulo}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro na requisição: {str(e)}"}


tools_wekan = [FunctionTool(criar_card_wekan)]

wekan_agent = create_platform_agent(
    name="WekanAgent",
    instructions="Assistente para o Wekan, um kanban open-source.",
    tools=tools_wekan,
)
