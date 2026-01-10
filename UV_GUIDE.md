# Using UV with Marco

[UV](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver, written in Rust. It's 10-100x faster than pip!

## Why UV?

- ⚡️ **10-100x faster** than pip for package installation
- 🔒 **Deterministic** dependency resolution with lockfiles
- 🚀 **Drop-in replacement** for pip commands
- 💾 **Efficient caching** to save bandwidth and time
- 🦀 **Written in Rust** for maximum performance

## Installation

### Install UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with brew
brew install uv

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup Marco with UV

```bash
# 1. Navigate to project
cd /Users/guillaume.bailleul/perso/marco

# 2. Create virtual environment
uv venv

# 3. Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# 4. Install dependencies
uv pip install -e .

# 5. Configure and initialize
cp .env.example .env
# Edit .env with your API key
marco init
```

## Using UV Commands

### Install Package
```bash
# Development install
uv pip install -e .

# With dev dependencies
uv pip install -e ".[dev]"

# Production install (when published)
uv pip install marco
```

### Sync Dependencies
```bash
# Install from pyproject.toml
uv pip sync

# Upgrade all packages
uv pip install --upgrade -e .
```

### Install Specific Packages
```bash
# Add a new dependency
uv pip install package-name

# Install specific version
uv pip install package-name==1.2.3
```

### Virtual Environment Management
```bash
# Create venv with specific Python version
uv venv --python 3.11

# Create venv with custom name
uv venv my-env

# Remove venv
rm -rf .venv
```

## Makefile Commands with UV

The Makefile has been updated to use UV by default:

```bash
# Complete setup (checks uv, creates venv, installs, inits)
make setup

# Check if uv is installed
make check-uv

# Create virtual environment
make venv

# Install with uv
make install

# Install with pip (fallback)
make install-pip

# Install dev dependencies
make install-dev
```

## Speed Comparison

Example installation times:

```bash
# pip (traditional)
$ time pip install -e .
real    0m45.231s

# uv (fast!)
$ time uv pip install -e .
real    0m3.847s
```

**That's ~12x faster!** ⚡️

## UV vs PIP Cheatsheet

| Task | pip | uv |
|------|-----|-----|
| Install package | `pip install package` | `uv pip install package` |
| Install from requirements | `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| Editable install | `pip install -e .` | `uv pip install -e .` |
| Upgrade package | `pip install --upgrade package` | `uv pip install --upgrade package` |
| List installed | `pip list` | `uv pip list` |
| Create venv | `python -m venv venv` | `uv venv` |
| Freeze requirements | `pip freeze` | `uv pip freeze` |

## Troubleshooting

### "uv: command not found"
Make sure UV is installed and in your PATH:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Virtual environment issues
Remove and recreate:
```bash
rm -rf .venv
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Dependency conflicts
UV has better dependency resolution than pip, but if you encounter issues:
```bash
# Clear UV cache
uv cache clean

# Reinstall
uv pip install -e . --no-cache
```

## Additional UV Features

### Python Version Management
```bash
# Install a specific Python version
uv python install 3.11

# Use specific Python for venv
uv venv --python 3.11
```

### Compile Dependencies
```bash
# Generate requirements.txt with locked versions
uv pip compile pyproject.toml -o requirements.txt

# With extras
uv pip compile pyproject.toml --extra dev -o requirements-dev.txt
```

## Migration from pip

If you've been using pip, migration is simple:

1. **Install UV**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. **Replace commands**: Change `pip` to `uv pip` in your workflow
3. **Enjoy speed**: Everything works the same, just faster!

Your existing `pyproject.toml`, `requirements.txt`, and virtual environments all work with UV - no changes needed!

## Learn More

- [UV Documentation](https://github.com/astral-sh/uv)
- [UV vs pip performance](https://github.com/astral-sh/uv#performance)
- [Astral.sh](https://astral.sh/) - The team behind UV and Ruff

---

**Tip**: You can use `uv pip` as a drop-in replacement for `pip` in all your commands. UV is fully compatible with pip's API! 🎉
