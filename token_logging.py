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

def demonstrate_token_logging(text_input):
    """
    Demonstrates token logging for a simple recipe generation.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    user_prompt = f"Create a simple recipe name and a short ingredients list using: {text_input}"

    print(f"--- Token Logging Example ---")
    print(f"Prompt sent to LLM:\n{user_prompt}\n")

    try:
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        recipe_output = json.loads(response.text)
        print("--- LLM Generated Output ---")
        print(json.dumps(recipe_output, indent=2))
        log_tokens(user_prompt, response) # The token logging function call

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the Token Logging Example ---
demonstrate_token_logging("flour, sugar, butter, eggs")