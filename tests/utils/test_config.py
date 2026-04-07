from src.utils.config import get_config


def test_get_config_returns_dict():
    config = get_config()
    assert isinstance(config, dict)
    for platform in ["asana", "clickup", "freedcamp", "trello"]:
        assert platform in config


def test_config_keys_have_correct_structure():
    config = get_config()
    for platform in ["asana", "clickup", "freedcamp", "trello"]:
        assert isinstance(config[platform], dict)
