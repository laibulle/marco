"""PDF generation for recipes using WeasyPrint."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from marco.config import settings
from marco.schemas import Recipe


def generate_recipe_pdf(recipe: Recipe, output_path: Path) -> None:
    """Generate a beautiful PDF from a recipe.

    Args:
        recipe: Recipe object to render
        output_path: Path where PDF should be saved
    """
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(settings.templates_dir)))
    template = env.get_template("recipe.html")

    # Render HTML
    html_content = template.render(recipe=recipe)

    # Generate PDF
    HTML(string=html_content, base_url=str(settings.templates_dir)).write_pdf(
        output_path
    )


def preview_recipe_html(recipe: Recipe, output_path: Path) -> None:
    """Generate HTML preview of recipe (for development/debugging).

    Args:
        recipe: Recipe object to render
        output_path: Path where HTML should be saved
    """
    env = Environment(loader=FileSystemLoader(str(settings.templates_dir)))
    template = env.get_template("recipe.html")

    html_content = template.render(recipe=recipe)
    output_path.write_text(html_content)
