from pathlib import Path
from typing import Dict, Any
import yaml
from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuration for Claude API."""
    api_key: str
    model: str = "claude-3-sonnet-20240229"
    temperature: float = 0.7
    max_tokens: int = 4096

@dataclass
class VectorDBConfig:
    """Configuration for vector database."""
    provider: str = "chroma"  # or other vector DB providers
    persist_directory: str = "data/vectordb"
    collection_name: str = "investment_docs"

@dataclass
class ProcessingConfig:
    """Configuration for document processing."""
    chunk_size: int = 1000
    chunk_overlap: int = 200
    supported_languages: list = None
    input_directory: str = "data/input"
    output_directory: str = "data/output"
    temp_directory: str = "data/temp"

    def __post_init__(self):
        if self.supported_languages is None:
            self.supported_languages = ["en", "nl"]  # English and Dutch

class Config:
    """Main configuration class."""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._get_default_config()
        self.llm: LLMConfig = None
        self.vector_db: VectorDBConfig = None
        self.processing: ProcessingConfig = None
        self.load_config()
        self._ensure_directories()

    def _get_default_config(self) -> str:
        """Get path to default config file."""
        return str(Path(__file__).parent / "config.yml")

    def load_config(self) -> None:
        """Load configuration from YAML file."""
        if not Path(self.config_path).exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
            
        with open(self.config_path, "r") as f:
            config_data = yaml.safe_load(f)

        self.llm = LLMConfig(**config_data.get("llm", {}))
        self.vector_db = VectorDBConfig(**config_data.get("vector_db", {}))
        self.processing = ProcessingConfig(**config_data.get("processing", {}))

    def _ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            self.processing.input_directory,
            self.processing.output_directory,
            self.processing.temp_directory,
            self.vector_db.persist_directory
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)