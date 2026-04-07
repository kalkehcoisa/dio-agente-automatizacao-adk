from src.orchestrator import (
    clickup_tool,
    kanboard_tool,
    orchestrator,
    plane_tool,
    wekan_tool,
)


def test_orchestrator_has_expected_tools():
    """Verifica se o orquestrador possui todas as ferramentas de plataforma."""
    tool_names = [tool.name for tool in orchestrator.tools]
    assert "ClickUpAgent" in tool_names
    assert "PlaneAgent" in tool_names
    assert "WekanAgent" in tool_names
    assert "KanboardAgent" in tool_names


def test_each_platform_tool_is_agenttool():
    """Garante que cada tool é uma instância de AgentTool."""
    from google.adk.tools.agent_tool import AgentTool

    assert isinstance(clickup_tool, AgentTool)
    assert isinstance(plane_tool, AgentTool)
    assert isinstance(wekan_tool, AgentTool)
    assert isinstance(kanboard_tool, AgentTool)


def test_orchestrator_instruction_contains_platforms():
    """Verifica se a instrução menciona as quatro plataformas."""
    instruction = orchestrator.instruction
    assert "ClickUp" in instruction
    assert "Plane" in instruction
    assert "Wekan" in instruction
    assert "Kanboard" in instruction
