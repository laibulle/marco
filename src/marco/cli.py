"""Command-line interface for Marco."""

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from marco.config import settings
from marco.db import Database, init_db
from marco.graph import create_recipe_graph
from marco.schemas import RecipeRequest, RecipeState

app = typer.Typer(
    name="marco",
    help="🍽️  AI-powered recipe generator with psychonutrition for anxiety management",
    add_completion=False,
)
console = Console()


@app.command()
def generate(
    description: str = typer.Argument(...,
                                      help="Description of the recipe to generate"),
    anxiety_focus: bool = typer.Option(
        True, "--anxiety-focus/--no-anxiety-focus", help="Optimize for anxiety reduction"
    ),
    dietary_restrictions: Optional[str] = typer.Option(
        None, "--restrictions", help="Dietary restrictions (comma-separated)"
    ),
    season: Optional[str] = typer.Option(
        None, "--season", help="Season for ingredients (winter, spring, summer, fall, auto)"
    ),
    region: Optional[str] = typer.Option(
        None, "--region", help="Geographic region (europe, north-america, asia)"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Save recipe to JSON file"
    ),
    pdf: Optional[Path] = typer.Option(
        None, "--pdf", help="Export recipe to PDF file"
    ),
):
    """Generate a chef-quality healthy recipe with psychonutrition analysis."""
    console.print(
        f"\n[bold cyan]🍽️  Generating recipe:[/bold cyan] {description}\n")

    # Parse dietary restrictions
    restrictions = []
    if dietary_restrictions:
        restrictions = [r.strip() for r in dietary_restrictions.split(",")]

    # Create request
    request = RecipeRequest(
        description=description,
        anxiety_focus=anxiety_focus,
        dietary_restrictions=restrictions,
        season=season or settings.default_season,
        region=region or settings.default_region,
    )

    # Execute graph with streaming to show progress
    graph = create_recipe_graph()

    console.print("[dim]Starting recipe generation workflow...[/dim]\n")

    step_names = {
        "generate_recipe": "🍳 Generating base recipe",
        "psychonutrition": "🧠 Dr. Maya: Analyzing psychonutrition benefits",
        "recipe_improvement": "🔄 Improving recipe based on expert feedback",
        "seasonal": "🌿 Chef Marco: Optimizing seasonal ingredients",
        "chef_review": "👨‍🍳 Chef Isabella: Reviewing culinary techniques",
        "expert_summary": "🗣️ Expert Collaboration: Creating consensus",
        "seasonal_check": "🔍 Checking seasonal requirements"
    }

    result = None
    try:
        for event in graph.stream({"request": request, "messages": []}):
            # event is a dict like {"node_name": state_update}
            for node_name, state_update in event.items():
                if node_name in step_names:
                    console.print(f"[cyan]→[/cyan] {step_names[node_name]}")
                else:
                    console.print(f"[dim]→ {node_name}[/dim]")
            result = state_update
    except Exception as e:
        error_msg = str(e)
        console.print(
            f"\n[red]✗ Error during recipe generation:[/red] {error_msg[:200]}")

        # Check if it's a JSON parsing error with Ollama
        if "Invalid json output" in error_msg and settings.llm_provider == "ollama":
            console.print(
                f"\n[yellow]Tip:[/yellow] The model '{settings.ollama_model}' may struggle with structured JSON output.")
            console.print(
                "[yellow]Try using a larger model like 'qwen2.5:7b' or 'llama3.2:3b' for better results:[/yellow]")
            console.print("  ollama pull qwen2.5:7b")
            console.print("  # or")
            console.print("  ollama pull llama3.2:3b")
            console.print("\nThen update the model in config:")
            console.print("  export OLLAMA_MODEL=qwen2.5:7b")
            console.print("  # or set in .env file: OLLAMA_MODEL=qwen2.5:7b")

        raise typer.Exit(1)

    if result is None or "recipe" not in result or result["recipe"] is None:
        console.print("[red]✗ Failed to generate recipe[/red]")
        raise typer.Exit(1)

    # Display result
    recipe = result["recipe"]
    console.print(
        f"\n[bold green]✓ Recipe generated:[/bold green] {recipe.name}\n")
    console.print(f"[dim]{recipe.description}[/dim]\n")

    # Display psychonutrition analysis
    if recipe.psychonutrition_analysis:
        analysis = recipe.psychonutrition_analysis
        console.print(
            f"[bold magenta]🧠 Anxiety Reduction Score:[/bold magenta] {analysis.anxiety_score}/10")
        console.print(
            f"[dim]Key nutrients: {', '.join(analysis.key_nutrients[:3])}[/dim]\n")

    # Display ingredients
    console.print("[bold]Ingredients:[/bold]")
    for ingredient in recipe.ingredients:
        console.print(
            f"  • {ingredient.quantity} {ingredient.unit} {ingredient.name}")

    console.print(f"\n[bold]Preparation time:[/bold] {recipe.prep_time} min")
    console.print(f"[bold]Cooking time:[/bold] {recipe.cook_time} min")
    console.print(f"[bold]Servings:[/bold] {recipe.servings}\n")

    # Save to file
    if output:
        output.write_text(recipe.model_dump_json(indent=2))
        console.print(f"[green]✓ Saved to {output}[/green]")

    # Export to PDF
    if pdf:
        try:
            from marco.pdf import generate_recipe_pdf
            generate_recipe_pdf(recipe, pdf)
            console.print(f"[green]✓ PDF exported to {pdf}[/green]")
        except ImportError as e:
            console.print(
                f"[red]✗ PDF export failed: {e}[/red]\n"
                "[yellow]PDF support requires system libraries. On macOS, install with:[/yellow]\n"
                "  brew install pango cairo gdk-pixbuf"
            )
        except Exception as e:
            console.print(f"[red]✗ PDF export failed: {e}[/red]")

    # Save to database
    db = Database()
    db.save_recipe(recipe)


