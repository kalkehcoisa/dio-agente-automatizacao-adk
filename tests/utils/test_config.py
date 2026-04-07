from src.utils.config import get_config


def test_get_config_returns_dict():
    config = get_config()
    assert isinstance(config, dict)
    assert "clickup" in config
    assert "plane" in config
    assert "wekan" in config
    assert "kanboard" in config


def test_config_keys_have_correct_structure():
    config = get_config()
    for platform in ["clickup", "plane", "wekan", "kanboard"]:
        assert isinstance(config[platform], dict)
