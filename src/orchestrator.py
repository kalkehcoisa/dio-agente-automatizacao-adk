from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from src.platforms.clickup import clickup_agent
from src.platforms.kanboard import kanboard_agent
from src.platforms.plane import plane_agent
from src.platforms.wekan import wekan_agent

# Transforma cada agente em uma ferramenta
clickup_tool = AgentTool(agent=clickup_agent)
plane_tool = AgentTool(agent=plane_agent)
wekan_tool = AgentTool(agent=wekan_agent)
kanboard_tool = AgentTool(agent=kanboard_agent)

orchestrator = Agent(
    model="gemini-1.5-flash",
    name="OrchestratorAgent",
    instruction="""
    Você é um orquestrador de automação de tarefas. Você tem acesso a quatro assistentes especializados:
    - ClickUpAgent: cria e gerencia tarefas no ClickUp
    - PlaneAgent: trabalha com issues no Plane
    - WekanAgent: gerencia cards no Wekan
    - KanboardAgent: gerencia tarefas no Kanboard

    O usuário vai pedir para criar ou listar tarefas. Você deve decidir qual ferramenta usar baseado na plataforma mencionada.
    Se o usuário não especificar, pergunte qual plataforma ele prefere.
    Não invente respostas – sempre delegue a tarefa para o agente correto.
    """,
    tools=[clickup_tool, plane_tool, wekan_tool, kanboard_tool],
)
