.PHONY: install init clean test format lint help venv check-uv

help: ## Show this help message
	@echo "Marco - Development Commands (using UV ⚡️)"
	@echo ""
	@echo "Quick start: make setup"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode (using uv)
	uv pip install -e .

install-dev: ## Install with development dependencies (using uv)
	uv pip install -e ".[dev]"

init: ## Initialize Marco (database and config check)
	uv run python -m marco init

clean: ## Clean up generated files and caches
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf build/ dist/ *.egg-info
	rm -f *.pdf example_recipe.pdf

test: ## Run tests (when available)
	uv run pytest tests/ -v

format: ## Format code with black
	uv run black src/marco/

lint: ## Lint code with ruff
	uv run ruff check src/marco/

example: ## Run example script
	uv run python examples.py

generate: ## Quick test: generate a recipe
	uv run python -m marco generate "grilled salmon with vegetables" --anxiety-focus

recipe-pdf: ## Generate a recipe and export to PDF
	uv run python -m marco generate "mediterranean quinoa bowl" --anxiety-focus --pdf test_recipe.pdf

interactive: ## Start interactive mode
	uv run python -m marco interactive

# Development helpers
venv: ## Create virtual environment with uv
	uv venv
	@echo "Activate with: source .venv/bin/activate"

check-ollama: ## Check if Ollama is running and model is available
	@command -v ollama >/dev/null 2>&1 || (echo "✗ Ollama not installed. Run: curl -fsSL https://ollama.com/install.sh | sh" && exit 1)
	@curl -s http://localhost:11434/api/tags >/dev/null 2>&1 || (echo "✗ Ollama not running. Run: ollama serve" && exit 1)
	@ollama list | grep -q qwen3:4b && echo "✓ Ollama is running with qwen3:4b model" || echo "⚠ qwen3:4b not found. Run: ollama pull qwen3:4b"

check-llamacpp: ## Check if llamacpp server is running
	@curl -s http://localhost:8080/health >/dev/null 2>&1 && echo "✓ llamacpp server is running on port 8080" || echo "✗ llamacpp server not running. Run: make start-llamacpp"

check-deps: ## Check if dependencies are installed
	@python -c "import langgraph, langchain, typer, pydantic, weasyprint, jinja2" && echo "✓ All dependencies installed" || echo "✗ Missing dependencies - run 'make install'"

check-uv: ## Check if uv is installed
	@command -v uv >/dev/null 2>&1 && echo "✓ uv is installed" || (echo "✗ uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh" && exit 1)

setup: check-uv venv install check-ollama init ## Complete setup (uv + venv + install + ollama + init)
	@echo ""
	@echo "✓ Marco is ready!"
	@echo ""
	@echo "Activate venv: source .venv/bin/activate"
	@echo "Try: make generate"
	@echo "Or:  marco generate 'your recipe idea'"

start-llamacpp: ## Start a local LlamaCpp server (example command)
	llama-server -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q4_K_M -ngl 80 --port 8080

.DEFAULT_GOAL := help
