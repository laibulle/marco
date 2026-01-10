"""LangGraph workflow for Marco recipe generation with expert collaboration."""

from typing import Literal

from langgraph.graph import END, StateGraph
from langchain_core.messages import HumanMessage, AIMessage

from marco.agents.recipe_generator import generate_recipe_node
from marco.agents.psychonutrition_collaborative import analyze_psychonutrition_node
from marco.agents.recipe_improvement import recipe_improvement_node
from marco.agents.seasonal_collaborative import seasonal_optimization_node
from marco.agents.chef_collaborative import chef_collaboration_node
from marco.agents.conversation_summary import conversation_summary_node
from marco.schemas import RecipeState


def should_optimize_seasonal(state: RecipeState) -> Literal["seasonal", "chef_review"]:
    """Decide if seasonal optimization is needed."""
    if state.request.season and state.request.season != "auto":
        return "seasonal"
    return "chef_review"


def seasonal_check_node(state: RecipeState) -> RecipeState:
    """Passthrough node for seasonal check when psychonutrition is skipped."""
    return state


def should_analyze_psychonutrition(state: RecipeState) -> Literal["psychonutrition", "seasonal_check"]:
    """Decide if psychonutrition analysis is needed."""
    if state.request.anxiety_focus:
        return "psychonutrition"
    return "seasonal_check"


def should_improve_recipe(state: RecipeState) -> Literal["recipe_improvement", "seasonal_check"]:
    """Decide if recipe needs improvement based on expert feedback."""
    if (state.recipe and
        state.recipe.psychonutrition_analysis and
            state.recipe.psychonutrition_analysis.anxiety_score < 6.0):
        return "recipe_improvement"
    return "seasonal_check"


def create_recipe_graph() -> StateGraph:
    """Create the LangGraph workflow for collaborative recipe generation.

    Enhanced Workflow with Expert Collaboration and Iteration:
    1. Generate base recipe (recipe_generator)
    2. If anxiety_focus: Psychonutrition expert analysis with discussion
    3. If score < 6.0: Recipe improvement based on expert feedback
    4. If season specified: Seasonal expert optimization with collaboration
    5. Chef expert review and technique enhancement
    6. Expert conversation summary and consensus
    7. End
    """
    # Create the state graph
    workflow = StateGraph(RecipeState)

    # Add nodes - now with collaborative experts and improvement
    workflow.add_node("generate_recipe", generate_recipe_node)
    workflow.add_node("psychonutrition", analyze_psychonutrition_node)
    workflow.add_node("recipe_improvement", recipe_improvement_node)
    workflow.add_node("seasonal_check", seasonal_check_node)
    workflow.add_node("seasonal", seasonal_optimization_node)
    workflow.add_node("chef_review", chef_collaboration_node)
    workflow.add_node("expert_summary", conversation_summary_node)

    # Set entry point
    workflow.set_entry_point("generate_recipe")

    # Add edges - enhanced collaboration flow
    workflow.add_conditional_edges(
        "generate_recipe",
        should_analyze_psychonutrition,
        {
            "psychonutrition": "psychonutrition",
            "seasonal_check": "seasonal_check"
        }
    )

    # After psychonutrition, check if recipe needs improvement
    workflow.add_conditional_edges(
        "psychonutrition",
        should_improve_recipe,
        {
            "recipe_improvement": "recipe_improvement",
            "seasonal_check": "seasonal_check"
        }
    )

    # After improvement, go to seasonal check
    workflow.add_edge("recipe_improvement", "seasonal_check")

    # Seasonal check (when skipping psychonutrition) - just a passthrough
    workflow.add_conditional_edges(
        "seasonal_check",
        should_optimize_seasonal,
        {
            "seasonal": "seasonal",
            "chef_review": "chef_review"
        }
    )

    # After seasonal, always go to chef review
    workflow.add_edge("seasonal", "chef_review")

    # After chef review, create expert summary
    workflow.add_edge("chef_review", "expert_summary")

    # End after expert summary
    workflow.add_edge("expert_summary", END)

    # Compile and return the graph
    return workflow.compile()
