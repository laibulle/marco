"""Pydantic schemas for Marco recipe system."""

from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from enum import Enum

from pydantic import BaseModel, Field


class ExpertRole(str, Enum):
    """Expert roles in the recipe creation process."""
    NUTRITIONIST = "nutritionist"
    CHEF = "chef"
    SEASONAL_EXPERT = "seasonal_expert"
    PSYCHONUTRITIONIST = "psychonutritionist"


class MessageType(str, Enum):
    """Types of messages experts can exchange."""
    SUGGESTION = "suggestion"
    QUESTION = "question"
    OPINION = "opinion"
    APPROVAL = "approval"
    CONCERN = "concern"
    MODIFICATION = "modification"
    FINAL_DECISION = "final_decision"


class ExpertMessage(BaseModel):
    """Message between experts during recipe creation."""
    
    id: str = Field(description="Unique message ID")
    from_expert: ExpertRole = Field(description="Expert sending the message")
    to_expert: Optional[ExpertRole] = Field(default=None, description="Target expert (None for all)")
    message_type: MessageType = Field(description="Type of message")
    content: str = Field(description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now)
    reference_to: Optional[str] = Field(default=None, description="ID of message this refers to")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class ExpertProfile(BaseModel):
    """Profile and specialization of each expert."""
    
    role: ExpertRole = Field(description="Expert role")
    name: str = Field(description="Expert name")
    specialization: str = Field(description="Area of expertise")
    concerns: List[str] = Field(description="What this expert focuses on")
    communication_style: str = Field(description="How this expert communicates")


class Ingredient(BaseModel):
    """Single ingredient in a recipe."""

    name: str = Field(description="Name of the ingredient")
    quantity: float = Field(
        description="Quantity of the ingredient", validation_alias="amount")
    unit: str = Field(
        description="Unit of measurement (g, ml, cup, tbsp, etc.)")
    notes: Optional[str] = Field(
        default=None, description="Optional notes about the ingredient")

    class Config:
        populate_by_name = True


class NutrientInfo(BaseModel):
    """Nutritional information per serving."""

    calories: int = Field(description="Calories per serving")
    protein_g: float = Field(description="Protein in grams")
    carbs_g: float = Field(description="Carbohydrates in grams")
    fat_g: float = Field(description="Fat in grams")
    fiber_g: float = Field(description="Fiber in grams")

    # Anxiety-related micronutrients
    omega3_mg: Optional[float] = Field(
        default=None, description="Omega-3 fatty acids in mg")
    magnesium_mg: Optional[float] = Field(
        default=None, description="Magnesium in mg")
    vitamin_b6_mg: Optional[float] = Field(
        default=None, description="Vitamin B6 in mg")
    vitamin_b12_mcg: Optional[float] = Field(
        default=None, description="Vitamin B12 in mcg")
    tryptophan_mg: Optional[float] = Field(
        default=None, description="Tryptophan in mg")
    zinc_mg: Optional[float] = Field(default=None, description="Zinc in mg")


class PsychonutritionAnalysis(BaseModel):
    """Psychonutrition analysis for anxiety management."""

    anxiety_score: float = Field(
        description="Anxiety reduction score (0-10, higher is better)", ge=0, le=10
    )
    key_nutrients: List[str] = Field(
        description="Key anxiety-reducing nutrients present in the recipe"
    )
    mechanisms: List[str] = Field(
        description="How these nutrients help reduce anxiety"
    )
    recommendations: List[str] = Field(
        description="Additional recommendations for anxiety management"
    )
    cautions: Optional[List[str]] = Field(
        default=None, description="Any cautions or considerations"
    )


