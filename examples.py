#!/usr/bin/env python
"""Example script demonstrating Marco usage."""

from marco.agents.recipe_generator import generate_recipe
from marco.agents.psychonutrition import analyze_psychonutrition_node
from marco.agents.seasonal import generate_seasonal_variation
from marco.pdf import generate_recipe_pdf
from marco.schemas import RecipeRequest, RecipeState
from pathlib import Path


def example_basic_recipe():
    """Example: Generate a basic recipe."""
    print("=" * 60)
    print("Example 1: Basic Recipe Generation")
    print("=" * 60)

    recipe = generate_recipe(
        description="Grilled salmon with roasted vegetables",
        anxiety_focus=True,
        servings=4
    )

    print(f"\n✓ Generated: {recipe.name}")
    print(f"  Prep time: {recipe.prep_time} min")
    print(f"  Cook time: {recipe.cook_time} min")
    print(f"  Ingredients: {len(recipe.ingredients)}")
    print(f"  Instructions: {len(recipe.instructions)} steps")

    return recipe


def example_with_psychonutrition(recipe):
    """Example: Add psychonutrition analysis."""
    print("\n" + "=" * 60)
    print("Example 2: Psychonutrition Analysis")
    print("=" * 60)

    # Create state
    request = RecipeRequest(
        description="Grilled salmon with roasted vegetables",
        anxiety_focus=True
    )
    state = RecipeState(request=request, recipe=recipe, messages=[])

    # Analyze
    result_state = analyze_psychonutrition_node(state)
    analysis = result_state.recipe.psychonutrition_analysis

    if analysis:
        print(f"\n✓ Anxiety Reduction Score: {analysis.anxiety_score}/10")
        print(f"  Key Nutrients: {', '.join(analysis.key_nutrients[:3])}")
        print(f"  Mechanisms: {len(analysis.mechanisms)}")

    return result_state.recipe


def example_seasonal_variation(recipe):
    """Example: Generate seasonal variation."""
    print("\n" + "=" * 60)
    print("Example 3: Seasonal Variation")
    print("=" * 60)

    variation = generate_seasonal_variation(
        recipe=recipe,
        season="winter",
        region="europe"
    )

    print(f"\n✓ Created: {variation.name}")
    print(f"  Season: {variation.season}")
    print(f"  Substitutions: {len(variation.substitutions)}")

    if variation.substitutions:
        print("\n  Examples:")
        for sub in variation.substitutions[:3]:
            print(f"    • {sub.original} → {sub.substitute}")
            print(f"      Reason: {sub.reason}")


def example_pdf_export(recipe):
    """Example: Export to PDF."""
    print("\n" + "=" * 60)
    print("Example 4: PDF Export")
    print("=" * 60)

    output_path = Path("example_recipe.pdf")
    generate_recipe_pdf(recipe, output_path)

    print(f"\n✓ PDF exported to: {output_path}")
    print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")


def main():
    """Run all examples."""
    print("\n🍽️  Marco Examples\n")

    try:
        # Generate base recipe
        recipe = example_basic_recipe()

        # Add psychonutrition analysis
        recipe = example_with_psychonutrition(recipe)

        # Generate seasonal variation
        example_seasonal_variation(recipe)

        # Export to PDF
        example_pdf_export(recipe)

        print("\n" + "=" * 60)
        print("✓ All examples completed successfully!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure you've:")
        print("  1. Installed dependencies: pip install -e .")
        print("  2. Set up API key in .env file")
        print("  3. Run: marco init")


if __name__ == "__main__":
    main()
