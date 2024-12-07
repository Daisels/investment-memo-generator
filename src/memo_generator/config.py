from pathlib import Path
from typing import Dict, Any, Optional
import yaml

class Config:
    """Configuration manager for the Investment Memo Generator."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path("config/default_config.yml")
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path) as f:
            self.config = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        return self.config.get(key, default)

    @property
    def llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration."""
        return self.config.get("llm", {})
    
    @property
    def template_config(self) -> Dict[str, Any]:
        """Get template configuration."""
        return self.config.get("template", {})