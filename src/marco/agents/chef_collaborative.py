"""Enhanced chef agent with expert conversation capabilities."""

from ..config import settings  
from ..conversation import conversation_manager
from ..schemas import RecipeState, ExpertRole, MessageType


def create_chef_expert_response(state: RecipeState) -> RecipeState:
    """Chef Isabella responds to other experts and provides culinary insights."""
    
    if not state.recipe:
        return state
    
    # Get conversation context for chef
    conversation = conversation_manager.get_conversation_for_expert(
        state, ExpertRole.CHEF
    )
    
    # Check for questions directed to the chef
    questions_for_chef = [
        msg for msg in conversation 
        if msg.to_expert == ExpertRole.CHEF and msg.message_type == MessageType.QUESTION
    ]
    
    if questions_for_chef:
        latest_question = questions_for_chef[-1]
        
        if "cooking techniques" in latest_question.content.lower() or "maximize" in latest_question.content.lower():
            # Respond to seasonal expert's cooking technique question
            technique_response = f"""Marco, excellent point about seasonal cooking methods! 

For maximizing both nutrition and flavor in this recipe, I recommend:

🔥 **Cooking Technique Optimization:**
• **Low-temperature roasting** (325°F) for nuts - preserves omega-3 oils while developing flavor
• **Quick sauté** for leafy greens - maintains vitamin content while enhancing bioavailability  
• **Gentle steaming** for vegetables - preserves water-soluble B-vitamins crucial for anxiety management

**Technical Notes:**
• Cook magnesium-rich ingredients separately to prevent mineral leaching
• Add fermented components at the end to preserve probiotic benefits
• Use acidic ingredients (lemon, vinegar) to enhance mineral absorption

Maya, from a nutritional standpoint, does this cooking approach align with maximizing the anxiety-reducing compounds?"""
            
            state = conversation_manager.add_message(
                state,
                from_expert=ExpertRole.CHEF,
                content=technique_response,
                message_type=MessageType.OPINION,
                reference_to=latest_question.id
            )
            
            # Also ask follow-up question to psychonutritionist
            nutrition_question = """Dr. Chen, I want to ensure my cooking methods enhance rather than diminish the anxiety-reducing properties. 

Are there specific temperature ranges or cooking times I should avoid to preserve the bioactive compounds? 
Also, should certain ingredients be combined in specific ways for better absorption?"""
            
            state = conversation_manager.add_message(
                state,
                from_expert=ExpertRole.CHEF,
                content=nutrition_question,
                message_type=MessageType.QUESTION,
                to_expert=ExpertRole.PSYCHONUTRITIONIST
            )
    
    # Provide general culinary assessment
    culinary_assessment = f"""Looking at this recipe from a purely culinary perspective:

**Technique Assessment:**
• The flavor profile balances umami, acid, and natural sweetness well
• Cooking times are appropriate for ingredient sizes
• The progression from aromatics to proteins to vegetables follows classic French technique

**Potential Refinements:**
• Consider blooming spices in oil first to enhance flavor compounds
• A final acid touch (lemon zest) could brighten the dish and aid mineral absorption
• Temperature control will be crucial for the delicate anxiety-reducing compounds

**Presentation Notes:**
• This dish will have beautiful natural colors that indicate high antioxidant content
• The varied textures should create an engaging eating experience
• Proper plating can make this both nourishing and restaurant-quality

I'm confident this recipe achieves both culinary excellence and therapeutic benefits!"""
    
    state = conversation_manager.add_message(
        state,
        from_expert=ExpertRole.CHEF,
        content=culinary_assessment,
        message_type=MessageType.APPROVAL
    )
    
    return state


def enhance_recipe_with_chef_insights(state: RecipeState) -> RecipeState:
    """Add chef insights to the recipe based on expert conversation."""
    
    if not state.recipe:
        return state
    
    # Add chef tips based on the conversation
    chef_tips = [
        "Bloom spices in oil for 30 seconds to enhance flavor compounds",
        "Cook magnesium-rich ingredients separately to prevent mineral leaching",
        "Add fermented components at the end to preserve probiotic benefits",
        "Use low-temperature cooking for omega-3 rich ingredients",
        "Finish with acid (lemon) to enhance mineral absorption"
    ]
    
    # Add to recipe
    if not state.recipe.chef_tips:
        state.recipe.chef_tips = []
    
    state.recipe.chef_tips.extend([tip for tip in chef_tips if tip not in state.recipe.chef_tips])
    
    # Update difficulty based on conversation insights
    if len(state.recipe.chef_tips) > 3:
        state.recipe.difficulty = "medium"
    
    return state


def chef_collaboration_node(state: RecipeState) -> RecipeState:
    """Chef expert collaboration node."""
    
    try:
        # Initialize experts if needed
        if not state.experts:
            state = conversation_manager.initialize_experts(state)
        
        # Update context
        state = conversation_manager.update_context(
            state,
            topic="Culinary Refinement", 
            phase="refinement"
        )
        
        # Create expert responses
        state = create_chef_expert_response(state)
        
        # Enhance recipe with insights
        state = enhance_recipe_with_chef_insights(state)
        
        print("👨‍🍳 Chef Isabella has reviewed and enhanced the recipe")
        
    except Exception as e:
        state.errors.append(f"Chef collaboration error: {str(e)}")
    
    return state