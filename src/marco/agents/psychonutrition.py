"""Psychonutrition analysis agent for anxiety management."""

import json
from pathlib import Path
from typing import Dict, List

from marco.config import settings
from marco.schemas import PsychonutritionAnalysis, Recipe, RecipeState


def load_nutrient_database() -> Dict:
    """Load the nutrient database."""
    nutrient_file = settings.data_dir / "nutrients.json"
    if not nutrient_file.exists():
        return {"nutrients": {}, "food_combinations": [], "anxiety_types": {}}

    with open(nutrient_file) as f:
        return json.load(f)


def calculate_anxiety_score(recipe: Recipe, nutrient_db: Dict) -> float:
    """Calculate anxiety reduction score based on ingredients and nutrients.

    Score is 0-10, where higher is better for anxiety reduction.
    """
    score = 0.0
    nutrients = nutrient_db.get("nutrients", {})

    # Get all ingredient names (lowercase for matching)
    ingredient_names = [ing.name.lower() for ing in recipe.ingredients]

    # Check for anxiety-reducing nutrients in ingredients
    nutrient_matches = {}
    for nutrient_key, nutrient_info in nutrients.items():
        sources = [s.lower() for s in nutrient_info.get("sources", [])]
        matches = [ing for ing in ingredient_names if any(
            source in ing for source in sources)]
        if matches:
            nutrient_matches[nutrient_key] = matches
            # Add to score (max 1.5 points per nutrient category, up to 9 points)
            score += min(1.5, len(matches) * 0.5)

    # Bonus for food combinations
    for combo in nutrient_db.get("food_combinations", []):
        combo_ingredients = combo["combination"].lower().split(" + ")
        if sum(1 for ci in combo_ingredients if any(ci in ing for ing in ingredient_names)) >= 2:
            score += 0.5

    # Bonus for fermented/probiotic foods
    probiotic_sources = [s.lower() for s in nutrients.get(
        "probiotics", {}).get("sources", [])]
    if any(source in ing for ing in ingredient_names for source in probiotic_sources):
        score += 0.5

    # Cap at 10
    return min(10.0, score)


def identify_key_nutrients(recipe: Recipe, nutrient_db: Dict) -> List[str]:
    """Identify key anxiety-reducing nutrients in the recipe."""
    nutrients = nutrient_db.get("nutrients", {})
    ingredient_names = [ing.name.lower() for ing in recipe.ingredients]

    key_nutrients = []
    for nutrient_key, nutrient_info in nutrients.items():
        sources = [s.lower() for s in nutrient_info.get("sources", [])]
        if any(source in ing for ing in ingredient_names for source in sources):
            key_nutrients.append(nutrient_info["name"])

    return key_nutrients


def generate_mechanisms(key_nutrients: List[str], nutrient_db: Dict) -> List[str]:
    """Generate explanations of how nutrients help reduce anxiety."""
    mechanisms = []
    nutrients = nutrient_db.get("nutrients", {})

    for nutrient_key, nutrient_info in nutrients.items():
        if nutrient_info["name"] in key_nutrients:
            mechanisms.append(nutrient_info["anxiety_benefit"])

    return mechanisms[:5]  # Top 5 mechanisms


def generate_recommendations(recipe: Recipe, anxiety_score: float, nutrient_db: Dict) -> List[str]:
    """Generate personalized recommendations for anxiety management."""
    recommendations = []

    # General recommendations
    recommendations.append(
        "Eat this meal mindfully, chewing slowly to enhance nutrient absorption")

    if anxiety_score < 7:
        recommendations.append(
            "Consider adding fermented foods like yogurt or kimchi for gut health")
        recommendations.append(
            "Pair with herbal tea (chamomile or green tea) for added calming effects")

    recommendations.append(
        "Maintain consistent meal times to stabilize blood sugar and mood")
    recommendations.append(
        "Stay hydrated throughout the day for optimal brain function")

    # Check if recipe has protein
    has_good_protein = any(
        ing.name.lower() in ["chicken", "turkey", "salmon", "eggs", "tofu"]
        for ing in recipe.ingredients
    )
    if not has_good_protein:
        recommendations.append(
            "Add a protein source rich in tryptophan for better serotonin production")

    return recommendations[:5]


def analyze_psychonutrition_node(state: RecipeState) -> RecipeState:
    """Analyze recipe for psychonutrition and anxiety-reducing properties.

    This agent:
    - Calculates anxiety reduction score
    - Identifies key nutrients
    - Explains mechanisms of action
    - Provides recommendations
    """
    if not state.recipe:
        state.errors.append("No recipe to analyze")
        return state

    recipe = state.recipe
    nutrient_db = load_nutrient_database()

    # Calculate anxiety score
    anxiety_score = calculate_anxiety_score(recipe, nutrient_db)

    # Identify key nutrients
    key_nutrients = identify_key_nutrients(recipe, nutrient_db)

    # Generate mechanisms
    mechanisms = generate_mechanisms(key_nutrients, nutrient_db)

    # Generate recommendations
    recommendations = generate_recommendations(
        recipe, anxiety_score, nutrient_db)

    # Create analysis
    analysis = PsychonutritionAnalysis(
        anxiety_score=round(anxiety_score, 1),
        key_nutrients=key_nutrients[:5],  # Top 5
        mechanisms=mechanisms,
        recommendations=recommendations,
        cautions=["Consult healthcare provider for personalized advice"]
        if anxiety_score < 5
        else None,
    )

    # Update recipe with analysis
    recipe.psychonutrition_analysis = analysis
    state.recipe = recipe

    state.messages.append({
        "role": "assistant",
        "content": f"Psychonutrition analysis complete. Anxiety score: {anxiety_score}/10",
    })

    return state
