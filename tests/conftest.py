import pytest


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Define variáveis de ambiente falsas para todos os testes."""
    monkeypatch.setenv("CLICKUP_API_TOKEN", "fake_clickup_token")
    monkeypatch.setenv("CLICKUP_LIST_ID", "fake_list_id")

    monkeypatch.setenv("TRELLO_API_KEY", "fake_trello_api_key")
    monkeypatch.setenv("TRELLO_TOKEN", "fake_trello_token")
    monkeypatch.setenv("TRELLO_BOARD_ID", "fake_board_id")
    monkeypatch.setenv("TRELLO_DEFAULT_LIST_ID", "fake_list_id")

    monkeypatch.setenv("ASANA_TOKEN", "fake_asana_token")
    monkeypatch.setenv("ASANA_DEFAULT_PROJECT_ID", "fake_project_id")

    monkeypatch.setenv("FREEDCAMP_API_KEY", "fake_freedcamp_api_key")
    monkeypatch.setenv("FREEDCAMP_DEFAULT_PROJECT_ID", "fake_project_id")

    yield
