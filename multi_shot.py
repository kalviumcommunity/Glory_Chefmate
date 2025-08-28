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

def generate_recipe_multi_shot(ingredients, meal_type, restrictions):
    """
    Generates a recipe using multi-shot prompting with several examples.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Define multiple examples
    examples = [
        # Example 1: Classic Dish
        {
            "input": {"ingredients": ["beef", "onions", "potatoes"], "meal_type": "dinner"},
            "output": {
                "recipe_name": "Classic Beef Stew",
                "ingredients": ["1 lb beef stew meat", "2 large potatoes", "1 large onion"],
                "cooking_method": ["Sear beef in a pot. Add vegetables and broth. Simmer until tender."],
            }
        },
        # Example 2: Vegetarian Dish
        {
            "input": {"ingredients": ["chickpeas", "tomatoes", "spinach"], "meal_type": "lunch"},
            "output": {
                "recipe_name": "Hearty Chickpea and Spinach Curry",
                "ingredients": ["1 can chickpeas", "2 large tomatoes", "2 cups fresh spinach"],
                "cooking_method": ["Sauté onions and garlic. Add tomatoes and chickpeas. Stir in spinach."],
            }
        }
    ]

    # Create the user prompt with all examples
    user_prompt = "Generate a recipe following the format below. Make sure the output is a single JSON object."
    for example in examples:
        user_prompt += f"\n\nInput:\n{json.dumps(example['input'], indent=2)}\n\nOutput:\n{json.dumps(example['output'], indent=2)}"
    
    # Add the actual input for the model to work on
    user_prompt += f"\n\nInput:\n{json.dumps({'ingredients': ingredients, 'meal_type': meal_type}, indent=2)}\n\nOutput:\n"

    print(f"--- Multi-Shot Prompt Example ---")
    print(f"User Input: Meal Type='{meal_type}', Ingredients='{', '.join(ingredients)}'\n")
    print(f"Prompt sent to LLM:\n{user_prompt}\n")

    try:
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                response_mime_type="application/json"
            )
        )
        
        recipe_output = json.loads(response.text)
        print("--- LLM Generated Recipe (Multi-Shot) ---")
        print(json.dumps(recipe_output, indent=2))
        log_tokens(user_prompt, response)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the Multi-Shot Example ---
ingredients_list = ["ground turkey", "cabbage", "carrots"]
meal_type_input = "dinner"
restrictions_input = ["none"]
generate_recipe_multi_shot(ingredients_list, meal_type_input, restrictions_input)