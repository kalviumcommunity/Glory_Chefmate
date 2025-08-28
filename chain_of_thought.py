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

def generate_recipe_cot(ingredients, meal_type, dietary_restrictions):
    """
    Generates a recipe using Chain-of-Thought prompting for detailed nutritional analysis.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    cot_steps = """
    Let's think step by step to ensure a high-quality recipe.
    1.  First, create a delicious recipe name and list all ingredients.
    2.  Second, write out the cooking instructions in a clear, step-by-step manner.
    3.  Third, analyze the nutritional content of the main ingredients and provide an estimate for calories, protein, and carbs.
    4.  Fourth, assign a 'health score' on a scale of 1-10 based on the nutritional analysis.
    5.  Fifth, write a brief reasoning for the assigned health score.
    6.  Finally, combine all this information into a single JSON object.
    """
    
    user_prompt = f"""
    You are an expert chef and nutritionist. Generate a recipe for a {meal_type} using the ingredients {', '.join(ingredients)} and considering these dietary restrictions: {', '.join(dietary_restrictions)}.

    {cot_steps}
    """
    
    print(f"--- Chain-of-Thought Prompt Example ---")
    print(f"Prompt sent to LLM:\n{user_prompt}\n")

    try:
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        recipe_output = json.loads(response.text)
        print("--- LLM Generated Recipe (Chain-of-Thought) ---")
        print(json.dumps(recipe_output, indent=2))
        log_tokens(user_prompt, response)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the Chain-of-Thought Example ---
ingredients_list = ["lentils", "carrots", "onions"]
meal_type_input = "soup"
dietary_restrictions_input = ["vegan"]
generate_recipe_cot(ingredients_list, meal_type_input, dietary_restrictions_input)