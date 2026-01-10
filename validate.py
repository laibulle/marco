#!/usr/bin/env python
"""Validation script to check project structure and imports."""

import sys
from pathlib import Path


def check_file_exists(filepath: str) -> bool:
    """Check if a file exists."""
    path = Path(filepath)
    exists = path.exists()
    status = "✓" if exists else "✗"
    print(f"  {status} {filepath}")
    return exists


def main():
    """Run validation checks."""
    print("🔍 Validating Marco Project Structure\n")

    all_good = True

    # Check documentation
    print("📚 Documentation:")
    all_good &= check_file_exists("README.md")
    all_good &= check_file_exists("QUICKSTART.md")
    all_good &= check_file_exists("IMPLEMENTATION.md")
    all_good &= check_file_exists("PROJECT_SUMMARY.txt")

    # Check configuration
    print("\n⚙️  Configuration:")
    all_good &= check_file_exists("pyproject.toml")
    all_good &= check_file_exists("langgraph.json")
    all_good &= check_file_exists(".env.example")
    all_good &= check_file_exists(".gitignore")
    all_good &= check_file_exists("Makefile")

    # Check core modules
    print("\n🧠 Core Modules:")
    all_good &= check_file_exists("src/marco/__init__.py")
    all_good &= check_file_exists("src/marco/__main__.py")
    all_good &= check_file_exists("src/marco/cli.py")
    all_good &= check_file_exists("src/marco/config.py")
    all_good &= check_file_exists("src/marco/schemas.py")
    all_good &= check_file_exists("src/marco/graph.py")
    all_good &= check_file_exists("src/marco/db.py")
    all_good &= check_file_exists("src/marco/pdf.py")

    # Check agents
    print("\n🤖 Agents:")
    all_good &= check_file_exists("src/marco/agents/__init__.py")
    all_good &= check_file_exists("src/marco/agents/recipe_generator.py")
    all_good &= check_file_exists("src/marco/agents/psychonutrition.py")
    all_good &= check_file_exists("src/marco/agents/seasonal.py")

    # Check data
    print("\n📊 Knowledge Bases:")
    all_good &= check_file_exists("data/nutrients.json")
    all_good &= check_file_exists("data/seasonal_ingredients.json")

    # Check templates
    print("\n🎨 Templates:")
    all_good &= check_file_exists("templates/recipe.html")
    all_good &= check_file_exists("templates/style.css")

    # Check examples
    print("\n📝 Examples:")
    all_good &= check_file_exists("examples.py")

    # Summary
    print("\n" + "=" * 60)
    if all_good:
        print("✅ All files present! Project structure is complete.")
        print("\nNext steps:")
        print("  1. Install: pip install -e .")
        print("  2. Configure: cp .env.example .env (add API key)")
        print("  3. Initialize: marco init")
        print("  4. Generate: marco generate 'your recipe'")
        return 0
    else:
        print("❌ Some files are missing. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
