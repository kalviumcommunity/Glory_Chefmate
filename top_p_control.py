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

def generate_recipe_with_top_p(ingredients, meal_type, top_p_value):
    """
    Generates a recipe, demonstrating the effect of the top_p parameter.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    user_prompt = f"Generate a recipe for a {meal_type} using the following ingredients: {', '.join(ingredients)}. Include recipe_name, ingredients list, cooking_method, and a simple nutritional_analysis."

    print(f"--- Top P Control Example (Top P: {top_p_value}) ---")
    print(f"Prompt sent to LLM:\n{user_prompt}\n")

    try:
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7, # Keep temperature constant to isolate top_p effect
                top_p=top_p_value, # The top_p parameter
                response_mime_type="application/json"
            )
        )
        
        recipe_output = json.loads(response.text)
        print(f"--- LLM Generated Recipe (Top P: {top_p_value}) ---")
        print(json.dumps(recipe_output, indent=2))
        log_tokens(user_prompt, response)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the Top P Control Example ---
ingredients_list = ["pasta", "tomato", "basil"]
meal_type_input = "dinner"

print("--- Running with LOW Top P (0.1) for predictable vocabulary ---")
generate_recipe_with_top_p(ingredients_list, meal_type_input, 0.1)

print("\n" + "="*80 + "\n")

print("--- Running with HIGH Top P (0.9) for diverse vocabulary ---")
generate_recipe_with_top_p(ingredients_list, meal_type_input, 0.9)