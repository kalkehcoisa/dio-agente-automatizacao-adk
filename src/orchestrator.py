from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from src.platforms.asana import asana_agent
from src.platforms.clickup import clickup_agent
from src.platforms.freedcamp import freedcamp_agent
from src.platforms.trello import trello_agent

clickup_tool = AgentTool(agent=clickup_agent)
trello_tool = AgentTool(agent=trello_agent)
asana_tool = AgentTool(agent=asana_agent)
freedcamp_tool = AgentTool(agent=freedcamp_agent)

orchestrator = LlmAgent(
    model="gemini-1.5-flash",
    name="OrchestratorAgent",
    instruction="""
    Você é um orquestrador de automação de tarefas. Você tem acesso a quatro assistentes especializados:
    - ClickUpAgent: cria e gerencia tarefas no ClickUp
    - TrelloAgent: cria e gerencia cards no Trello
    - AsanaAgent: cria e gerencia tarefas no Asana
    - FreedcampAgent: cria e gerencia tarefas no Freedcamp

    O usuário vai pedir para criar ou listar tarefas. Você deve decidir qual ferramenta usar baseado na plataforma mencionada.
    Se o usuário não especificar, pergunte qual plataforma ele prefere.
    """,
    tools=[clickup_tool, trello_tool, asana_tool, freedcamp_tool],
)
