import pytest
from google.adk.tools.agent_tool import AgentTool
from src.orchestrator import orchestrator


def test_orchestrator_has_expected_tools(setup_test_env):
    """Verifica se o orquestrador possui as quatro ferramentas de plataforma."""
    tool_names = [tool.name for tool in orchestrator.tools]
    assert "ClickUpAgent" in tool_names
    assert "TrelloAgent" in tool_names
    assert "AsanaAgent" in tool_names
    assert "FreedcampAgent" in tool_names


def test_orchestrator_has_four_tools(setup_test_env):
    """Verifica se o orquestrador tem exatamente 4 ferramentas."""
    assert len(orchestrator.tools) == 4


def test_orchestrator_instruction_contains_platforms(setup_test_env):
    """Verifica se a instrução do orquestrador menciona as quatro plataformas."""
    instruction = orchestrator.instruction
    assert "ClickUp" in instruction
    assert "Trello" in instruction
    assert "Asana" in instruction
    assert "Freedcamp" in instruction


def test_orchestrator_has_correct_model(setup_test_env):
    """Verifica se o modelo configurado está correto."""
    assert orchestrator.model == "gemini-1.5-flash"
