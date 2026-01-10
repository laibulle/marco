# Using Ollama with Marco (Local Development)

## Why Ollama for Development?

- 🆓 **Free** - No API costs during development
- 🏠 **Local** - Runs on your machine, no internet needed
- 🚀 **Fast** - Optimized for local inference
- 🔒 **Private** - Your data never leaves your machine
- 🎯 **Perfect for dev** - Fast iteration, unlimited requests

## Quick Setup

### 1. Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or with brew (macOS)
brew install ollama

# Or download from https://ollama.com
```

### 2. Pull the qwen3:4b Model

```bash
# Start Ollama (it usually auto-starts)
ollama serve

# In another terminal, pull the model
ollama pull qwen3:4b
```

**Why qwen3:4b?**
- Small (2.5GB) - Fast to download
- Fast inference - Good for development iteration
- Quality output - Surprisingly good for 4B parameters
- Low RAM - Works on most laptops

### 3. Configure Marco

```bash
cd /Users/guillaume.bailleul/perso/marco

# Copy env example
cp .env.example .env

# The default is already set to ollama!
# LLM_PROVIDER=ollama
# OLLAMA_MODEL=qwen3:4b
# OLLAMA_BASE_URL=http://localhost:11434
```

### 4. Test It!

```bash
# Initialize
marco init

# Generate a recipe
marco generate "pasta with vegetables" --anxiety-focus
```

## Available Ollama Models

### For Development (Recommended)

```bash
# qwen3:4b - Small, fast, good quality
ollama pull qwen3:4b

# phi3:mini - Microsoft's small model (3.8B)
ollama pull phi3:mini

# llama3.2:3b - Meta's small model
ollama pull llama3.2:3b
```

### For Better Quality (Larger)

```bash
# qwen3:7b - Better quality, still fast
ollama pull qwen3:7b

# llama3.2:8b - Good balance
ollama pull llama3.2:8b

# mistral:7b - Popular choice
ollama pull mistral:7b
```

### For Best Quality (Requires more RAM)

```bash
# qwen3:14b - Excellent quality
ollama pull qwen3:14b

# llama3.1:13b - Very good
ollama pull llama3.1:13b
```

## Switching Models

Just update your `.env` file:

```bash
# Use a different Ollama model
OLLAMA_MODEL=qwen3:7b

# Or use a larger model
OLLAMA_MODEL=llama3.2:8b
```

## Switching Providers

### Development → Production

When you're ready for production, just change the provider:

```bash
# .env file

# For production with OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o

# Or with Anthropic
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### Switch via Environment Variable

```bash
# Use ollama for this run
LLM_PROVIDER=ollama marco generate "soup recipe"

# Use openai for this run
LLM_PROVIDER=openai marco generate "soup recipe"
```

## Performance Comparison

| Provider | Speed | Cost | Quality | Setup |
|----------|-------|------|---------|-------|
| **Ollama (qwen3:4b)** | ⚡️⚡️⚡️ Very Fast | 🆓 Free | ⭐️⭐️⭐️ Good | Easy |
| **Ollama (qwen3:7b)** | ⚡️⚡️ Fast | 🆓 Free | ⭐️⭐️⭐️⭐️ Great | Easy |
| **OpenAI (GPT-4o)** | ⚡️⚡️ Fast | 💰 ~$0.01/recipe | ⭐️⭐️⭐️⭐️⭐️ Excellent | API Key |
| **Anthropic (Claude)** | ⚡️⚡️ Fast | 💰 ~$0.02/recipe | ⭐️⭐️⭐️⭐️⭐️ Excellent | API Key |

## Troubleshooting

### "Connection refused" error

```bash
# Make sure Ollama is running
ollama serve

# Or restart it
pkill ollama && ollama serve
```

### "Model not found"

```bash
# Pull the model first
ollama pull qwen3:4b

# List available models
ollama list
```

### Slow generation

```bash
# Use a smaller model
echo "OLLAMA_MODEL=qwen3:4b" >> .env

# Or check if Ollama is using GPU
ollama ps  # Should show GPU usage
```

### Out of memory

```bash
# Use smaller model
ollama pull phi3:mini
echo "OLLAMA_MODEL=phi3:mini" >> .env

# Or stop other applications
```

## Ollama Commands

```bash
# List downloaded models
ollama list

# Remove a model
ollama rm qwen3:4b

# Show model info
ollama show qwen3:4b

# Test a model directly
ollama run qwen3:4b "Write a haiku about cooking"

# Monitor running models
ollama ps

# Stop Ollama
pkill ollama
```

## Development Workflow

### Typical Dev Flow

1. **Start Ollama** (usually auto-starts)
   ```bash
   ollama serve
   ```

2. **Develop with local model** (free, fast iteration)
   ```bash
   marco generate "test recipe" --anxiety-focus
   ```

3. **Test with production model** (before deploying)
   ```bash
   LLM_PROVIDER=openai marco generate "test recipe"
   ```

4. **Deploy** with production provider in `.env`

## Model Recommendations

### For Marco Development

**Best overall: qwen3:7b**
- Good balance of speed and quality
- Handles recipe JSON structure well
- Fast enough for development

```bash
ollama pull qwen3:7b
echo "OLLAMA_MODEL=qwen3:7b" >> .env
```

**Fastest: qwen3:4b** (default)
- Best for rapid iteration
- Good enough for development
- Smallest size

**Best quality: qwen3:14b**
- Nearly production-quality output
- Use for final testing before production
- Requires more RAM (~8GB)

## Advanced: Custom Ollama Server

If running Ollama on a different machine:

```bash
# .env
OLLAMA_BASE_URL=http://192.168.1.100:11434

# Or remote server
OLLAMA_BASE_URL=http://ollama-server.yourcompany.com:11434
```

## Cost Savings

Development costs with different approaches:

```
100 recipe generations:

Ollama (local):      $0.00 ✅
OpenAI (GPT-4o):     ~$1.00
Anthropic (Claude):  ~$2.00

1000 recipe generations:

Ollama (local):      $0.00 ✅
OpenAI (GPT-4o):     ~$10.00
Anthropic (Claude):  ~$20.00
```

Perfect for:
- Development and testing
- Prototyping features
- Learning and experimentation
- CI/CD pipelines
- Demo environments

## Learn More

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Models Library](https://ollama.com/library)
- [qwen3 Model Info](https://ollama.com/library/qwen3)
- [LangChain Ollama Integration](https://python.langchain.com/docs/integrations/llms/ollama)

---

**Pro Tip**: Keep `LLM_PROVIDER=ollama` in your `.env` for development, and only switch to paid providers when you need production-quality output! 🚀
