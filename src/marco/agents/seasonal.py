"""Seasonal optimization agent for ingredient substitutions."""

import json
from datetime import datetime
from typing import Dict, List

from marco.config import settings
from marco.schemas import (
    IngredientSubstitution,
    Recipe,
    RecipeState,
    SeasonalVariation,
)


def load_seasonal_database() -> Dict:
    """Load the seasonal ingredients database."""
    seasonal_file = settings.data_dir / "seasonal_ingredients.json"
    if not seasonal_file.exists():
        return {"seasonal_ingredients": {}, "regions": {}}

    with open(seasonal_file) as f:
        return json.load(f)


def get_current_season() -> str:
    """Determine current season based on month (Northern Hemisphere)."""
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:  # 9, 10, 11
        return "fall"


def find_substitutions(
    recipe: Recipe, season: str, region: str, seasonal_db: Dict
) -> List[IngredientSubstitution]:
    """Find seasonal substitutions for recipe ingredients."""
    substitutions = []
    seasonal_ingredients = seasonal_db.get("seasonal_ingredients", {})

    # Check each ingredient category
    for category in ["vegetables", "fruits", "herbs", "fish"]:
        category_items = seasonal_ingredients.get(category, {})

        for ingredient in recipe.ingredients:
            ingredient_name = ingredient.name.lower()

            # Check if this ingredient has seasonal data
            for item_name, item_data in category_items.items():
                if item_name in ingredient_name or ingredient_name in item_name:
                    peak_seasons = item_data.get("peak_season", [])

                    # If not in peak season, look for substitutes
                    if season not in peak_seasons:
                        substitutes = item_data.get("substitutes", {})
                        if season in substitutes:
                            sub_data = substitutes[season]
                            substitutions.append(
                                IngredientSubstitution(
                                    original=ingredient.name,
                                    substitute=sub_data["ingredient"],
                                    reason=sub_data["reason"],
                                    adjustment=f"Use same quantity: {ingredient.quantity} {ingredient.unit}",
                                )
                            )

    return substitutions


def seasonal_optimization_node(state: RecipeState) -> RecipeState:
    """Optimize recipe for seasonal ingredients.

    This agent:
    - Identifies out-of-season ingredients
    - Suggests seasonal substitutes
    - Provides reasoning for substitutions
    - Adjusts quantities if needed
    """
    if not state.recipe:
        state.errors.append("No recipe to optimize")
        return state

    recipe = state.recipe
    request = state.request

    # Determine season
    season = request.season
    if season == "auto":
        season = get_current_season()

    # Load seasonal database
    seasonal_db = load_seasonal_database()

    # Find substitutions
    substitutions = find_substitutions(
        recipe, season, request.region, seasonal_db)

    if substitutions:
        # Create seasonal variation
        variation = SeasonalVariation(
            name=f"{recipe.name} ({season.capitalize()} Variation)",
            season=season,
            region=request.region,
            substitutions=substitutions,
            notes=f"Optimized for {season} ingredients in {request.region}",
        )

        state.seasonal_variation = variation

        # Update recipe season metadata
        recipe.season = season
        recipe.variations.append(
            f"{season.capitalize()}: " +
            ", ".join([s.substitute for s in substitutions[:3]])
        )

        state.messages.append({
            "role": "assistant",
            "content": f"Found {len(substitutions)} seasonal substitutions for {season}",
        })
    else:
        state.messages.append({
            "role": "assistant",
            "content": f"Recipe is already optimized for {season}",
        })
        # Still update season
        recipe.season = season

    state.recipe = recipe
    return state


def generate_seasonal_variation(
    recipe: Recipe, season: str, region: str
) -> SeasonalVariation:
    """Generate seasonal variation (standalone function for CLI)."""
    seasonal_db = load_seasonal_database()
    substitutions = find_substitutions(recipe, season, region, seasonal_db)

    return SeasonalVariation(
        name=f"{recipe.name} ({season.capitalize()} Variation)",
        season=season,
        region=region,
        substitutions=substitutions,
        notes=f"Optimized for {season} ingredients in {region}",
    )
