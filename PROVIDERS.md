# Provider Switching Guide

Quick reference for switching between LLM providers in Marco.

## Current Setup

Marco supports **4 LLM providers**:

| Provider | Use Case | Cost | Setup |
|----------|----------|------|---------|
| **Ollama** (default) | Development, testing | Free | Local install |
| **llamacpp** | Local custom models | Free | GGUF model file |
| **OpenAI** | Production, best quality | ~$0.01/recipe | API key |
| **Anthropic** | Production, alternative | ~$0.02/recipe | API key |

## Quick Switch Commands

### View Current Provider

```bash
# Check your .env file
cat .env | grep LLM_PROVIDER
```

### Switch to Ollama (Local, Free)

```bash
# Edit .env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:4b
OLLAMA_BASE_URL=http://localhost:11434

# Make sure Ollama is running
ollama serve
ollama pull qwen2.5:4b
```

### Switch to llamacpp (Local Custom Models)

```bash
# Edit .env
LLM_PROVIDER=llamacpp
LLAMACPP_MODEL_PATH=/path/to/your/model.gguf
LLAMACPP_MAX_TOKENS=2048
LLAMACPP_TEMPERATURE=0.7
LLAMACPP_N_CTX=4096

# Download a GGUF model (example)
# From HuggingFace or other sources
```

## Setting Up llamacpp

### Step 1: Install Dependencies

llamacpp support is included when you install Marco with langchain-community:

```bash
uv pip install -e .
# or
pip install -e .
```

### Step 2: Download a GGUF Model

Popular options:

```bash
# Option 1: Download from HuggingFace
# Visit https://huggingface.co/TheBloke and download a GGUF model
# Example: Llama 2 7B Chat GGUF
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf

# Option 2: Use a smaller model for testing
wget https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/pytorch_model.bin

# Option 3: Convert your own model to GGUF format
# (Advanced - requires llama.cpp tools)
```

### Step 3: Configure Marco

```bash
# Create/edit .env
LLM_PROVIDER=llamacpp
LLAMACPP_MODEL_PATH=./models/llama-2-7b-chat.Q4_K_M.gguf
LLAMACPP_MAX_TOKENS=2048
LLAMACPP_TEMPERATURE=0.7
LLAMACPP_N_CTX=4096
```

### Step 4: Test Setup

```bash
# Test with Marco
marco generate "simple pasta recipe" --anxiety-focus

# If you get import errors, install additional dependencies:
pip install llama-cpp-python
```

### llamacpp Configuration Options

```bash
# Model file path (required)
LLAMACPP_MODEL_PATH=/path/to/model.gguf

# Maximum output tokens
LLAMACPP_MAX_TOKENS=2048

# Creativity level (0.0 = deterministic, 1.0 = very creative)
LLAMACPP_TEMPERATURE=0.7

# Context window size (how much text the model remembers)
LLAMACPP_N_CTX=4096
```

**Recommended GGUF Models for Recipe Generation:**
- **Llama 2 7B Chat Q4_K_M** - Good balance of size and quality
- **Mistral 7B Q4_K_M** - Excellent instruction following
- **Code Llama 7B Instruct Q4_K_M** - Good for structured output
- **Zephyr 7B Q4_K_M** - Fine-tuned for chat

### Switch to OpenAI

```bash
# Edit .env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
```

### Switch to llamacpp (Local Custom Models)

```bash
# Edit .env
LLM_PROVIDER=llamacpp
LLAMACPP_MODEL_PATH=/path/to/your/model.gguf
LLAMACPP_MAX_TOKENS=2048
LLAMACPP_TEMPERATURE=0.7
LLAMACPP_N_CTX=4096
```

### Switch to Anthropic

```bash
# Edit .env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

## One-Time Override

Test different providers without changing `.env`:

```bash
# Try with Ollama
LLM_PROVIDER=ollama marco generate "pasta recipe"

# Try with llamacpp
LLM_PROVIDER=llamacpp marco generate "pasta recipe"

# Try with OpenAI
LLM_PROVIDER=openai marco generate "pasta recipe"

# Try with Anthropic
LLM_PROVIDER=anthropic marco generate "pasta recipe"
```

## Recommended Workflow

### Development Phase
```bash
# .env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:4b
```

**Why?**
- ✅ Free unlimited requests
- ✅ Fast iteration
- ✅ No internet needed
- ✅ Privacy (local only)

### Testing Phase
```bash
# .env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:7b  # Better quality
```

**Why?**
- ✅ Still free
- ✅ Better quality for testing
- ✅ Closer to production output

### Pre-Production
```bash
# Test with actual production model
LLM_PROVIDER=openai marco generate "test recipe"
```

**Why?**
- ✅ Verify quality with production model
- ✅ Test API integration
- ✅ Minimal cost (few requests)

### Production
```bash
# .env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o
```

**Why?**
- ✅ Best quality
- ✅ Reliable
- ✅ Fast responses

## Model Comparison

### Ollama Models (Local)

```bash
# Fast & Small (Development)
OLLAMA_MODEL=qwen2.5:4b      # 2.5GB, very fast
OLLAMA_MODEL=phi3:mini        # 3.8GB, fast