@app.command()
def variations(
    recipe_file: Path = typer.Argument(..., help="Path to recipe JSON file"),
    season: str = typer.Option(..., "--season",
                               help="Season (winter, spring, summer, fall)"),
    region: Optional[str] = typer.Option(
        None, "--region", help="Geographic region"
    ),
):
    """Generate seasonal variations of an existing recipe."""
    console.print(
        f"\n[bold cyan]🌿 Generating seasonal variations[/bold cyan]\n")

    # Load recipe
    recipe_data = json.loads(recipe_file.read_text())

    # Create variation request
    from marco.schemas import Recipe
    recipe = Recipe.model_validate(recipe_data)

    # Use seasonal agent
    from marco.agents.seasonal import generate_seasonal_variation

    variation = generate_seasonal_variation(
        recipe,
        season=season,
        region=region or settings.default_region
    )

    # Display variation
    console.print(
        f"[bold green]✓ Seasonal variation:[/bold green] {variation.name}\n")

    table = Table(title="Ingredient Substitutions")
    table.add_column("Original", style="cyan")
    table.add_column("Substitute", style="green")
    table.add_column("Reason", style="dim")

    for sub in variation.substitutions:
        table.add_row(sub.original, sub.substitute, sub.reason)

    console.print(table)


@app.command()
def export_pdf(
    recipe_file: Path = typer.Argument(..., help="Path to recipe JSON file"),
    output: Path = typer.Option(
        "recipe.pdf", "--output", "-o", help="Output PDF path"),
):
    """Export a recipe to a beautiful PDF."""
    console.print(f"\n[bold cyan]📄 Exporting to PDF[/bold cyan]\n")

    # Load recipe
    from marco.schemas import Recipe
    recipe_data = json.loads(recipe_file.read_text())
    recipe = Recipe.model_validate(recipe_data)

    # Generate PDF
    generate_recipe_pdf(recipe, output)
    console.print(f"[green]✓ PDF exported to {output}[/green]")


@app.command()
def interactive():
    """Start interactive recipe generation session."""
    console.print(
        "\n[bold cyan]🍽️  Marco - Interactive Recipe Generator[/bold cyan]\n")
    console.print("Type 'exit' to quit\n")

    while True:
        try:
            description = typer.prompt("What would you like to cook?")
            if description.lower() in ["exit", "quit"]:
                break

            # Ask for preferences
            anxiety_focus = typer.confirm(
                "Optimize for anxiety reduction?", default=True)

            # Generate recipe
            generate(
                description=description,
                anxiety_focus=anxiety_focus,
                dietary_restrictions=None,
                season=None,
                region=None,
                output=None,
                pdf=None,
            )

            console.print("\n" + "─" * 60 + "\n")

        except KeyboardInterrupt:
            break

    console.print("\n[dim]Goodbye! 👋[/dim]\n")


@app.command()
def init():
    """Initialize Marco database and configuration."""
    console.print("\n[bold cyan]🔧 Initializing Marco[/bold cyan]\n")

    # Initialize database
    init_db()
    console.print("[green]✓ Database initialized[/green]")

    # Check configuration
    try:
        api_key = settings.get_api_key()
        console.print(
            f"[green]✓ API key configured for {settings.llm_provider}[/green]")
    except ValueError as e:
        console.print(f"[yellow]⚠ {e}[/yellow]")
        console.print("[dim]Please set your API key in .env file[/dim]")

    console.print("\n[green]✓ Marco is ready to use![/green]\n")


@app.command()
def version():
    """Show Marco version."""
    from marco import __version__
    console.print(f"Marco version {__version__}")


if __name__ == "__main__":
    app()
