from typing import Any, Dict

from config_models import AppConfig


def load_config() -> AppConfig:
    import tomllib
    try:
        with open('config.toml', 'rb') as file:
            raw: Dict[str, Any] = tomllib.load(file)
            return AppConfig.model_validate(raw)
    except FileNotFoundError:
        raise FileNotFoundError("Config file 'config.toml' not found")
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Error parsing config file: {e}")

config = load_config()
