# Marco 🍽️

AI-powered CLI tool for generating chef-quality healthy recipes with psychonutrition analysis for anxiety management.

## Features

- 🤖 **LangGraph Multi-Agent System**: Coordinated agents for recipe generation, nutritional analysis, and seasonal variations
- 🆓 **Free Local Development**: Uses Ollama with qwen3:4b or llamacpp with custom GGUF models - no API costs during development
- 🔄 **Easy Provider Switching**: Switch between Ollama, llamacpp (local), OpenAI, or Anthropic with one line
- 🧠 **Psychonutrition for Anxiety**: Recipes optimized with nutrients proven to reduce anxiety (omega-3, magnesium, tryptophan, B vitamins)
- 🌿 **Seasonal Intelligence**: Automatic ingredient substitutions based on seasonal availability and geography
- 📄 **Beautiful PDF Export**: Generate professional recipe cards with styling and nutritional information
- 👤 **User Profiles**: Track dietary restrictions, anxiety symptoms, and recipe history

## Installation

### Using uv (recommended - faster ⚡️)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv and install
uv venv
source .venv/bin/activate  # On macOS/Linux
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

> **Note**: UV is 10-100x faster than pip! See [UV_GUIDE.md](UV_GUIDE.md) for details.

## Configuration

### Development (Free, Local)

Marco supports multiple local options for development - no API key needed!

**Option 1: Ollama (Easiest)**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model
ollama pull qwen3:4b

# Create .env (already configured for Ollama!)
cp .env.example .env
```

**Option 2: llamacpp (Custom Models)**
```bash
# Download a GGUF model
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf

# Configure .env
LLM_PROVIDER=llamacpp
LLAMACPP_MODEL_PATH=/path/to/llama-2-7b-chat.Q4_K_M.gguf
```

### Production (Cloud APIs)

For production, switch to OpenAI or Anthropic:

```bash
# Edit .env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
```

See [OLLAMA_GUIDE.md](OLLAMA_GUIDE.md) and [LLAMACPP_GUIDE.md](LLAMACPP_GUIDE.md) for detailed setup.

## Usage

### Generate a Recipe

```bash
marco generate "salmon with vegetables" --anxiety-focus
```

### Generate Seasonal Variations

```bash
marco variations "mediterranean salad" --season winter --region europe
```

### Export to PDF

```bash
marco export-pdf recipe.json --output recipe.pdf
```

### Interactive Mode

```bash
marco interactive
```

## Architecture

- **LangGraph StateGraph**: Orchestrates multi-agent workflow
- **Recipe Generator Agent**: Creates chef-quality recipes with LLM
- **Psychonutrition Agent**: Analyzes and optimizes nutritional content for anxiety
- **Seasonal Agent**: Suggests ingredient substitutions based on season
- **PDF Generator**: Creates beautiful recipe cards using WeasyPrint

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
