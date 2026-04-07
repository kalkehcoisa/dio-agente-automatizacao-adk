from unittest.mock import patch

import pytest
from src.platforms.wekan import criar_card_wekan


class TestWekanTools:
    @patch("src.platforms.wekan.requests.post")
    def test_criar_card_wekan_success(self, mock_post, setup_test_env):
        """Testa criação bem-sucedida de card no Wekan."""
        mock_post.return_value.json.return_value = {
            "_id": "card_456",
            "title": "Meu Card",
        }
        mock_post.return_value.status_code = 200

        result = criar_card_wekan("board_1", "list_2", "Meu Card")
        assert result["_id"] == "card_456"
        assert result["title"] == "Meu Card"
        mock_post.assert_called_once()

    @patch("src.platforms.wekan.requests.post")
    def test_criar_card_wekan_configuracao_incompleta(
        self, mock_post, setup_test_env, monkeypatch
    ):
        """Testa erro quando a configuração do Wekan está incompleta."""
        monkeypatch.delenv("WEKAN_API_URL", raising=False)
        from src.platforms.wekan import criar_card_wekan

        result = criar_card_wekan("board", "list", "Card")
        assert "erro" in result
        assert "Configuração do Wekan incompleta" in result["erro"]
        mock_post.assert_not_called()

    @patch("src.platforms.wekan.requests.post")
    def test_criar_card_wekan_falha_http(self, mock_post, setup_test_env):
        """Testa falha HTTP (ex: 401 Unauthorized)."""
        mock_post.return_value.status_code = 401
        mock_post.return_value.json.return_value = {"error": "Unauthorized"}

        result = criar_card_wekan("board", "list", "Card")
        # A função retorna o JSON da resposta, que contém 'error'
        assert "error" in result or result.get("status_code") == 401

    def test_wekan_agent_initialization(self, setup_test_env):
        from src.platforms.wekan import wekan_agent

        assert wekan_agent.name == "WekanAgent"
        assert len(wekan_agent.tools) >= 1
