from typing import Any, Dict


def validate_config(config: Dict[str, Any]) -> None:
    """Validate that all required configuration items exist"""
    required_sections = ['employment_start_date', 'standard_pto', 'flexible_pto', 'schedule_file']
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required config section: {section}")

def load_config() -> Dict[str, Any]:
    import tomllib
    try:
        with open('config.toml', 'rb') as file:
            config = tomllib.load(file)
            validate_config(config)
            return config
    except FileNotFoundError:
        raise FileNotFoundError("Config file 'config.toml' not found")
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Error parsing config file: {e}")

config = load_config()
