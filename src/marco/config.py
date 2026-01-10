"""Configuration management for Marco."""

import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # LLM Configuration
    llm_provider: Literal["openai", "anthropic", "ollama", "llamacpp"] = Field(
        default="ollama", description="LLM provider to use (ollama/llamacpp for local dev, openai/anthropic for production)"
    )
    openai_api_key: str | None = Field(
        default=None, description="OpenAI API key")
    anthropic_api_key: str | None = Field(
        default=None, description="Anthropic API key")
    openai_model: str = Field(
        default="gpt-4o", description="OpenAI model to use")
    anthropic_model: str = Field(
        default="claude-3-5-sonnet-20241022", description="Anthropic model to use"
    )
    ollama_model: str = Field(
        default="qwen3:4b", description="Ollama model to use"
    )
    ollama_base_url: str = Field(
        default="http://localhost:11434", description="Ollama base URL"
    )
    
    # llamacpp configuration (for local development with custom models)
    llamacpp_model_path: str = Field(
        default="./models/your-model.gguf", description="Path to GGUF model file for llamacpp (or use llamacpp_server_url for server mode)"
    )
    llamacpp_server_url: str = Field(
        default="http://localhost:8080", description="URL for llama.cpp server (alternative to model_path)"
    )
    llamacpp_max_tokens: int = Field(
        default=2048, description="Maximum tokens for llamacpp"
    )
    llamacpp_temperature: float = Field(
        default=0.7, description="Temperature for llamacpp"
    )
    llamacpp_n_ctx: int = Field(
        default=4096, description="Context window size for llamacpp"
    )

    # Database Configuration
    database_path: Path = Field(
        default_factory=lambda: Path.home() / ".marco" / "marco.db",
        description="Path to SQLite database",
    )

    # User Preferences
    default_region: str = Field(
        default="europe", description="Default geographic region")
    default_season: str = Field(
        default="auto", description="Default season (auto, winter, spring, summer, fall)")

    # Data Paths
    data_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent / "data",
        description="Path to data directory",
    )
    templates_dir: Path = Field(
        default_factory=lambda: Path(
            __file__).parent.parent.parent / "templates",
        description="Path to templates directory",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_api_key(self) -> str:
        """Get API key based on provider."""
        if self.llm_provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY not set in environment")
            return self.openai_api_key
        elif self.llm_provider == "anthropic":
            if not self.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY not set in environment")
            return self.anthropic_api_key
        elif self.llm_provider == "ollama":
            return "not-needed"  # Ollama doesn't require an API key
        elif self.llm_provider == "llamacpp":
            return "not-needed"  # llamacpp doesn't require an API key
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")

    def get_model_name(self) -> str:
        """Get model name based on provider."""
        if self.llm_provider == "openai":
            return self.openai_model
        elif self.llm_provider == "anthropic":
            return self.anthropic_model
        elif self.llm_provider == "ollama":
            return self.ollama_model
        elif self.llm_provider == "llamacpp":
            return self.llamacpp_model_path
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")

    def ensure_directories(self):
        """Ensure required directories exist."""
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
settings.ensure_directories()
