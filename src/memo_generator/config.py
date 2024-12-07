"""Configuration management for the Investment Memo Generator."""

import os
from pathlib import Path
from typing import Dict, Any

import yaml

class Config:
    """Handles configuration loading and management."""
    
    def __init__(self, config_path: str = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to configuration file. If None, uses default.
        """
        self.config_path = config_path or self._get_default_config()
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def _get_default_config(self) -> str:
        """Get path to default config file."""
        root_dir = Path(__file__).parent.parent.parent
        return str(root_dir / "config" / "default_config.yml")
    
    def load_config(self) -> None:
        """Load configuration from file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
            
        with open(self.config_path, "r") as f:
            self.config = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key to retrieve
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
        
    def __getitem__(self, key: str) -> Any:
        """Get configuration value using dictionary syntax."""
        return self.config[key]