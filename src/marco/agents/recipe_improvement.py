"""Recipe improvement agent based on expert feedback."""

from ..recipe_iterator import recipe_iterator
from ..conversation import conversation_manager
from ..agents.psychonutrition_collaborative import analyze_psychonutrition_node
from ..schemas import RecipeState, ExpertRole, MessageType


def recipe_improvement_node(state: RecipeState) -> RecipeState:
    """Improve recipe based on expert feedback and re-analyze."""

    try:
        # Check if recipe needs improvement
        if not recipe_iterator.should_iterate_recipe(state):
            print("✅ Recipe meets quality standards - no improvements needed")
            return state

        print("🔄 Experts identified issues - improving recipe...")

        # Store original recipe info for comparison
        original_score = state.recipe.psychonutrition_analysis.anxiety_score if state.recipe.psychonutrition_analysis else 0
        original_name = state.recipe.name if state.recipe else "Unknown"

        # Improve the recipe
        state = recipe_iterator.improve_recipe(state)

        # Re-analyze the improved recipe
        print("🧪 Re-analyzing improved recipe...")
        state = analyze_psychonutrition_node(state)

        # Create improvement summary message
        new_score = state.recipe.psychonutrition_analysis.anxiety_score if state.recipe.psychonutrition_analysis else 0
        improvement = new_score - original_score

        summary_msg = f"""🎉 Recipe Improvement Summary!

**Before:** {original_name} - Anxiety Score: {original_score:.1f}/10
**After:** {state.recipe.name} - Anxiety Score: {new_score:.1f}/10
**Improvement:** {'+' if improvement > 0 else ''}{improvement:.1f} points

The collaborative discussion has led to a significantly better recipe for anxiety management!"""

        state = conversation_manager.add_message(
            state,
            from_expert=ExpertRole.PSYCHONUTRITIONIST,
            content=summary_msg,
            message_type=MessageType.FINAL_DECISION
        )

        print(
            f"🚀 Recipe improved! Anxiety score: {original_score:.1f} → {new_score:.1f} (+{improvement:.1f})")

    except Exception as e:
        state.errors.append(f"Recipe improvement error: {str(e)}")

    return state
