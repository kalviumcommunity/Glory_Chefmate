import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
import tiktoken

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def log_tokens(prompt_text, response):
    """Logs the number of tokens used."""
    # The Gemini API provides token counts directly in the response object
    print(f"\n--- Token Usage ---")
    print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Completion Tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Total Tokens: {response.usage_metadata.total_token_count}")
    print(f"-------------------\n")

def generate_recipe_zero_shot(ingredients, meal_type):
    """
    Generates a recipe using zero-shot prompting.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    user_prompt = f"Generate a detailed recipe in JSON format for a {meal_type} using the following ingredients: {', '.join(ingredients)}. Include 'recipe_name', 'ingredients' list, 'cooking_method', and a 'nutritional_analysis' with calories, protein, and carbs."

    print(f"--- Zero-Shot Prompt Example ---")
    print(f"User Input: Meal Type='{meal_type}', Ingredients='{', '.join(ingredients)}'\n")
    print(f"Prompt sent to LLM:\n{user_prompt}\n")

    try:
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        # The response is a JSON string, so we need to parse it
        recipe_output = json.loads(response.text)
        print("--- LLM Generated Recipe (Zero-Shot) ---")
        print(json.dumps(recipe_output, indent=2))
        log_tokens(user_prompt, response)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the Zero-Shot Example ---
ingredients_list = ["chicken", "rice", "spinach"]
meal_type_input = "dinner"
generate_recipe_zero_shot(ingredients_list, meal_type_input)