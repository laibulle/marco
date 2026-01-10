# Using llamacpp with Marco (Local Custom Models)

## Overview

llamacpp support allows you to run Marco with custom GGUF models locally, giving you:

- 🆓 **Free** - No API costs, runs locally
- 🎯 **Custom Models** - Use any GGUF model you prefer
- 🔒 **Private** - Your data never leaves your machine
- ⚡️ **Fast** - Optimized local inference with llama.cpp
- 🛠️ **Flexible** - Support for any model size and quantization

## Quick Setup

### 1. Install Dependencies

llamacpp support is included with Marco:

```bash
uv pip install -e .
# or
pip install -e .
```

If you encounter issues, you may need to install llamacpp separately:

```bash
pip install llama-cpp-python
```

### 2. Download a GGUF Model

Choose from these popular options:

```bash
# Create models directory
mkdir -p ./models

# Option 1: Llama 2 7B Chat (Recommended for recipes)
wget -O ./models/llama2-7b-chat.gguf \
  "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"

# Option 2: Mistral 7B (Great for structured output)
wget -O ./models/mistral-7b.gguf \
  "https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf"

# Option 3: Code Llama 7B (Good for JSON generation)
wget -O ./models/codellama-7b.gguf \
  "https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q4_K_M.gguf"
```

### 3. Configure Marco

```bash
# Edit .env file
LLM_PROVIDER=llamacpp
LLAMACPP_MODEL_PATH=./models/llama2-7b-chat.gguf
LLAMACPP_MAX_TOKENS=2048
LLAMACPP_TEMPERATURE=0.7
LLAMACPP_N_CTX=4096
```

### 4. Test Setup

```bash
# Initialize Marco
marco init

# Generate a test recipe
marco generate "simple pasta recipe" --anxiety-focus
```

## Configuration Options

### Environment Variables

```bash
# Required: Path to your GGUF model file
LLAMACPP_MODEL_PATH=/path/to/your/model.gguf

# Optional: Maximum tokens in response (default: 2048)
LLAMACPP_MAX_TOKENS=2048

# Optional: Creativity level 0.0-1.0 (default: 0.7)
LLAMACPP_TEMPERATURE=0.7

# Optional: Context window size (default: 4096)
LLAMACPP_N_CTX=4096
```

### Model Size Recommendations

| Model Size | RAM Required | Speed | Quality | Use Case |
|------------|--------------|-------|---------|----------|
| **3-4B models** | 4-6 GB | Very Fast | Good | Development/Testing |
| **7B models** | 6-10 GB | Fast | Great | Recommended for recipes |
| **13B models** | 12-16 GB | Medium | Excellent | High quality output |
| **30B+ models** | 20+ GB | Slow | Outstanding | Production quality |

### Quantization Levels

GGUF models come in different quantization levels:

- **Q2_K** - Smallest size, lowest quality
- **Q4_K_M** - **Recommended** - Good balance of size/quality
- **Q5_K_M** - Higher quality, larger size
- **Q6_K** - Near-original quality, much larger
- **Q8_0** - Highest quality, largest size

## Model Sources

### HuggingFace (TheBloke's Models)

TheBloke provides high-quality GGUF conversions:

```bash
# Browse available models
https://huggingface.co/TheBloke

# Popular choices for recipe generation:
# - Llama-2-7B-Chat-GGUF (conversational)
# - Mistral-7B-v0.1-GGUF (instruction following)
# - CodeLlama-7B-Instruct-GGUF (structured output)
# - Zephyr-7B-Beta-GGUF (fine-tuned chat)
```

### Direct Download Examples

```bash
# Llama 2 7B Chat Q4_K_M (4.08 GB)
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf

# Mistral 7B Q4_K_M (4.37 GB)
wget https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf

# Code Llama 7B Q4_K_M (4.24 GB)
wget https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q4_K_M.gguf
```

## Performance Tuning

### For Recipe Generation

```bash
# Optimized for structured JSON output
LLAMACPP_TEMPERATURE=0.3    # Lower for more consistent JSON
LLAMACPP_MAX_TOKENS=3000    # Enough for complete recipes
LLAMACPP_N_CTX=4096         # Good context for instructions
```

### For Development/Testing