class Recipe(BaseModel):
    """Complete recipe with all details."""

    name: str = Field(description="Name of the recipe")
    description: str = Field(description="Brief description of the dish")

    # Timing and servings
    prep_time: int = Field(description="Preparation time in minutes")
    cook_time: int = Field(description="Cooking time in minutes")
    servings: int = Field(description="Number of servings")

    # Recipe content
    ingredients: List[Ingredient] = Field(description="List of ingredients")
    instructions: List[str] = Field(
        description="Step-by-step cooking instructions", validation_alias="steps")

    class Config:
        populate_by_name = True

    # Nutritional information
    nutrition: Optional[NutrientInfo] = Field(
        default=None, description="Nutritional information per serving")
    psychonutrition_analysis: Optional[PsychonutritionAnalysis] = Field(
        default=None, description="Psychonutrition analysis for anxiety"
    )

    # Metadata
    tags: List[str] = Field(
        default_factory=list, description="Recipe tags (e.g., 'breakfast', 'vegan')")
    difficulty: str = Field(
        default="medium", description="Difficulty level (easy, medium, hard)")
    cuisine: Optional[str] = Field(default=None, description="Cuisine type")
    season: Optional[str] = Field(
        default=None, description="Best season for this recipe")

    # Chef tips
    chef_tips: List[str] = Field(
        default_factory=list, description="Chef tips and tricks")

    # Storage and variations
    storage_instructions: Optional[str] = Field(
        default=None, description="How to store leftovers"
    )
    variations: List[str] = Field(
        default_factory=list, description="Possible variations of the recipe"
    )


class IngredientSubstitution(BaseModel):
    """Seasonal ingredient substitution."""

    original: str = Field(description="Original ingredient")
    substitute: str = Field(description="Seasonal substitute")
    reason: str = Field(description="Reason for substitution")
    adjustment: Optional[str] = Field(
        default=None, description="Any adjustment needed (quantity, cooking time, etc.)"
    )


class SeasonalVariation(BaseModel):
    """Seasonal variation of a recipe."""

    name: str = Field(description="Name of the variation")
    season: str = Field(description="Season (winter, spring, summer, fall)")
    region: str = Field(description="Geographic region")
    substitutions: List[IngredientSubstitution] = Field(
        description="List of ingredient substitutions"
    )
    notes: Optional[str] = Field(default=None, description="Additional notes")


class RecipeRequest(BaseModel):
    """Request to generate a recipe."""

    description: str = Field(description="Description of what to cook")
    anxiety_focus: bool = Field(
        default=True, description="Whether to optimize for anxiety reduction"
    )
    dietary_restrictions: List[str] = Field(
        default_factory=list, description="Dietary restrictions (vegan, gluten-free, etc.)"
    )
    season: str = Field(
        default="auto", description="Season (auto, winter, spring, summer, fall)")
    region: str = Field(default="europe", description="Geographic region")
    servings: int = Field(default=4, description="Number of servings")


class ConversationContext(BaseModel):
    """Context of the expert conversation."""
    
    topic: str = Field(description="Current discussion topic")
    phase: str = Field(description="Current phase (planning, creation, review, finalization)")
    decisions_made: List[str] = Field(default_factory=list, description="Decisions already agreed upon")
    pending_questions: List[str] = Field(default_factory=list, description="Open questions")
    consensus_reached: bool = Field(default=False, description="Whether experts agree")


class RecipeState(BaseModel):
    """State for LangGraph recipe generation workflow with expert collaboration."""

    request: RecipeRequest = Field(description="Original recipe request")
    recipe: Optional[Recipe] = Field(
        default=None, description="Generated recipe")
    seasonal_variation: Optional[SeasonalVariation] = Field(
        default=None, description="Seasonal variation if requested"
    )
    
    # Expert conversation system
    experts: Dict[ExpertRole, ExpertProfile] = Field(
        default_factory=dict, description="Active experts in the conversation")
    conversation: List[ExpertMessage] = Field(
        default_factory=list, description="Expert-to-expert conversation")
    conversation_context: ConversationContext = Field(
        default_factory=lambda: ConversationContext(
            topic="Recipe Planning",
            phase="planning"
        ), 
        description="Current conversation context"
    )
    
    # Legacy support
    messages: List[dict] = Field(
        default_factory=list, description="Legacy message format for compatibility")
    errors: List[str] = Field(default_factory=list,
                              description="Any errors encountered")


class UserProfile(BaseModel):
    """User profile for personalized recipes."""

    user_id: str = Field(description="Unique user identifier")
    dietary_restrictions: List[str] = Field(
        default_factory=list, description="Dietary restrictions"
    )
    anxiety_symptoms: List[str] = Field(
        default_factory=list, description="Anxiety symptoms to address"
    )
    favorite_cuisines: List[str] = Field(
        default_factory=list, description="Favorite cuisine types"
    )
    disliked_ingredients: List[str] = Field(
        default_factory=list, description="Ingredients to avoid"
    )
    region: str = Field(default="europe", description="Geographic region")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
