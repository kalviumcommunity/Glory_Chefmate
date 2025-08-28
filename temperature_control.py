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

def generate_recipe_with_temperature(ingredients, meal_type, temp_value):
    """
    Generates a recipe, demonstrating the effect of the temperature parameter.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    user_prompt = f"Generate a recipe for a {meal_type} using the following ingredients: {', '.join(ingredients)}. Include recipe_name, ingredients list, cooking_method, and a simple nutritional_analysis."

    print(f"--- Temperature Control Example (Temp: {temp_value}) ---")
    print(f"Prompt sent to LLM:\n{user_prompt}\n")

    try:
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temp_value, # The temperature parameter
                response_mime_type="application/json"
            )
        )
        
        recipe_output = json.loads(response.text)
        print(f"--- LLM Generated Recipe (Temperature: {temp_value}) ---")
        print(json.dumps(recipe_output, indent=2))
        log_tokens(user_prompt, response)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the Temperature Control Example ---
ingredients_list = ["potatoes", "cheese", "bacon"]
meal_type_input = "side dish"

print("--- Running with LOW Temperature (0.2) for predictable output ---")
generate_recipe_with_temperature(ingredients_list, meal_type_input, 0.2)

print("\n" + "="*80 + "\n")

print("--- Running with HIGH Temperature (0.8) for creative output ---")
generate_recipe_with_temperature(ingredients_list, meal_type_input, 0.8)