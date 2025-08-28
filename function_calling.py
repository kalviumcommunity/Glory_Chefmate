import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Step 1: Define the external tool/function
def get_nutritional_info(ingredient_name: str) -> dict:
    """A mock function to get nutritional info for a given ingredient."""
    print(f"**Application is calling the external function: get_nutritional_info('{ingredient_name}')**")
    mock_db = {
        "chicken": {"calories": 165, "protein": 31, "carbs": 0},
        "rice": {"calories": 130, "protein": 2.7, "carbs": 28},
        "spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6},
    }
    # Return a dictionary with the mock data
    return mock_db.get(ingredient_name.lower(), {"calories": "N/A", "protein": "N/A", "carbs": "N/A"})

# Step 2: Define the function declaration for the model
function_declarations = [
    {
        "name": "get_nutritional_info",
        "description": "Get the approximate nutritional information (calories, protein, carbs) for a food ingredient.",
        "parameters": {
            "type": "object",
            "properties": {
                "ingredient_name": {
                    "type": "string",
                    "description": "The name of the food ingredient.",
                }
            },
            "required": ["ingredient_name"],
        }
    }
]

def generate_recipe_with_tools(ingredients):
    """
    Generates a recipe and uses a function call to get nutritional data.
    """
    model = genai.GenerativeModel('gemini-1.5-flash', tools=function_declarations)
    
    # The user prompt that the model will interpret
    user_prompt = f"Create a simple recipe using: {', '.join(ingredients)}. Also, tell me the calories and protein for each ingredient."

    print(f"--- Function Calling Example ---")
    print(f"User Request: '{user_prompt}'\n")

    try:
        # Step 3: Send the request to the model
        response = model.generate_content(user_prompt)
        
        # Step 4: Check if the model wants to call a function
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            
            # Step 5: Execute the function and get the result
            if function_name == "get_nutritional_info":
                ingredient = function_call.args["ingredient_name"]
                result = get_nutritional_info(ingredient)

                # Step 6: Send the function's result back to the model
                second_response = model.generate_content(
                    genai.types.tool_response.ToolResponse(
                        name="get_nutritional_info",
                        response=result,
                    )
                )
                print("\n**Model received the function result and is now generating the final response.**\n")
                print("--- LLM Generated Recipe (via Function Call) ---")
                print(second_response.text)
                
            else:
                print("Model requested a function that does not exist.")
        else:
            print("Model did not request a function call.")
            print("--- LLM Generated Response ---")
            print(response.text)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the Function Calling Example ---
ingredients_list = ["chicken", "rice", "spinach"]
generate_recipe_with_tools(ingredients_list)