# Balanced (Testing)
OLLAMA_MODEL=qwen2.5:7b      # 5GB, good quality
OLLAMA_MODEL=llama3.2:8b     # 8GB, good quality

# High Quality (Pre-prod)
OLLAMA_MODEL=qwen2.5:14b     # 14GB, excellent
OLLAMA_MODEL=llama3.1:13b    # 13GB, excellent
```

### llamacpp Models (Local GGUF)

You can use any GGUF model file with llamacpp. Popular sources:

```bash
# Download GGUF models from HuggingFace
# Example paths (adjust to your setup):
LLAMACPP_MODEL_PATH=/path/to/models/llama-2-7b-chat.Q4_K_M.gguf
LLAMACPP_MODEL_PATH=./models/codellama-7b-instruct.Q4_K_M.gguf
LLAMACPP_MODEL_PATH=/home/user/models/mistral-7b-v0.1.Q4_K_M.gguf

# Configuration examples:
LLAMACPP_N_CTX=4096          # Context window
LLAMACPP_MAX_TOKENS=2048     # Max output tokens
LLAMACPP_TEMPERATURE=0.7     # Creativity level
```

**Popular GGUF model sources:**
- [TheBloke's models](https://huggingface.co/TheBloke) on HuggingFace
- [Llama 2 GGUF](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF)
- [Code Llama GGUF](https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF)
- [Mistral GGUF](https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF)

### OpenAI Models

```bash
OPENAI_MODEL=gpt-4o          # Best, ~$0.01/recipe
OPENAI_MODEL=gpt-4o-mini     # Cheaper, ~$0.001/recipe
```

### Anthropic Models

```bash
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # Best, ~$0.02/recipe
ANTHROPIC_MODEL=claude-3-haiku-20240307     # Cheaper, ~$0.001/recipe
```

## Configuration Files

### Full .env Example

```bash
# === DEVELOPMENT (Default) ===
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:4b
OLLAMA_BASE_URL=http://localhost:11434

# === PRODUCTION (Commented out) ===
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-proj-your-key-here
# OPENAI_MODEL=gpt-4o

# === ALTERNATIVE (Commented out) ===
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# === OTHER SETTINGS ===
DATABASE_PATH=~/.marco/marco.db
DEFAULT_REGION=europe
DEFAULT_SEASON=auto
```

## Troubleshooting

### Ollama not working?

```bash
# Check Ollama is installed
ollama --version

# Check Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Check model is downloaded
ollama list

# Pull model if missing
ollama pull qwen2.5:4b
```

### llamacpp not working?

```bash
# Check if model file exists
ls -la /path/to/your/model.gguf

# Verify model path in .env
cat .env | grep LLAMACPP_MODEL_PATH

# Test model loading (Python)
python -c "
from langchain_community.llms import LlamaCpp
llm = LlamaCpp(model_path='/path/to/your/model.gguf')
print('Model loaded successfully!')
"

# Check available memory
free -h  # Linux
top     # Monitor memory usage while loading
```

### OpenAI not working?

```bash
# Check API key is set
echo $OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check for typos in .env
cat .env | grep OPENAI
```

### Anthropic not working?

```bash
# Check API key is set
echo $ANTHROPIC_API_KEY

# Check for typos in .env
cat .env | grep ANTHROPIC
```

## Cost Estimation

### Development (100 recipes)
- **Ollama**: $0 ✅
- **OpenAI (GPT-4o)**: ~$1.00
- **Anthropic (Claude)**: ~$2.00

### Production (1,000 recipes/month)
- **Ollama**: $0 (+ server costs if hosted)
- **OpenAI (GPT-4o)**: ~$10.00
- **Anthropic (Claude)**: ~$20.00

## Best Practices

1. **Development**: Use Ollama (qwen2.5:4b) for fast iteration
2. **Testing**: Use Ollama (qwen2.5:7b) for better quality
3. **Pre-prod**: Test with OpenAI to verify quality
4. **Production**: Use OpenAI or Anthropic for best results
5. **CI/CD**: Use Ollama to avoid API costs in tests

## Provider Selection Logic

```python
# The config.py automatically handles this:

if LLM_PROVIDER == "ollama":
    # Use local Ollama
    # No API key needed
    # Uses ChatOllama from langchain-ollama
    
elif LLM_PROVIDER == "llamacpp":
    # Use local llamacpp with GGUF models
    # No API key needed
    # Uses LlamaCpp from langchain-community
    # Direct model file access
    
elif LLM_PROVIDER == "openai":
    # Use OpenAI API
    # Requires OPENAI_API_KEY
    # Uses ChatOpenAI from langchain-openai
    # Supports native structured output
    
elif LLM_PROVIDER == "anthropic":
    # Use Anthropic API
    # Requires ANTHROPIC_API_KEY
    # Uses ChatAnthropic from langchain-anthropic
    # Uses parser for structured output
```

## Learn More

- [Ollama Setup Guide](OLLAMA_GUIDE.md)
- [llamacpp Setup Guide](LLAMACPP_GUIDE.md)
- [UV Package Manager](UV_GUIDE.md)
- [Quick Start Guide](QUICKSTART.md)

---

**Remember**: Keep it simple! Use Ollama for dev, switch to OpenAI for production. 🚀
