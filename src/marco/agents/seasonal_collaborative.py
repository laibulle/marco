"""Enhanced seasonal optimization agent with expert conversation."""

import json
from datetime import datetime
from typing import List, Dict

from ..config import settings
from ..conversation import conversation_manager
from ..schemas import (
    RecipeState, IngredientSubstitution, SeasonalVariation,
    ExpertRole, MessageType
)


def load_seasonal_data() -> Dict:
    """Load seasonal ingredient data."""
    seasonal_file = settings.data_dir / "seasonal_ingredients.json"
    if not seasonal_file.exists():
        return {"seasons": {}, "regions": {}}

    with open(seasonal_file) as f:
        return json.load(f)


def get_current_season() -> str:
    """Get current season based on date."""
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "fall"


def create_seasonal_expert_response(state: RecipeState) -> RecipeState:
    """Chef Marco responds to psychonutrition questions and provides seasonal insights."""
    
    # Get conversation context
    conversation = conversation_manager.get_conversation_for_expert(
        state, ExpertRole.SEASONAL_EXPERT
    )
    
    # Check if psychonutritionist asked about seasonality
    psycho_questions = [
        msg for msg in conversation 
        if msg.from_expert == ExpertRole.PSYCHONUTRITIONIST 
        and msg.message_type == MessageType.QUESTION
    ]
    
    current_season = get_current_season()
    seasonal_data = load_seasonal_data()
    
    if psycho_questions:
        # Respond to Dr. Maya's question about ingredient seasonality
        response_msg = f"""Maya, great question about seasonal nutrient density! 

Looking at this recipe for {current_season}, I have some insights:

🌱 **Current Season Analysis ({current_season.title()}):**
"""
        
        # Analyze each ingredient for seasonality
        if state.recipe:
            seasonal_notes = []
            for ingredient in state.recipe.ingredients[:5]:  # Check first 5 ingredients
                ing_name = ingredient.name.lower()
                
                # Check if ingredient is in season
                season_ingredients = seasonal_data.get("seasons", {}).get(current_season, [])
                season_ingredients_lower = [s.lower() for s in season_ingredients]
                
                if any(si in ing_name for si in season_ingredients_lower):
                    seasonal_notes.append(f"✅ {ingredient.name} - Perfect timing! Peak season now")
                else:
                    seasonal_notes.append(f"⚠️  {ingredient.name} - Out of season, consider alternatives")
            
            response_msg += "\\n".join(seasonal_notes[:3])  # Top 3
        
        response_msg += f"""

**My Seasonal Recommendations:**
• For maximum omega-3 absorption, fresh walnuts are at their best right now
• Winter greens like kale and spinach have concentrated nutrients from slower growth
• If we need magnesium, I suggest seasonal pumpkin seeds - they're stored at peak quality

Should we make any seasonal swaps to boost the nutritional profile while working with nature's timing?"""
        
        state = conversation_manager.add_message(
            state,
            from_expert=ExpertRole.SEASONAL_EXPERT,
            content=response_msg,
            message_type=MessageType.OPINION,
            to_expert=ExpertRole.PSYCHONUTRITIONIST
        )
    
    # Also address the chef if there are cooking considerations
    chef_suggestion = f"""Isabella, from a seasonal cooking perspective:

The {current_season} season affects our cooking methods too. These ingredients will have different moisture content and cooking times than their off-season versions. 

For example:
• Root vegetables are denser and sweeter now - they'll caramelize beautifully
• Leafy greens are more robust - they can handle higher heat
• Stored nuts have concentrated oils - perfect for bringing out anxiety-reducing compounds

What cooking techniques would you recommend to maximize both flavor and nutritional benefits?"""
    
    state = conversation_manager.add_message(
        state,
        from_expert=ExpertRole.SEASONAL_EXPERT,
        content=chef_suggestion,
        message_type=MessageType.QUESTION,
        to_expert=ExpertRole.CHEF
    )
    
    return state


def seasonal_optimization_node(state: RecipeState) -> RecipeState:
    """Enhanced seasonal optimization with expert collaboration."""
    
    try:
        if not state.recipe:
            state.errors.append("No recipe to optimize for season")
            return state

        # Initialize experts if needed
        if not state.experts:
            state = conversation_manager.initialize_experts(state)

        # Update conversation context
        state = conversation_manager.update_context(
            state,
            topic="Seasonal Optimization",
            phase="optimization"
        )

        # Create expert response
        state = create_seasonal_expert_response(state)

        # Load seasonal data for actual optimization
        seasonal_data = load_seasonal_data()
        current_season = state.request.season
        
        if current_season == "auto":
            current_season = get_current_season()

        # Create seasonal variation
        substitutions = []
        season_ingredients = seasonal_data.get("seasons", {}).get(current_season, [])
        
        if state.recipe and season_ingredients:
            for ingredient in state.recipe.ingredients:
                # Simple heuristic for substitutions
                if "tomato" in ingredient.name.lower() and current_season == "winter":
                    substitutions.append(IngredientSubstitution(
                        original=ingredient.name,
                        substitute="canned tomatoes",
                        reason="Fresh tomatoes are out of season",
                        adjustment="Use high-quality canned for better flavor"
                    ))

        if substitutions:
            seasonal_variation = SeasonalVariation(
                name=f"{state.recipe.name} - {current_season.title()} Variation",
                season=current_season,
                region=state.request.region,
                substitutions=substitutions,
                notes=f"Optimized for {current_season} ingredients"
            )
            state.seasonal_variation = seasonal_variation
            
            # Announce the optimization
            optimization_msg = f"""I've created a {current_season} variation of this recipe! 

**Seasonal Optimizations:**
{chr(10).join('• ' + sub.reason + ': ' + sub.original + ' → ' + sub.substitute for sub in substitutions)}

This ensures we're working with ingredients at their peak quality and supporting local growing cycles."""
            
            state = conversation_manager.add_message(
                state,
                from_expert=ExpertRole.SEASONAL_EXPERT,
                content=optimization_msg,
                message_type=MessageType.FINAL_DECISION
            )

        print(f"🌿 Seasonal optimization for {current_season} complete")

    except Exception as e:
        state.errors.append(f"Seasonal optimization error: {str(e)}")

    return state