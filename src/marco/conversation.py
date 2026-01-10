"""Expert conversation management for Marco recipe system."""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from .schemas import (
    ExpertRole, MessageType, ExpertMessage, ExpertProfile, 
    ConversationContext, RecipeState
)


class ConversationManager:
    """Manages conversations between recipe experts."""
    
    def __init__(self):
        """Initialize the conversation manager with expert profiles."""
        self.expert_profiles = {
            ExpertRole.PSYCHONUTRITIONIST: ExpertProfile(
                role=ExpertRole.PSYCHONUTRITIONIST,
                name="Dr. Maya Chen",
                specialization="Psychonutrition and anxiety management",
                concerns=[
                    "anxiety-reducing nutrients",
                    "mood-stabilizing compounds",
                    "stress-response optimization",
                    "gut-brain axis health"
                ],
                communication_style="Scientific but approachable, focuses on evidence-based nutrition"
            ),
            ExpertRole.SEASONAL_EXPERT: ExpertProfile(
                role=ExpertRole.SEASONAL_EXPERT,
                name="Chef Marco Rossi",
                specialization="Seasonal and sustainable cooking",
                concerns=[
                    "ingredient seasonality",
                    "local availability",
                    "environmental impact",
                    "peak flavor timing"
                ],
                communication_style="Passionate about seasonality, speaks from experience with local farms"
            ),
            ExpertRole.CHEF: ExpertProfile(
                role=ExpertRole.CHEF,
                name="Chef Isabella Laurent",
                specialization="Culinary technique and flavor harmony",
                concerns=[
                    "cooking techniques",
                    "flavor balance",
                    "texture combinations",
                    "presentation",
                    "cooking times and temperatures"
                ],
                communication_style="Detail-oriented, focuses on technique and perfect execution"
            )
        }
    
    def initialize_experts(self, state: RecipeState) -> RecipeState:
        """Initialize expert profiles in the recipe state."""
        state.experts = self.expert_profiles.copy()
        return state
    
    def add_message(
        self,
        state: RecipeState,
        from_expert: ExpertRole,
        content: str,
        message_type: MessageType = MessageType.SUGGESTION,
        to_expert: Optional[ExpertRole] = None,
        reference_to: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RecipeState:
        """Add a message to the expert conversation."""
        
        message = ExpertMessage(
            id=str(uuid.uuid4()),
            from_expert=from_expert,
            to_expert=to_expert,
            message_type=message_type,
            content=content,
            reference_to=reference_to,
            metadata=metadata or {}
        )
        
        state.conversation.append(message)
        return state
    
    def get_conversation_for_expert(
        self, 
        state: RecipeState, 
        expert: ExpertRole,
        include_general: bool = True
    ) -> List[ExpertMessage]:
        """Get messages relevant to a specific expert."""
        messages = []
        
        for msg in state.conversation:
            # Messages to this expert specifically
            if msg.to_expert == expert:
                messages.append(msg)
            # Messages from this expert
            elif msg.from_expert == expert:
                messages.append(msg)
            # General messages (when to_expert is None) if requested
            elif include_general and msg.to_expert is None:
                messages.append(msg)
        
        return messages
    
    def format_conversation_history(
        self, 
        state: RecipeState,
        for_expert: Optional[ExpertRole] = None
    ) -> str:
        """Format conversation history for LLM context."""
        
        if for_expert:
            messages = self.get_conversation_for_expert(state, for_expert)
        else:
            messages = state.conversation
        
        if not messages:
            return "No previous conversation."
        
        formatted = ["=== EXPERT CONVERSATION ===\n"]
        
        for msg in messages[-10:]:  # Last 10 messages to avoid token limits
            expert_name = state.experts[msg.from_expert].name
            target = f" → {state.experts[msg.to_expert].name}" if msg.to_expert else " → All"
            
            formatted.append(f"**{expert_name}** ({msg.message_type.value}){target}:")
            formatted.append(f"  {msg.content}\n")
        
        return "\n".join(formatted)
    
    def check_consensus(self, state: RecipeState) -> bool:
        """Check if experts have reached consensus on the current topic."""
        recent_messages = state.conversation[-5:]  # Check last 5 messages
        
        approval_count = sum(
            1 for msg in recent_messages 
            if msg.message_type == MessageType.APPROVAL
        )
        concern_count = sum(
            1 for msg in recent_messages 
            if msg.message_type == MessageType.CONCERN
        )
        
        # Simple heuristic: more approvals than concerns
        return approval_count > concern_count
    
    def update_context(
        self, 
        state: RecipeState, 
        topic: Optional[str] = None,
        phase: Optional[str] = None,
        decision: Optional[str] = None,
        question: Optional[str] = None
    ) -> RecipeState:
        """Update conversation context."""
        
        if topic:
            state.conversation_context.topic = topic
        
        if phase:
            state.conversation_context.phase = phase
        
        if decision:
            state.conversation_context.decisions_made.append(decision)
        
        if question:
            state.conversation_context.pending_questions.append(question)
        
        state.conversation_context.consensus_reached = self.check_consensus(state)
        
        return state
    
    def get_expert_prompt_context(
        self, 
        state: RecipeState, 
        expert: ExpertRole
    ) -> str:
        """Get context for an expert's prompt including conversation history."""
        
        expert_profile = state.experts[expert]
        conversation_history = self.format_conversation_history(state, expert)
        
        context = f"""You are {expert_profile.name}, a {expert_profile.specialization} expert.

Your expertise focuses on: {', '.join(expert_profile.concerns)}
Your communication style: {expert_profile.communication_style}

CURRENT CONTEXT:
- Topic: {state.conversation_context.topic}
- Phase: {state.conversation_context.phase}
- Previous decisions: {', '.join(state.conversation_context.decisions_made) if state.conversation_context.decisions_made else 'None'}
- Pending questions: {', '.join(state.conversation_context.pending_questions) if state.conversation_context.pending_questions else 'None'}

{conversation_history}

You are collaborating with other experts to create the perfect recipe. Consider their input and respond naturally as your expert persona would.
"""
        
        return context


# Global conversation manager instance
conversation_manager = ConversationManager()