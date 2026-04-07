from unittest.mock import MagicMock, patch

import pytest
from src.platforms.asana import asana_agent, criar_tarefa_asana, listar_tarefas_asana


class TestAsanaTools:
    @patch("src.platforms.asana.requests.post")
    def test_criar_tarefa_asana_success(self, mock_post, setup_test_env):
        """Testa criação bem-sucedida de tarefa no Asana."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {"gid": "123", "name": "Nova Tarefa"}
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = criar_tarefa_asana("Nova Tarefa", "Descrição detalhada")
        assert result["data"]["gid"] == "123"
        assert result["data"]["name"] == "Nova Tarefa"
        mock_post.assert_called_once()

    @patch("src.platforms.asana.requests.post")
    def test_criar_tarefa_asana_sem_token(self, mock_post, setup_test_env, monkeypatch):
        """Testa erro quando o token do Asana não está configurado."""
        monkeypatch.delenv("ASANA_TOKEN", raising=False)

        import importlib

        import src.platforms.asana

        importlib.reload(src.platforms.asana)
        from src.platforms.asana import criar_tarefa_asana

        result = criar_tarefa_asana("Tarefa sem token")
        assert "erro" in result
        assert "Token do Asana não configurado" in result["erro"]
        mock_post.assert_not_called()

    @patch("src.platforms.asana.requests.post")
    def test_criar_tarefa_asana_api_error(self, mock_post, setup_test_env):
        """Testa erro na requisição à API do Asana."""
        from requests.exceptions import Timeout

        mock_post.side_effect = Timeout("Tempo esgotado")

        result = criar_tarefa_asana("Tarefa com erro")
        assert "erro" in result
        assert "Erro ao criar tarefa" in result["erro"]

    @patch("src.platforms.asana.requests.get")
    def test_listar_tarefas_asana_success(self, mock_get, setup_test_env):
        """Testa listagem bem-sucedida de tarefas."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [{"gid": "1", "name": "Tarefa A"}, {"gid": "2", "name": "Tarefa B"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = listar_tarefas_asana()
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["name"] == "Tarefa A"

    @patch("src.platforms.asana.requests.get")
    def test_listar_tarefas_asana_sem_token(
        self, mock_get, setup_test_env, monkeypatch
    ):
        """Testa erro ao listar tarefas sem token."""
        monkeypatch.delenv("ASANA_TOKEN", raising=False)

        import importlib

        import src.platforms.asana

        importlib.reload(src.platforms.asana)
        from src.platforms.asana import listar_tarefas_asana

        result = listar_tarefas_asana()
        assert isinstance(result, list)
        assert len(result) == 1
        assert "erro" in result[0]
        mock_get.assert_not_called()


class TestAsanaAgent:
    def test_asana_agent_initialization(self, setup_test_env):
        """Verifica se o agente do Asana foi criado corretamente."""
        assert asana_agent.name == "AsanaAgent"
        assert len(asana_agent.tools) >= 2
