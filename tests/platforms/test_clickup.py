from unittest.mock import MagicMock, patch

from src.platforms.clickup import criar_tarefa_clickup, listar_tarefas_clickup


class TestClickUpTools:
    @patch("src.platforms.clickup.requests.post")
    def test_criar_tarefa_clickup_success(self, mock_post, setup_test_env):
        """Testa criação bem-sucedida de tarefa no ClickUp."""
        mock_post.return_value.json.return_value = {"id": "123", "name": "Nova Tarefa"}
        mock_post.return_value.status_code = 200

        result = criar_tarefa_clickup("Nova Tarefa", "Descrição detalhada")
        assert result["id"] == "123"
        assert result["name"] == "Nova Tarefa"
        mock_post.assert_called_once()

    @patch("src.platforms.clickup.requests.post")
    def test_criar_tarefa_clickup_sem_token(
        self, mock_post, setup_test_env, monkeypatch
    ):
        """Testa erro quando o token não está configurado."""
        monkeypatch.delenv("CLICKUP_API_TOKEN", raising=False)
        from src.platforms.clickup import criar_tarefa_clickup

        result = criar_tarefa_clickup("Tarefa sem token")
        assert "erro" in result
        assert "Token do ClickUp não configurado" in result["erro"]
        mock_post.assert_not_called()

    @patch("src.platforms.clickup.requests.get")
    def test_listar_tarefas_clickup(self, mock_get, setup_test_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tasks": [{"id": "1", "name": "Tarefa A"}, {"id": "2", "name": "Tarefa B"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = listar_tarefas_clickup()
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["name"] == "Tarefa A"

    def test_clickup_agent_tools_count(self, setup_test_env):
        """Verifica que o agente ClickUp possui as ferramentas corretas."""
        from src.platforms.clickup import clickup_agent

        assert clickup_agent.name == "ClickUpAgent"
        assert len(clickup_agent.tools) >= 2
