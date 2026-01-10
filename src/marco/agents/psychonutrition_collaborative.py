"""Enhanced psychonutrition analysis agent with expert conversation."""

import json
import uuid
from pathlib import Path
from typing import Dict, List

from ..config import settings
from ..conversation import conversation_manager
from ..schemas import (
    PsychonutritionAnalysis, Recipe, RecipeState, 
    ExpertRole, MessageType
)


def load_nutrient_database() -> Dict:
    """Load the nutrient database."""
    nutrient_file = settings.data_dir / "nutrients.json"
    if not nutrient_file.exists():
        return {"nutrients": {}, "food_combinations": [], "anxiety_types": {}}

    with open(nutrient_file) as f:
        return json.load(f)


def calculate_anxiety_score(recipe: Recipe, nutrient_db: Dict) -> float:
    """Calculate anxiety reduction score based on ingredients and nutrients."""
    score = 0.0
    nutrients = nutrient_db.get("nutrients", {})

    ingredient_names = [ing.name.lower() for ing in recipe.ingredients]

    nutrient_matches = {}
    for nutrient_key, nutrient_info in nutrients.items():
        sources = [s.lower() for s in nutrient_info.get("sources", [])]
        matches = [ing for ing in ingredient_names if any(
            source in ing for source in sources)]
        if matches:
            nutrient_matches[nutrient_key] = matches
            score += min(1.5, len(matches) * 0.5)

    for combo in nutrient_db.get("food_combinations", []):
        combo_ingredients = combo["combination"].lower().split(" + ")
        if sum(1 for ci in combo_ingredients if any(ci in ing for ing in ingredient_names)) >= 2:
            score += 0.5

    probiotic_sources = [s.lower() for s in nutrients.get(
        "probiotics", {}).get("sources", [])]
    if any(source in ing for source in probiotic_sources for ing in ingredient_names):
        score += 1.0

    return min(score, 10.0)


def create_expert_discussion(state: RecipeState, analysis: PsychonutritionAnalysis) -> RecipeState:
    """Create expert discussion about the psychonutrition analysis."""
    
    # Initialize experts if not already done
    if not state.experts:
        state = conversation_manager.initialize_experts(state)
    
    # Update context
    state = conversation_manager.update_context(
        state,
        topic="Psychonutrition Analysis",
        phase="analysis"
    )
    
    # Dr. Maya Chen presents her analysis
    if analysis.anxiety_score < 5.0:
        concern_msg = f"""I've analyzed this recipe and I have some concerns about its anxiety-reducing potential. 
        
The current anxiety score is only {analysis.anxiety_score:.1f}/10. While the recipe includes {', '.join(analysis.key_nutrients[:3])}, 
I think we could significantly improve this by considering some modifications:

1. Could we add more omega-3 rich ingredients like walnuts or chia seeds?
2. The magnesium content could be boosted with dark leafy greens or pumpkin seeds
3. For better GABA support, fermented ingredients would be beneficial

What do you think, Chef Isabella and Marco? Can we enhance this nutritionally while maintaining the culinary integrity?"""
        
        state = conversation_manager.add_message(
            state,
            from_expert=ExpertRole.PSYCHONUTRITIONIST,
            content=concern_msg,
            message_type=MessageType.CONCERN
        )
    else:
        approval_msg = f"""Excellent work on this recipe! I'm pleased to see an anxiety score of {analysis.anxiety_score:.1f}/10.

The recipe effectively incorporates {', '.join(analysis.key_nutrients)} which work through these mechanisms:
{chr(10).join('• ' + mech for mech in analysis.mechanisms[:3])}

This combination should help users feel more balanced and less anxious. The nutritional synergy here is particularly good - 
these nutrients work together to support the gut-brain axis and neurotransmitter production.

I give this my full approval from a psychonutrition standpoint!"""
        
        state = conversation_manager.add_message(
            state,
            from_expert=ExpertRole.PSYCHONUTRITIONIST,
            content=approval_msg,
            message_type=MessageType.APPROVAL
        )
    
    # Add a question for the seasonal expert
    seasonal_question = """Marco, from a seasonal perspective, are these ingredients at their peak right now? 
I want to make sure we're getting maximum nutrient density from fresh, in-season produce."""
    
    state = conversation_manager.add_message(
        state,
        from_expert=ExpertRole.PSYCHONUTRITIONIST,
        content=seasonal_question,
        message_type=MessageType.QUESTION,
        to_expert=ExpertRole.SEASONAL_EXPERT
    )
    
    return state


def analyze_psychonutrition_node(state: RecipeState) -> RecipeState:
    """Enhanced psychonutrition analysis with expert conversation."""
    
    try:
        if not state.recipe:
            state.errors.append("No recipe to analyze")
            return state

        # Load nutrient database
        nutrient_db = load_nutrient_database()

        # Calculate anxiety score
        anxiety_score = calculate_anxiety_score(state.recipe, nutrient_db)

        # Identify key nutrients present
        key_nutrients = []
        mechanisms = []
        recommendations = []

        ingredients = [ing.name.lower() for ing in state.recipe.ingredients]
        
        # Check each nutrient category
        for nutrient_key, nutrient_info in nutrient_db.get("nutrients", {}).items():
            sources = [s.lower() for s in nutrient_info.get("sources", [])]
            if any(source in ing for source in sources for ing in ingredients):
                key_nutrients.append(nutrient_info["name"])
                if nutrient_info.get("mechanism"):
                    mechanisms.append(nutrient_info["mechanism"])
                if nutrient_info.get("recommendation"):
                    recommendations.append(nutrient_info["recommendation"])

        # Create analysis
        analysis = PsychonutritionAnalysis(
            anxiety_score=anxiety_score,
            key_nutrients=key_nutrients[:5],  # Top 5
            mechanisms=mechanisms[:3],  # Top 3
            recommendations=recommendations[:3]  # Top 3
        )

        # Add to recipe
        state.recipe.psychonutrition_analysis = analysis

        # Create expert discussion
        state = create_expert_discussion(state, analysis)

        print(f"🧠 Anxiety Reduction Score: {anxiety_score:.1f}/10")
        print(f"Key nutrients: {', '.join(key_nutrients[:3])}")

    except Exception as e:
        state.errors.append(f"Psychonutrition analysis error: {str(e)}")

    return state