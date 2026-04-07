import importlib

import pytest


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Define variáveis de ambiente falsas e recarrega todos os módulos das plataformas."""
    monkeypatch.setenv("CLICKUP_API_TOKEN", "fake_clickup_token_123")
    monkeypatch.setenv("CLICKUP_LIST_ID", "fake_list_id_456")

    monkeypatch.setenv("PLANE_API_TOKEN", "fake_plane_token_789")
    monkeypatch.setenv("PLANE_BASE_URL", "https://fake.plane.so/api")

    monkeypatch.setenv("WEKAN_API_URL", "http://fake-wekan:8080/api")
    monkeypatch.setenv("WEKAN_USER_ID", "fake_user_abc")
    monkeypatch.setenv("WEKAN_API_TOKEN", "fake_wekan_token_def")

    monkeypatch.setenv("KANBOARD_API_URL", "http://fake-kanboard:8000/api")
    monkeypatch.setenv("KANBOARD_USERNAME", "admin")
    monkeypatch.setenv("KANBOARD_PASSWORD", "admin")

    yield
