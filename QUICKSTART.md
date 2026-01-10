# Marco Quick Start Guide

## Installation

1. **Clone/Navigate to the project directory:**
   ```bash
   cd /Users/guillaume.bailleul/perso/marco
   ```

2. **Install uv (if not already installed):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create a virtual environment and install:**
   ```bash
   # uv automatically creates and manages the virtual environment
   uv venv
   source .venv/bin/activate  # On macOS/Linux
   uv pip install -e .
   ```

   **Alternative with pip:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

4. **Set up LLM (choose one):**

   **Option A: Ollama (Recommended for Dev - Free & Local)**
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull model
   ollama pull qwen3:4b
   
   # Config is already set for Ollama!
   cp .env.example .env
   ```

   **Option B: llamacpp (Custom GGUF Models - Free & Local)**
   ```bash
   # Download a GGUF model (example)
   mkdir -p ./models
   wget -O ./models/llama2-7b.gguf https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
   
   # Configure
   cp .env.example .env
   # Edit .env:
   # LLM_PROVIDER=llamacpp
   # LLAMACPP_MODEL_PATH=./models/llama2-7b.gguf
   ```

   **Option C: OpenAI or Anthropic (Production)**
   ```bash
   cp .env.example .env
   # Edit .env:
   # LLM_PROVIDER=openai
   # OPENAI_API_KEY=your_key_here
   ```

5. **Initialize the database:**
   ```bash
   marco init
   ```

## Usage Examples

### Generate a Recipe

```bash
# Basic recipe generation
marco generate "grilled salmon with asparagus"

# With options
marco generate "chicken stir fry" --season summer --region europe --output recipe.json

# Without anxiety focus
marco generate "pasta carbonara" --no-anxiety-focus

# With dietary restrictions
marco generate "buddha bowl" --restrictions "vegan,gluten-free"
```

### Generate Seasonal Variations

```bash
# First, generate and save a recipe
marco generate "mediterranean salad" --output salad.json

# Then create seasonal variations
marco variations salad.json --season winter --region europe
```

### Export to PDF

```bash
# Generate recipe with PDF export
marco generate "quinoa bowl" --pdf quinoa.pdf

# Or export existing recipe
marco export-pdf recipe.json --output beautiful_recipe.pdf
```

### Interactive Mode

```bash
marco interactive
```

## Project Structure

```
marco/
├── src/marco/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # CLI entry point
│   ├── cli.py               # Typer CLI commands
│   ├── config.py            # Configuration management
│   ├── schemas.py           # Pydantic data models
│   ├── graph.py             # LangGraph workflow
│   ├── db.py                # SQLite database layer
│   ├── pdf.py               # PDF generation
│   └── agents/
│       ├── __init__.py
│       ├── recipe_generator.py   # Recipe generation agent
│       ├── psychonutrition.py    # Psychonutrition analysis
│       └── seasonal.py           # Seasonal optimization
├── data/
│   ├── nutrients.json            # Psychonutrition knowledge base
│   └── seasonal_ingredients.json # Seasonal ingredient database
├── templates/
│   ├── recipe.html               # PDF template
│   └── style.css                 # PDF styling
├── pyproject.toml               # Project configuration
├── langgraph.json              # LangGraph configuration
└── README.md                   # Documentation
```

## How It Works

### LangGraph Workflow

1. **Recipe Generator Agent**: Creates chef-quality recipe using LLM with structured output
2. **Psychonutrition Agent**: Analyzes ingredients for anxiety-reducing nutrients
3. **Seasonal Agent**: Suggests seasonal ingredient substitutions

### Key Features

- **Multi-Agent System**: Uses LangGraph's StateGraph for coordinated agents
- **Structured Output**: Pydantic schemas ensure consistent recipe format
- **Psychonutrition Database**: Evidence-based nutrients for anxiety management
- **Seasonal Intelligence**: Automatic substitutions based on availability
- **Beautiful PDFs**: Professional recipe cards with WeasyPrint + CSS

## Troubleshooting

### "No API key found"
Make sure you've created a `.env` file and added your API key.

### Import errors
Make sure you've installed the package: `uv pip install -e .` or `pip install -e .`

### WeasyPrint installation issues (macOS)
You may need system dependencies:
```bash
brew install pango libffi
```

### Database not found
Run `marco init` to initialize the database.

## Development

### Run tests (when available)
```bash
pytest
```

### Format code
```bash
black src/
```

### Lint code
```bash
ruff check src/
```

## Next Steps

1. Try generating your first recipe: `marco generate "salmon with vegetables"`
2. Experiment with different cuisines and dietary restrictions
3. Generate seasonal variations for your favorite recipes
4. Export beautiful PDFs to share with friends!

Enjoy cooking with Marco! 🍽️
