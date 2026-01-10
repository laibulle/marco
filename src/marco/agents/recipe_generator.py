"""Recipe generation agent using LLM."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser

from marco.config import settings
from marco.schemas import Recipe, RecipeState


def get_llm():
    """Get the configured LLM."""
    if settings.llm_provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.7,
        )
    elif settings.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=settings.anthropic_model,
            api_key=settings.anthropic_api_key,
            temperature=0.7,
        )
    elif settings.llm_provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=0.7,
        )
    elif settings.llm_provider == "llamacpp":
        # Check if using server mode (connect to llama.cpp server via OpenAI-compatible API)
        if hasattr(settings, 'llamacpp_server_url') and settings.llamacpp_server_url:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                base_url=f"{settings.llamacpp_server_url}/v1",
                api_key="dummy-key",  # llama.cpp server doesn't require real API key
                temperature=settings.llamacpp_temperature,
                max_tokens=settings.llamacpp_max_tokens,
                model="llama-3.2-3b-instruct",  # Model name for server
            )
        else:
            # Local file mode - load GGUF model directly
            from langchain_community.llms import LlamaCpp
            from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

            base_llm = LlamaCpp(
                model_path=settings.llamacpp_model_path,
                max_tokens=settings.llamacpp_max_tokens,
                temperature=settings.llamacpp_temperature,
                n_ctx=settings.llamacpp_n_ctx,
                verbose=False,
            )

            # Wrap it to handle chat messages like other providers
            class LlamaCppChatWrapper:
                def __init__(self, llm):
                    self.llm = llm

                def invoke(self, messages):
                    # Convert messages to a single prompt
                    prompt_parts = []
                    for msg in messages:
                        if hasattr(msg, 'content'):
                            content = msg.content
                        else:
                            content = str(msg)
                        prompt_parts.append(content)
                    prompt = "\\n\\n".join(prompt_parts)

                    # Get response from LLM
                    response_text = self.llm.invoke(prompt)

                    # Return in expected format
                    class Response:
                        def __init__(self, content):
                            self.content = content

                    return Response(response_text)

                def with_structured_output(self, schema):
                    # For llamacpp, we'll use parser like Anthropic
                    return self

            return LlamaCppChatWrapper(base_llm)

            def with_structured_output(self, schema):
                # For llamacpp, we'll use parser like Anthropic
                return self

        return LlamaCppChatWrapper(base_llm)
    else:
        raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")


def generate_recipe_node(state: RecipeState) -> RecipeState:
    """Generate a chef-quality recipe based on the request.

    This agent creates a complete recipe with:
    - Professional chef-quality instructions
    - Precise measurements and timing
    - Chef tips and techniques
    - Nutritional information
    """
    request = state.request

    # Build system prompt
    system_prompt = """You are a world-class chef and nutritionist. You create delicious, healthy recipes that taste amazing while being nutritious.

Your recipes should:
- Have clear, precise instructions that anyone can follow
- Use proper cooking techniques and terminology
- Include chef tips for best results
- Provide accurate nutritional information
- Balance flavors and textures like a professional chef
- Be practical and achievable for home cooks

Focus on making food that is both incredibly tasty AND healthy."""

    # Build user prompt
    user_prompt = f"""Create a chef-quality recipe for: {request.description}

Requirements:
- Number of servings: {request.servings}
- Dietary restrictions: {', '.join(request.dietary_restrictions) if request.dietary_restrictions else 'None'}
- Geographic region: {request.region}
"""

    if request.anxiety_focus:
        user_prompt += "\n- IMPORTANT: Include ingredients rich in anxiety-reducing nutrients (omega-3, magnesium, B vitamins, tryptophan, zinc)"

    if request.season != "auto":
        user_prompt += f"\n- Use ingredients that are in season during: {request.season}"

    user_prompt += """

Provide a complete recipe with:
1. A creative, appetizing name
2. An enticing description
3. Precise ingredient measurements
4. Step-by-step instructions
5. Preparation and cooking times
6. Nutritional information per serving (including micronutrients if anxiety-focused)
7. Chef tips for best results
8. Storage instructions
9. Possible variations

Make it taste incredible while being healthy!"""

    # Get LLM with structured output
    llm = get_llm()
    parser = PydanticOutputParser(pydantic_object=Recipe)

    # For OpenAI, use with_structured_output
    if settings.llm_provider == "openai":
        structured_llm = llm.with_structured_output(Recipe)
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
        recipe = structured_llm.invoke(messages)
    else:
        # For other providers (llamacpp, anthropic, etc), use parser with explicit schema
        if settings.llm_provider == "llamacpp":
            # Simplified prompt for smaller models - minimal for iteration system
            simple_prompt = f"""Create a basic recipe for: {request.description}

JSON format:
{{
  "name": "recipe name",
  "description": "brief description", 
  "prep_time": 15,
  "cook_time": 20,
  "servings": {request.servings},
  "ingredients": [
    {{"name": "main ingredient", "quantity": 1, "unit": "piece"}}
  ],
  "instructions": ["Cook it", "Serve hot"]
}}

Just the JSON:"""

            messages = [HumanMessage(content=simple_prompt)]
            response = llm.invoke(messages)

            # Clean up response - remove any non-JSON content
            content = response.content.strip()

            # Find JSON boundaries
            start_idx = content.find('{')
            end_idx = content.rfind('}')

            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_content = content[start_idx:end_idx + 1]
            else:
                json_content = content

            print(f"Debug - Raw response: {content[:200]}...")
            print(f"Debug - Extracted JSON: {json_content[:200]}...")

            recipe = parser.parse(json_content)
        else:
            # Standard parser approach for anthropic etc
            format_instructions = parser.get_format_instructions()
            messages = [
                SystemMessage(content=system_prompt + "\n\n" + format_instructions +
                              "\n\nCRITICAL INSTRUCTIONS:\n- Output ONLY valid JSON, nothing else\n- Do NOT include markdown formatting, explanations, or any text outside the JSON\n- Start your response with { and end with }\n- Use the EXACT field names from the schema\n- Include ALL required fields"),
                HumanMessage(content=user_prompt +
                             "\n\nOutput ONLY the JSON object. No markdown, no explanations, just pure JSON starting with { and ending with }."),
            ]
            response = llm.invoke(messages)

            # Clean up response - remove markdown code blocks if present
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            recipe = parser.parse(content)

    # Update state
    state.recipe = recipe
    state.messages.append({
        "role": "assistant",
        "content": f"Generated recipe: {recipe.name}",
    })

    return state


# Standalone function for CLI usage
def generate_recipe(description: str, **kwargs) -> Recipe:
    """Generate a recipe (standalone function)."""
    from marco.schemas import RecipeRequest

    request = RecipeRequest(description=description, **kwargs)
    state = RecipeState(request=request, messages=[])
    result_state = generate_recipe_node(state)
    return result_state.recipe
