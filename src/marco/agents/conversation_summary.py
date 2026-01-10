"""Expert conversation summary and finalization."""

from ..conversation import conversation_manager
from ..schemas import RecipeState, ExpertRole, MessageType


def create_final_consensus(state: RecipeState) -> RecipeState:
    """Create final expert consensus and recipe approval."""
    
    if not state.experts or not state.conversation:
        return state
    
    # Dr. Maya provides final nutritional sign-off
    final_nutrition_approval = f"""After our collaborative discussion, I'm pleased to give this recipe my final approval!

**Final Nutritional Assessment:**
✅ Anxiety reduction score: {state.recipe.psychonutrition_analysis.anxiety_score:.1f}/10
✅ Key compounds optimized for bioavailability  
✅ Cooking methods preserve therapeutic properties
✅ Seasonal ingredients at peak nutrient density

The collaboration between culinary technique and nutritional science has created something truly special. This recipe should provide genuine anxiety-reducing benefits while being absolutely delicious.

**My Prescription:** Enjoy this meal mindfully, ideally in good company. The combination of nutrients and the act of sharing food will amplify the anxiety-reducing effects!"""
    
    state = conversation_manager.add_message(
        state,
        from_expert=ExpertRole.PSYCHONUTRITIONIST,
        content=final_nutrition_approval,
        message_type=MessageType.FINAL_DECISION
    )
    
    # Chef Marco provides seasonal sustainability approval
    seasonal_approval = f"""From a seasonal and sustainability perspective, this recipe is perfectly aligned with natural cycles!

**Seasonal Sustainability Score:** 🌿🌿🌿🌿🌿 (5/5)

We're supporting:
• Local farmers by using seasonal produce
• Environmental health through reduced transportation
• Maximum flavor and nutrition from peak-season ingredients
• Traditional food wisdom that honors natural timing

This recipe connects us to the land and the season - which is deeply nourishing for both body and soul."""
    
    state = conversation_manager.add_message(
        state,
        from_expert=ExpertRole.SEASONAL_EXPERT,
        content=seasonal_approval,
        message_type=MessageType.FINAL_DECISION
    )
    
    # Chef Isabella provides final culinary approval
    culinary_approval = f"""Mes amis, this has been a beautiful collaboration! 

**Culinary Excellence:** ⭐⭐⭐⭐⭐ (5/5 stars)

What we've created together is more than a recipe - it's a symphony of:
• **Technique:** Each cooking method optimized for both flavor and nutrition
• **Balance:** Textures, flavors, and nutrients in perfect harmony  
• **Elegance:** Simple enough for home cooking, sophisticated enough for fine dining
• **Soul:** Food that nourishes the mind, body, and spirit

I would be proud to serve this in my restaurant. More importantly, I'm confident it will bring joy and healing to those who prepare and share it.

**Chef's Final Verdict:** Magnifique! 👨‍🍳✨"""
    
    state = conversation_manager.add_message(
        state,
        from_expert=ExpertRole.CHEF,
        content=culinary_approval,
        message_type=MessageType.FINAL_DECISION
    )
    
    # Mark consensus reached
    state.conversation_context.consensus_reached = True
    state.conversation_context.phase = "finalized"
    
    return state


def print_conversation_summary(state: RecipeState) -> None:
    """Print a beautiful summary of the expert conversation."""
    
    if not state.conversation:
        return
    
    print("\\n" + "="*60)
    print("🗣️  EXPERT COLLABORATION SUMMARY")
    print("="*60)
    
    print(f"\\n📋 **Topic:** {state.conversation_context.topic}")
    print(f"🔄 **Phase:** {state.conversation_context.phase}")
    print(f"✅ **Consensus:** {'Reached' if state.conversation_context.consensus_reached else 'In Progress'}")
    
    print("\\n👥 **Expert Participants:**")
    for role, profile in state.experts.items():
        print(f"   • **{profile.name}** - {profile.specialization}")
    
    print(f"\\n💬 **Conversation Highlights:** ({len(state.conversation)} messages)")
    
    # Show key messages
    key_messages = [
        msg for msg in state.conversation 
        if msg.message_type in [MessageType.CONCERN, MessageType.APPROVAL, MessageType.FINAL_DECISION]
    ]
    
    for msg in key_messages[-3:]:  # Last 3 key messages
        expert_name = state.experts[msg.from_expert].name
        emoji = {"concern": "⚠️", "approval": "✅", "final_decision": "🏆"}.get(msg.message_type.value, "💬")
        print(f"\\n   {emoji} **{expert_name}:** {msg.content[:100]}...")
    
    print("\\n" + "="*60)
    print("🎉 Recipe created through collaborative expertise!")
    print("="*60 + "\\n")


def conversation_summary_node(state: RecipeState) -> RecipeState:
    """Finalize expert conversation and create summary."""
    
    try:
        # Create final consensus
        state = create_final_consensus(state)
        
        # Print beautiful summary
        print_conversation_summary(state)
        
    except Exception as e:
        state.errors.append(f"Conversation summary error: {str(e)}")
    
    return state