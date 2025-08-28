import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
import tiktoken

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def log_tokens(prompt_text, response):
    """Logs the number of tokens used."""
    print(f"\n--- Token Usage ---")
    print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Completion Tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Total Tokens: {response.usage_metadata.total_token_count}")
    print(f"-------------------\n")

def generate_recipe_dynamic(ingredients, meal_type, restrictions):
    """
    Builds a prompt dynamically based on user-provided data.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # A simple, flexible prompt template
    base_prompt = "Generate a detailed recipe in JSON format for a {meal_type}."
    
    # Dynamically add ingredients and restrictions
    if ingredients:
        base_prompt += f" It must use the following ingredients: {', '.join(ingredients)}."
    
    if "vegetarian" in restrictions:
        base_prompt += " The recipe must be vegetarian."
    
    if "gluten-free" in restrictions:
        base_prompt += " The recipe must be gluten-free."
    
    # Add the final instruction for JSON format
    base_prompt += " Include 'recipe_name', 'ingredients' list, 'cooking_method', and a 'nutritional_analysis' with calories and protein."

    print(f"--- Dynamic Prompt Example ---")
    print(f"User Input: Meal Type='{meal_type}', Ingredients='{', '.join(ingredients)}', Restrictions='{', '.join(restrictions)}'\n")
    print(f"Prompt sent to LLM:\n{base_prompt}\n")

    try:
        response = model.generate_content(
            base_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                response_mime_type="application/json"
            )
        )
        
        recipe_output = json.loads(response.text)
        print("--- LLM Generated Recipe (Dynamic Prompting) ---")
        print(json.dumps(recipe_output, indent=2))
        log_tokens(base_prompt, response)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the Dynamic Prompting Example ---
ingredients_list = ["quinoa", "black beans", "avocado"]
meal_type_input = "salad"
restrictions_input = ["vegetarian", "gluten-free"]
generate_recipe_dynamic(ingredients_list, meal_type_input, restrictions_input)