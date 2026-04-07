from unittest.mock import patch

import pytest
from src.platforms.kanboard import criar_tarefa_kanboard


class TestKanboardTools:
    @patch("src.platforms.kanboard.requests.post")
    def test_criar_tarefa_kanboard_success(self, mock_post, setup_test_env):
        """Testa criação bem-sucedida de tarefa no Kanboard via JSON-RPC."""
        mock_post.return_value.json.return_value = {
            "jsonrpc": "2.0",
            "result": 42,
            "id": 1,
        }
        mock_post.return_value.status_code = 200

        result = criar_tarefa_kanboard(1, "Tarefa Kanboard")
        assert result["result"] == 42
        mock_post.assert_called_once()
        # Verifica o payload JSON-RPC
        args, kwargs = mock_post.call_args
        payload = kwargs["json"]
        assert payload["method"] == "createTask"
        assert payload["params"]["title"] == "Tarefa Kanboard"
        assert payload["params"]["project_id"] == 1

    @patch("src.platforms.kanboard.requests.post")
    def test_criar_tarefa_kanboard_sem_url(
        self, mock_post, setup_test_env, monkeypatch
    ):
        """Testa erro quando a URL da API não está configurada."""
        monkeypatch.delenv("KANBOARD_API_URL", raising=False)
        from src.platforms.kanboard import criar_tarefa_kanboard

        result = criar_tarefa_kanboard(1, "Tarefa")
        assert "erro" in result
        assert "Kanboard não configurado" in result["erro"]
        mock_post.assert_not_called()

    @patch("src.platforms.kanboard.requests.post")
    def test_criar_tarefa_kanboard_erro_jsonrpc(self, mock_post, setup_test_env):
        """Testa erro retornado pelo JSON-RPC (ex: método não encontrado)."""
        mock_post.return_value.json.return_value = {
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Method not found"},
            "id": 1,
        }
        result = criar_tarefa_kanboard(99, "Método inválido")
        assert "error" in result
        assert result["error"]["code"] == -32601

    def test_kanboard_agent_initialization(self, setup_test_env):
        from src.platforms.kanboard import kanboard_agent

        assert kanboard_agent.name == "KanboardAgent"
        assert len(kanboard_agent.tools) >= 1
