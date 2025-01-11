from typing import Any, Dict

import yaml


def validate_config(config: Dict[str, Any]) -> None:
    """Validate that all required configuration items exist"""
    required_sections = ['employment_start_date', 'standard_pto', 'flexible_pto']
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required config section: {section}")
    
def load_config() -> Dict[str, Any]:
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            validate_config(config)
            return config
    except FileNotFoundError:
        raise FileNotFoundError("Config file 'config.yaml' not found")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing config file: {e}")

config = load_config()