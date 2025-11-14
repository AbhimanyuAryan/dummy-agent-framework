"""
Configuration loader for Gemini Agent.

Supports YAML configuration files for easy agent setup.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to YAML config file
    
    Returns:
        Configuration dictionary
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config or {}


def get_agent_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract agent configuration from config dict.
    
    Args:
        config: Full configuration dictionary
    
    Returns:
        Agent configuration
    """
    agent_config = config.get('agent', {})
    
    # Extract backend config
    backend_config = agent_config.get('backend', {})
    
    return {
        'model': backend_config.get('model', 'gemini-2.0-flash-exp'),
        'system_message': agent_config.get('system_message', 'You are a helpful AI assistant.'),
        'enable_code_execution': backend_config.get('enable_code_execution', False),
        'enable_web_search': backend_config.get('enable_web_search', False),
        'temperature': backend_config.get('temperature'),
        'max_tokens': backend_config.get('max_tokens'),
    }


def get_ui_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract UI configuration from config dict.
    
    Args:
        config: Full configuration dictionary
    
    Returns:
        UI configuration
    """
    return config.get('ui', {
        'display_type': 'rich_terminal',
        'logging_enabled': True,
    })
