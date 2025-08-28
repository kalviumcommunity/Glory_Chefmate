import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
import tiktoken

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def log_tokens(prompt_text, response):
    """Logs the number of tokens used."""
    print(f"\n--- Token Usage ---")
    print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Completion Tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Total Tokens: {response.usage_metadata.total_token_count}")
    print(f"-------------------\n")

def generate_recipe_one_shot(ingredients, meal_type, dietary_restrictions):
    """
    Generates a recipe using one-shot prompting.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # The one-shot example
    example_input = {
        "ingredients": ["salmon", "asparagus", "lemon"],
        "meal_type": "dinner",
        "dietary_restrictions": ["none"]
    }
    example_output = {
        "recipe_name": "Lemon Herb Baked Salmon with Asparagus",
        "ingredients": ["1 salmon fillet", "1 bunch asparagus"],
        "cooking_method": ["Bake salmon and asparagus at 400°F with lemon and herbs."],
        "nutritional_analysis": {"calories": "450 kcal", "protein": "40g"}
    }
    
    user_input_for_llm = {
        "ingredients": ingredients,
        "meal_type": meal_type,
        "dietary_restrictions": dietary_restrictions
    }
    
    user_prompt = f"""
    Generate a recipe based on the user's input, following the exact JSON structure provided in the example.

    Example Input:
    {json.dumps(example_input, indent=2)}

    Example Output:
    {json.dumps(example_output, indent=2)}

    Actual Input:
    {json.dumps(user_input_for_llm, indent=2)}
    """

    print(f"--- One-Shot Prompt Example ---")
    print(f"User Input: Meal Type='{meal_type}', Ingredients='{', '.join(ingredients)}', Restrictions='{', '.join(dietary_restrictions)}'\n")
    print(f"Prompt sent to LLM:\n{user_prompt}\n")

    try:
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        recipe_output = json.loads(response.text)
        print("--- LLM Generated Recipe (One-Shot) ---")
        print(json.dumps(recipe_output, indent=2))
        log_tokens(user_prompt, response)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the One-Shot Example ---
ingredients_list = ["tofu", "bell pepper", "rice noodles"]
meal_type_input = "lunch"
dietary_restrictions_input = ["vegan"]
generate_recipe_one_shot(ingredients_list, meal_type_input, dietary_restrictions_input)