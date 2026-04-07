from unittest.mock import patch

import pytest
from src.platforms.plane import criar_tarefa_plane


class TestPlaneTools:
    @patch("src.platforms.plane.requests.post")
    def test_criar_tarefa_plane_success(self, mock_post, setup_test_env):
        """Testa criação bem-sucedida de issue no Plane."""
        mock_post.return_value.json.return_value = {"id": "issue_123", "title": "Teste"}
        mock_post.return_value.status_code = 201

        result = criar_tarefa_plane("proj_xyz", "Nova Issue", "Descrição detalhada")
        assert result["id"] == "issue_123"
        assert result["title"] == "Teste"
        mock_post.assert_called_once()

    @patch("src.platforms.plane.requests.post")
    def test_criar_tarefa_plane_sem_token(self, mock_post, setup_test_env, monkeypatch):
        """Testa erro quando o token do Plane não está configurado."""
        monkeypatch.delenv("PLANE_API_TOKEN", raising=False)
        from src.platforms.plane import criar_tarefa_plane

        result = criar_tarefa_plane("proj", "Tarefa sem token")
        assert "erro" in result
        assert "Token do Plane não configurado" in result["erro"]
        mock_post.assert_not_called()

    @patch("src.platforms.plane.requests.post")
    def test_criar_tarefa_plane_api_error(self, mock_post, setup_test_env):
        """Testa comportamento quando a API retorna erro."""
        mock_post.side_effect = Exception("Conexão recusada")
        result = criar_tarefa_plane("proj", "Falha")
        # A função pode retornar um erro ou propagar a exceção; aqui esperamos um dict com erro
        assert "erro" in result or "Exception" in str(result)

    def test_plane_agent_initialization(self, setup_test_env):
        from src.platforms.plane import plane_agent

        assert plane_agent.name == "PlaneAgent"
        assert len(plane_agent.tools) >= 1
