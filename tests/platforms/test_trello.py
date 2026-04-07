from unittest.mock import MagicMock, patch

import pytest
from src.platforms.trello import criar_card_trello, listar_cards_trello, trello_agent


class TestTrelloTools:
    @patch("src.platforms.trello.requests.post")
    def test_criar_card_trello_success(self, mock_post, setup_test_env):
        """Testa criação bem-sucedida de card no Trello."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "card_123", "name": "Meu Card"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = criar_card_trello("Meu Card", "Descrição do card")
        assert result["id"] == "card_123"
        assert result["name"] == "Meu Card"
        mock_post.assert_called_once()

    @patch("src.platforms.trello.requests.post")
    def test_criar_card_trello_sem_credenciais(
        self, mock_post, setup_test_env, monkeypatch
    ):
        """Testa erro quando API Key ou Token não estão configurados."""
        monkeypatch.delenv("TRELLO_API_KEY", raising=False)

        # Recarrega o módulo para forçar a leitura das novas variáveis
        import importlib

        import src.platforms.trello

        importlib.reload(src.platforms.trello)
        from src.platforms.trello import criar_card_trello

        result = criar_card_trello("Card sem credenciais")
        assert "erro" in result
        assert "API Key ou Token do Trello não configurados" in result["erro"]
        mock_post.assert_not_called()

    @patch("src.platforms.trello.requests.post")
    def test_criar_card_trello_api_error(self, mock_post, setup_test_env):
        """Testa erro na requisição à API do Trello."""
        from requests.exceptions import ConnectionError

        mock_post.side_effect = ConnectionError("Falha na conexão")

        result = criar_card_trello("Card com erro")
        assert "erro" in result
        assert "Erro ao criar card" in result["erro"]

    @patch("src.platforms.trello.requests.get")
    def test_listar_cards_trello_success(self, mock_get, setup_test_env):
        """Testa listagem bem-sucedida de cards."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"id": "1", "name": "Card A"},
            {"id": "2", "name": "Card B"},
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = listar_cards_trello()
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["name"] == "Card A"

    @patch("src.platforms.trello.requests.get")
    def test_listar_cards_trello_sem_credenciais(
        self, mock_get, setup_test_env, monkeypatch
    ):
        """Testa erro ao listar cards sem credenciais."""
        monkeypatch.delenv("TRELLO_API_KEY", raising=False)

        import importlib

        import src.platforms.trello

        importlib.reload(src.platforms.trello)
        from src.platforms.trello import listar_cards_trello

        result = listar_cards_trello()
        assert isinstance(result, list)
        assert len(result) == 1
        assert "erro" in result[0]
        mock_get.assert_not_called()


class TestTrelloAgent:
    def test_trello_agent_initialization(self, setup_test_env):
        """Verifica se o agente do Trello foi criado corretamente."""
        assert trello_agent.name == "TrelloAgent"
        assert len(trello_agent.tools) >= 2
