import requests
from google.adk.tools import FunctionTool
from src.platforms.base import create_platform_agent
from src.utils.config import get_config


def criar_tarefa_plane(projeto_id: str, titulo: str, conteudo: str = "") -> dict:
    config = get_config()["plane"]
    if not config["token"]:
        return {"erro": "Token do Plane não configurado"}
    url = f"{config['base_url']}/workspaces/me/projects/{projeto_id}/issues/"
    headers = {"Authorization": f"Bearer {config['token']}"}
    payload = {"title": titulo, "description_html": conteudo}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro na requisição: {str(e)}"}
    except Exception as e:
        # captura qualquer outra exceção (ex: ConnectionError, Timeout)
        return {"erro": f"Erro inesperado: {str(e)}"}


tools_plane = [FunctionTool(criar_tarefa_plane)]

plane_agent = create_platform_agent(
    name="PlaneAgent",
    instructions="Você gerencia tarefas no Plane, uma ferramenta open-source de planejamento.",
    tools=tools_plane,
)
