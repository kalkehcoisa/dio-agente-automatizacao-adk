from unittest.mock import MagicMock, patch

import pytest
from src.platforms.freedcamp import (
    criar_tarefa_freedcamp,
    freedcamp_agent,
    listar_tarefas_freedcamp,
)


class TestFreedcampTools:
    @patch("src.platforms.freedcamp.requests.post")
    def test_criar_tarefa_freedcamp_success(self, mock_post, setup_test_env):
        """Testa criação bem-sucedida de tarefa no Freedcamp."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "task_123", "title": "Minha Tarefa"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = criar_tarefa_freedcamp("Minha Tarefa", "Descrição da tarefa")
        assert result["id"] == "task_123"
        assert result["title"] == "Minha Tarefa"
        mock_post.assert_called_once()

    @patch("src.platforms.freedcamp.requests.post")
    def test_criar_tarefa_freedcamp_sem_api_key(
        self, mock_post, setup_test_env, monkeypatch
    ):
        """Testa erro quando a API Key do Freedcamp não está configurada."""
        monkeypatch.delenv("FREEDCAMP_API_KEY", raising=False)

        import importlib

        import src.platforms.freedcamp

        importlib.reload(src.platforms.freedcamp)
        from src.platforms.freedcamp import criar_tarefa_freedcamp

        result = criar_tarefa_freedcamp("Tarefa sem API Key")
        assert "erro" in result
        assert "API Key do Freedcamp não configurada" in result["erro"]
        mock_post.assert_not_called()

    @patch("src.platforms.freedcamp.requests.post")
    def test_criar_tarefa_freedcamp_api_error(self, mock_post, setup_test_env):
        """Testa erro na requisição à API do Freedcamp."""
        from requests.exceptions import HTTPError

        mock_post.side_effect = HTTPError("Erro 500")

        result = criar_tarefa_freedcamp("Tarefa com erro")
        assert "erro" in result
        assert "Erro ao criar tarefa" in result["erro"]

    @patch("src.platforms.freedcamp.requests.get")
    def test_listar_tarefas_freedcamp_success(self, mock_get, setup_test_env):
        """Testa listagem bem-sucedida de tarefas."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tasks": [
                {"id": "1", "title": "Tarefa A"},
                {"id": "2", "title": "Tarefa B"},
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = listar_tarefas_freedcamp()
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["title"] == "Tarefa A"

    @patch("src.platforms.freedcamp.requests.get")
    def test_listar_tarefas_freedcamp_sem_api_key(
        self, mock_get, setup_test_env, monkeypatch
    ):
        """Testa erro ao listar tarefas sem API Key."""
        monkeypatch.delenv("FREEDCAMP_API_KEY", raising=False)

        import importlib

        import src.platforms.freedcamp

        importlib.reload(src.platforms.freedcamp)
        from src.platforms.freedcamp import listar_tarefas_freedcamp

        result = listar_tarefas_freedcamp()
        assert isinstance(result, list)
        assert len(result) == 1
        assert "erro" in result[0]
        mock_get.assert_not_called()


class TestFreedcampAgent:
    def test_freedcamp_agent_initialization(self, setup_test_env):
        """Verifica se o agente do Freedcamp foi criado corretamente."""
        assert freedcamp_agent.name == "FreedcampAgent"
        assert len(freedcamp_agent.tools) >= 2
