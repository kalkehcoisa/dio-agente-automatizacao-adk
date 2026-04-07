import requests
from google.adk.tools import FunctionTool
from src.platforms.base import create_platform_agent
from src.utils.config import get_config


def criar_card_trello(nome: str, descricao: str = "", lista_id: str = "") -> dict:
    """Cria um novo card no Trello."""
    config = get_config()["trello"]
    if not config["api_key"] or not config["token"]:
        return {"erro": "API Key ou Token do Trello não configurados"}

    url = "https://api.trello.com/1/cards"
    params = {
        "key": config["api_key"],
        "token": config["token"],
        "name": nome,
        "desc": descricao,
        "idList": lista_id or config["default_list_id"],
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro ao criar card no Trello: {str(e)}"}


def listar_cards_trello() -> list:
    """Lista os cards do quadro padrão do Trello."""
    config = get_config()["trello"]
    if not config["api_key"] or not config["token"]:
        return [{"erro": "API Key ou Token do Trello não configurados"}]

    url = f"https://api.trello.com/1/boards/{config['board_id']}/cards"
    params = {"key": config["api_key"], "token": config["token"]}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return [{"erro": f"Erro ao listar cards: {str(e)}"}]


tool_criar = FunctionTool(criar_card_trello)
tool_listar = FunctionTool(listar_cards_trello)

trello_agent = create_platform_agent(
    name="TrelloAgent",
    instructions="Você é um assistente especializado em gerenciar cards no Trello. Use as ferramentas para criar ou listar cards.",
    tools=[tool_criar, tool_listar],
)