```bash
# Faster generation, good enough quality
LLAMACPP_TEMPERATURE=0.7
LLAMACPP_MAX_TOKENS=2048
LLAMACPP_N_CTX=2048         # Smaller context = faster
```

## Troubleshooting

### "Model file not found"

```bash
# Check file exists
ls -la /path/to/your/model.gguf

# Check permissions
chmod 644 /path/to/your/model.gguf

# Use absolute path
LLAMACPP_MODEL_PATH=/home/user/models/model.gguf
```

### "Out of memory" errors

```bash
# Try a smaller model
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf

# Reduce context size
LLAMACPP_N_CTX=2048

# Check available RAM
free -h
```

### Slow generation

```bash
# Use smaller quantization
# Q4_K_M instead of Q5_K_M or Q6_K

# Reduce max tokens
LLAMACPP_MAX_TOKENS=1500

# Use GPU acceleration (if available)
pip install llama-cpp-python[cuda]  # For NVIDIA
pip install llama-cpp-python[metal] # For Apple Silicon
```

### JSON parsing errors

Some models struggle with consistent JSON output. Try:

```bash
# Lower temperature for more consistent output
LLAMACPP_TEMPERATURE=0.2

# Use models specifically fine-tuned for instruction following
# - CodeLlama-7B-Instruct
# - Mistral-7B-v0.1
# - Zephyr-7B-Beta
```

## Comparing Providers

| Feature | llamacpp | Ollama | OpenAI | Anthropic |
|---------|----------|--------|--------|-----------|
| **Cost** | Free | Free | ~$0.01/recipe | ~$0.02/recipe |
| **Setup** | Model download | `ollama pull` | API key | API key |
| **Customization** | High | Medium | Low | Low |
| **Model Choice** | Any GGUF | Ollama library | Fixed models | Fixed models |
| **Quality** | Depends on model | Good | Excellent | Excellent |

## Best Practices

### Development Workflow

1. **Start with llamacpp** for custom model experimentation
2. **Use Ollama** for easier model management
3. **Test with OpenAI** before production deployment

### Model Selection

- **For Development**: Use smaller models (3-7B) with Q4_K_M quantization
- **For Testing**: Use 7B models with Q4_K_M or Q5_K_M
- **For Production**: Consider larger models or cloud APIs

### Storage Management

```bash
# Models can be large - organize them
mkdir -p ~/models/{3b,7b,13b}

# Symlink active model for easy switching
ln -sf ~/models/7b/mistral-7b-v0.1.Q4_K_M.gguf ./current-model.gguf
LLAMACPP_MODEL_PATH=./current-model.gguf
```

## Example Configurations

### Quick Start (Small Model)

```bash
# Download a small model for testing
wget -O ./models/tinyllama.gguf \
  "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

# Configure
LLM_PROVIDER=llamacpp
LLAMACPP_MODEL_PATH=./models/tinyllama.gguf
LLAMACPP_MAX_TOKENS=1500
LLAMACPP_N_CTX=2048
```

### Balanced Setup (Recommended)

```bash
# Download Llama 2 7B
wget -O ./models/llama2-7b.gguf \
  "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"

# Configure
LLM_PROVIDER=llamacpp
LLAMACPP_MODEL_PATH=./models/llama2-7b.gguf
LLAMACPP_MAX_TOKENS=2048
LLAMACPP_TEMPERATURE=0.7
LLAMACPP_N_CTX=4096
```

### High Quality Setup

```bash
# Download larger model
wget -O ./models/llama2-13b.gguf \
  "https://huggingface.co/TheBloke/Llama-2-13B-Chat-GGUF/resolve/main/llama-2-13b-chat.Q5_K_M.gguf"

# Configure for quality
LLM_PROVIDER=llamacpp
LLAMACPP_MODEL_PATH=./models/llama2-13b.gguf
LLAMACPP_MAX_TOKENS=3000
LLAMACPP_TEMPERATURE=0.5
LLAMACPP_N_CTX=4096
```

## Learn More

- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [GGUF Format](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md)
- [TheBloke's Models](https://huggingface.co/TheBloke)
- [LangChain llamacpp Integration](https://python.langchain.com/docs/integrations/llms/llamacpp)

---

**Pro Tip**: Start with a 7B Q4_K_M model for the best balance of speed, quality, and resource usage! 🚀