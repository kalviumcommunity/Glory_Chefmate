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

def generate_recipe_structured(ingredients, meal_type):
    """
    Generates a recipe, strictly enforcing JSON output using response_mime_type.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    user_prompt = f"""
    Generate a recipe for a {meal_type} using the following ingredients: {', '.join(ingredients)}.
    The JSON should have 'recipe_name', 'ingredients' (list of strings), 'cooking_method' (list of strings), and 'nutritional_analysis' (object with calories, protein, carbs).
    """

    print(f"--- Structured Output Example ---")
    print(f"Prompt sent to LLM:\n{user_prompt}\n")

    try:
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json" # The key for structured output
            )
        )
        
        recipe_output = json.loads(response.text)
        print("--- LLM Generated Recipe (Structured Output) ---")
        print(json.dumps(recipe_output, indent=2))
        log_tokens(user_prompt, response)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the Structured Output Example ---
ingredients_list = ["eggs", "bread", "cheese"]
meal_type_input = "breakfast"
generate_recipe_structured(ingredients_list, meal_type_input)